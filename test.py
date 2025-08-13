import argparse
import os
import socket
import sys
import threading
import time
from typing import List, Tuple


ENCODING = "utf-8"
BUFFER_SIZE = 4096


class ClientConnection:
    """Represents a connected client with read/write file objects and metadata."""

    def __init__(self, conn: socket.socket, address: Tuple[str, int], display_name: str = "") -> None:
        self.socket = conn
        self.address = address
        self.display_name = display_name
        self.read_file = conn.makefile("r", encoding=ENCODING, newline="\n")
        self.write_file = conn.makefile("w", encoding=ENCODING, newline="\n")
        self.alive = True

    def send_line(self, text: str) -> None:
        if not self.alive:
            return
        try:
            self.write_file.write(text + "\n")
            self.write_file.flush()
        except Exception:
            self.alive = False

    def close(self) -> None:
        self.alive = False
        try:
            try:
                self.read_file.close()
            finally:
                self.write_file.close()
        finally:
            self.socket.close()


class ChatServer:
    """
    A minimal, safe, line-based chat server.

    - Accepts multiple clients using a thread per client.
    - Broadcasts messages to all connected clients.
    - No command execution, file access, or privileged operations.
    """

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.server_socket: socket.socket | None = None
        self.client_connections: List[ClientConnection] = []
        self.client_lock = threading.Lock()
        self.shutdown_event = threading.Event()

    def start(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(50)
        print(f"[SERVER] Listening on {self.host}:{self.port}")

        try:
            while not self.shutdown_event.is_set():
                try:
                    self.server_socket.settimeout(1.0)
                    conn, addr = self.server_socket.accept()
                except socket.timeout:
                    continue

                client = ClientConnection(conn, addr)
                client.send_line("SERVER: Welcome! Please send your display name as the first line.")
                thread = threading.Thread(target=self._handle_client, args=(client,), daemon=True)
                thread.start()
        except KeyboardInterrupt:
            print("\n[SERVER] Shutdown requested (Ctrl+C). Closing...")
        finally:
            self._shutdown()

    def _handle_client(self, client: ClientConnection) -> None:
        try:
            # First line should be the client's display name
            name_line = client.read_file.readline()
            if not name_line:
                client.close()
                return
            client.display_name = name_line.strip() or f"guest-{client.address[0]}:{client.address[1]}"

            with self.client_lock:
                self.client_connections.append(client)
            self._broadcast(f"SERVER: {client.display_name} joined the chat.", exclude=client)
            client.send_line("SERVER: You are connected. Type 'exit' to quit.")

            while True:
                line = client.read_file.readline()
                if not line:
                    break
                message = line.rstrip("\n")
                if message.lower() == "exit":
                    client.send_line("SERVER: Goodbye!")
                    break
                self._broadcast(f"{client.display_name}: {message}", exclude=None)
        except Exception as exc:
            print(f"[SERVER] Error with {client.address}: {exc}")
        finally:
            with self.client_lock:
                if client in self.client_connections:
                    self.client_connections.remove(client)
            self._broadcast(f"SERVER: {client.display_name or client.address} left the chat.", exclude=client)
            client.close()

    def _broadcast(self, text: str, exclude: ClientConnection | None) -> None:
        with self.client_lock:
            dead_clients: List[ClientConnection] = []
            for other in self.client_connections:
                if exclude is not None and other is exclude:
                    continue
                other.send_line(text)
                if not other.alive:
                    dead_clients.append(other)
            for dead in dead_clients:
                if dead in self.client_connections:
                    self.client_connections.remove(dead)
                dead.close()

    def _shutdown(self) -> None:
        self.shutdown_event.set()
        if self.server_socket is not None:
            try:
                self.server_socket.close()
            except Exception:
                pass
        with self.client_lock:
            for client in list(self.client_connections):
                client.close()
            self.client_connections.clear()
        print("[SERVER] Closed.")


class ChatClient:
    """
    A simple chat client that connects to the ChatServer.
    """

    def __init__(self, host: str, port: int, display_name: str) -> None:
        self.host = host
        self.port = port
        self.display_name = display_name
        self.socket: socket.socket | None = None
        self.read_file = None
        self.write_file = None
        self.stop_event = threading.Event()

    def start(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.read_file = self.socket.makefile("r", encoding=ENCODING, newline="\n")
        self.write_file = self.socket.makefile("w", encoding=ENCODING, newline="\n")

        # Read initial server greeting if present (non-blocking-ish)
        self.socket.settimeout(1.0)
        try:
            greeting = self.read_file.readline()
            if greeting:
                print(greeting.rstrip("\n"))
        except Exception:
            pass
        finally:
            self.socket.settimeout(None)

        # Send our display name as the first line
        self._send_line(self.display_name)

        # Start receiver thread
        receiver = threading.Thread(target=self._receiver_loop, daemon=True)
        receiver.start()

        print("[CLIENT] Connected. Type messages and press Enter. Type 'exit' to quit.")
        self._input_loop()

    def _send_line(self, text: str) -> None:
        if self.write_file is None:
            return
        self.write_file.write(text + "\n")
        self.write_file.flush()

    def _receiver_loop(self) -> None:
        assert self.read_file is not None
        try:
            while not self.stop_event.is_set():
                line = self.read_file.readline()
                if not line:
                    print("[CLIENT] Disconnected from server.")
                    self.stop_event.set()
                    break
                print(line.rstrip("\n"))
        except Exception as exc:
            print(f"[CLIENT] Error receiving: {exc}")
            self.stop_event.set()

    def _input_loop(self) -> None:
        try:
            for user_input in sys.stdin:
                text = user_input.rstrip("\n")
                if text.lower() == "exit":
                    self._send_line(text)
                    break
                self._send_line(text)
                if self.stop_event.is_set():
                    break
        except KeyboardInterrupt:
            print("\n[CLIENT] Exiting...")
        finally:
            self.stop_event.set()
            self._close()

    def _close(self) -> None:
        try:
            if self.read_file is not None:
                self.read_file.close()
        finally:
            try:
                if self.write_file is not None:
                    self.write_file.close()
            finally:
                if self.socket is not None:
                    self.socket.close()


def _detect_default_name() -> str:
    user = os.getenv("USER") or os.getenv("USERNAME")
    if user:
        return user
    return f"user-{os.getpid()}"


def run_server(host: str, port: int) -> None:
    server = ChatServer(host, port)
    server.start()


def run_client(host: str, port: int, name: str) -> None:
    client = ChatClient(host, port, name)
    client.start()


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Safe demo: simple multi-client chat server/client",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    server_parser = subparsers.add_parser("server", help="Run the chat server")
    server_parser.add_argument("--host", default="0.0.0.0", help="Host/IP to bind")
    server_parser.add_argument("--port", type=int, default=9999, help="Port to listen on")

    client_parser = subparsers.add_parser("client", help="Run the chat client")
    client_parser.add_argument("--host", default="127.0.0.1", help="Server host/IP to connect to")
    client_parser.add_argument("--port", type=int, default=9999, help="Server port to connect to")
    client_parser.add_argument("--name", default=_detect_default_name(), help="Display name to use in chat")

    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)

    if args.command == "server":
        run_server(args.host, args.port)
        return

    if args.command == "client":
        run_client(args.host, args.port, args.name)
        return

    raise SystemExit(2)


if __name__ == "__main__":
    # Small delay to make Ctrl+C messaging cleaner in some terminals
    try:
        main()
    except KeyboardInterrupt:
        time.sleep(0.05)
        print("\n[INFO] Interrupted by user.")