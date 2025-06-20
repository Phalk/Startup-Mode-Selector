import subprocess
import sys
import os
import configparser
import time
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

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

# Obter diretórios
script_dir = get_exe_dir()
config_path = os.path.join(script_dir, 'config.ini')
current_dir = os.getcwd()

# Logar informações de depuração
log_message(f"Diretório do executável: {script_dir}")
log_message(f"Caminho do config.ini: {config_path}")
log_message(f"Diretório de trabalho atual: {current_dir}")

# Carregar configurações do arquivo config.ini
config = configparser.ConfigParser()
try:
    if not config.read(config_path):
        error_msg = f"Erro: {config_path} não encontrado ou inválido!"
        print(error_msg)
        log_message(error_msg)
        input("Pressione Enter para fechar...")
        sys.exit(1)
    
    # Obter aplicativos para Console Mode e Desktop Mode
    console_apps = []
    desktop_apps = []
    if 'consoleMode' in config:
        console_keys = sorted(config['consoleMode'].keys(), key=int)  # Ordenar chaves como números
        console_apps = [config['consoleMode'][key] for key in console_keys if config['consoleMode'].get(key)]
    if 'desktopMode' in config:
        desktop_keys = sorted(config['desktopMode'].keys(), key=int)
        desktop_apps = [config['desktopMode'][key] for key in desktop_keys if config['desktopMode'].get(key)]

    log_message(f"Aplicativos Console Mode: {console_apps}")
    log_message(f"Aplicativos Desktop Mode: {desktop_apps}")

    if not console_apps and not desktop_apps:
        error_msg = "Erro: Nenhuma aplicação válida encontrada em [consoleMode] ou [desktopMode]!"
        print(error_msg)
        log_message(error_msg)
        input("Pressione Enter para fechar...")
        sys.exit(1)

except Exception as e:
    error_msg = f"Erro ao ler {config_path}: {str(e)}"
    print(error_msg)
    log_message(error_msg)
    input("Pressione Enter para fechar...")
    sys.exit(1)

# Criar aplicação PyQt5
app = QApplication(sys.argv)

# Criar janela sem bordas com fundo transparente
window = QWidget()
window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
window.setAttribute(Qt.WA_TranslucentBackground)
window.setStyleSheet("background-color: rgba(0, 0, 0, 200); color: white;")

# Layout e labels
layout = QVBoxLayout()
label_message1 = QLabel("Inicializando console mode em 3 segundos...")
label_message2 = QLabel("Pressione Enter para inicializar no modo desktop")
label_countdown = QLabel("3...")
label_message1.setFont(QFont('Arial', 16))
label_message2.setFont(QFont('Arial', 14))
label_countdown.setFont(QFont('Arial', 16))
label_message1.setStyleSheet("color: white;")
label_message2.setStyleSheet("color: white;")
label_countdown.setStyleSheet("color: white;")
layout.addWidget(label_message1, alignment=Qt.AlignCenter)
layout.addWidget(label_message2, alignment=Qt.AlignCenter)
layout.addWidget(label_countdown, alignment=Qt.AlignCenter)
window.setLayout(layout)

# Centralizar a janela
screen = app.primaryScreen().geometry()
window.resize(600, 200)
window.move((screen.width() - window.width()) // 2, (screen.height() - window.height()) // 2)

# Mostrar janela
window.show()

# Countdown e lógica de Enter
countdown = 3
desktop_mode = False

def update_countdown():
    global countdown, desktop_mode
    if countdown > 0:
        label_countdown.setText(f"{countdown}...")
        countdown -= 1
    else:
        if not desktop_mode:
            log_message("Iniciando Console Mode")
            window.close()
            subprocess.run(['taskkill', '/F', '/IM', 'explorer.exe'], shell=True)
            for app in console_apps:
                log_message(f"Executando Console Mode app: {app}")
                subprocess.Popen(app, shell=True)  # Usa Popen para não esperar
            os._exit(0)  # Encerra o processo completamente

# Configurar timer para atualizar o countdown
timer = QTimer()
timer.timeout.connect(update_countdown)
timer.start(1000)  # Atualiza a cada 1 segundo

# Detectar tecla Enter
def keyPressEvent(event):
    global desktop_mode
    if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
        desktop_mode = True
        label_countdown.setText("Executando Desktop Mode...")
        log_message("Iniciando Desktop Mode")
        timer.stop()
        time.sleep(0.1)  # Pequeno atraso para animação
        window.close()
        for app in desktop_apps:
            log_message(f"Executando Desktop Mode app: {app}")
            subprocess.Popen(app, shell=True)  # Usa Popen para não esperar
        os._exit(0)  # Encerra o processo completamente

window.keyPressEvent = keyPressEvent

# Iniciar loop da aplicação
sys.exit(app.exec_())