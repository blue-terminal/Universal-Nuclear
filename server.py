# Importazione delle librerie necessarie
import socket  # Per la comunicazione di rete
import threading  # Per gestire più client
from colorama import Fore, init  # Per l'output colorato nel terminale

# Inizializzazione di colorama per l'output colorato
init()

# Configurazione del server
HOST = "0.0.0.0"  # IP del server - ascolta su tutte le interfacce
PORT = 9999  # Porta su cui ascoltare

def handle_client(conn, addr):
    """
    Gestisce le connessioni dei singoli client
    conn: connessione socket del client
    addr: indirizzo del client (IP, porta)
    """
    print(f"{Fore.GREEN}[+] Connesso a {addr}")
    while True:
        try:
            # Ottieni il comando dall'input dell'utente
            command = input(f"{Fore.GREEN}---> ")
            if not command.strip():
                break
            
            # Invia il comando al client
            conn.send(command.encode())
            
            # Ricevi e mostra la risposta dal client
            response = conn.recv(4096).decode()
            print(f"{Fore.CYAN}{response}")
        except:
            # Se la connessione fallisce, chiudila
            print(f"{Fore.RED}[-] Client disconnesso: {addr}")
            break
    conn.close()

def main():
    # Crea il socket del server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Collega il server all'indirizzo e alla porta
    server.bind((HOST, PORT))
    
    # Inizia ad ascoltare le connessioni
    server.listen(5)  # Permette fino a 5 connessioni in coda
    print(f"{Fore.GREEN}[*] Server in ascolto su tutte le interfacce:{PORT}")

    # Loop principale del server
    while True:
        # Accetta una nuova connessione client
        client_socket, client_address = server.accept()
        
        # Crea un nuovo thread per ogni client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.daemon = True  # Il thread si chiuderà quando il programma principale termina
        client_thread.start()

# Avvia il server quando lo script viene eseguito
if __name__ == "__main__":
    main()
