import subprocess
import sys
import os
import configparser
import time
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

# Função para obter o diretório do executável
def get_exe_dir():
    if getattr(sys, 'frozen', False):  # Rodando como .exe (PyInstaller)
        return os.path.dirname(os.path.realpath(sys.executable))
    else:  # Rodando como .py
        return os.path.dirname(os.path.abspath(__file__))

# Configurar log de depuração
log_file = os.path.join(get_exe_dir(), 'startup_mode_log.txt')
def log_message(message):
    with open(log_file, 'a') as f:
        f.write(f"{time.ctime()}: {message}\n")

# Função para obter a resolução da tela atual
def get_current_screen_resolution(window):
    app = QApplication.instance()
    screen = app.screenAt(window.pos())
    if screen:
        resolution = f"{screen.geometry().width()}x{screen.geometry().height()}"
        log_message(f"Janela está na tela com resolução: {resolution}")
        return resolution
    else:
        log_message("Nenhuma tela detectada para a posição da janela")
        return None

# Obter diretórios
script_dir = get_exe_dir()
config_path = os.path.join(script_dir, 'config.ini')
current_dir = os.getcwd()

# Logar informações de depuração
log_message(f"Diretório do executável: {script_dir}")
log_message(f"Caminho do config.ini: {config_path}")
log_message(f"Diretório de trabalho atual: {current_dir}")

# Criar aplicação PyQt5
app = QApplication(sys.argv)

# Criar janela temporária para detectar a tela
window = QWidget()
window.setWindowFlags(Qt.WindowStaysOnTopHint)
window.show()

# Obter a resolução da tela atual após exibir a janela
resolution = get_current_screen_resolution(window)
if not resolution:
    error_msg = "Erro: Não foi possível detectar a resolução da tela atual!"
    print(error_msg)
    log_message(error_msg)
    sys.exit(1)

# Carregar configurações do arquivo config.ini
config = configparser.ConfigParser()
try:
    if not config.read(config_path):
        error_msg = f"Erro: {config_path} não encontrado ou inválido!"
        print(error_msg)
        log_message(error_msg)
        sys.exit(1)
    
    # Obter aplicativos para a resolução detectada ou seção [other]
    apps = []
    section = resolution if resolution in config else 'other'
    if section in config:
        # Ordenar chaves como números e obter os aplicativos
        app_keys = sorted(config[section].keys(), key=int)
        apps = [config[section][key] for key in app_keys if config[section].get(key)]
    
    log_message(f"Aplicativos para a seção [{section}]: {apps}")

    if not apps:
        error_msg = f"Erro: Nenhuma aplicação válida encontrada para a seção [{section}]!"
        print(error_msg)
        log_message(error_msg)
        sys.exit(1)

except Exception as e:
    error_msg = f"Erro ao ler {config_path}: {str(e)}"
    print(error_msg)
    log_message(error_msg)
    sys.exit(1)

# Fechar a janela
window.close()

# Executar aplicativos
log_message(f"Iniciando aplicativos na seção [{section}]")
for app in apps:
    log_message(f"Executando app: {app}")
    subprocess.Popen(app, shell=True)  # Usa Popen para não esperar

# Encerrar o script
os._exit(0)