# Keylogger_v0.1

Este é um keylogger simples desenvolvido em Python. 
Ele registra as teclas pressionadas pelo usuário salva em um arquivo de log.
Além disso, o script pode enviar automaticamente os registros capturados por e-mail a cada 24 horas.  

## 🚀 Funcionalidades  
- Captura todas as teclas digitadas pelo usuário.  
- Registra as teclas em um arquivo `system_log.txt`.  
- Roda em segundo plano sem exibir uma janela no Windows.  
- Envia os logs capturados para um e-mail especificado a cada 24 horas.  
- Exclui o arquivo de log após o envio do e-mail.  

## 🛠 Como Funciona  
1. O script inicia ocultando a janela do console no Windows.  
2. Define um arquivo de log para armazenar as teclas pressionadas.  
3. Utiliza a biblioteca `pynput` para capturar as teclas digitadas.  
4. Armazena cada tecla pressionada no log.  
5. A cada 24 horas, um processo secundário envia o conteúdo do log por e-mail.  
6. Após o envio do e-mail, o log é apagado e um novo é iniciado.

Passos para Criar o Executável 💾

Instale o PyInstaller
```sh
pip install pyinstaller
```
```sh
pyinstaller --onefile --noconsole --hidden-import=pynput keylogger.py
```
## 📌 Requisitos  
- Python 3.x instalado  
- Bibliotecas necessárias:  
  ```sh
  pip install pynput

📌 Melhorias Futuras
🔒 Adicionar um e-mail criptografado: Implementar um sistema de criptografia para proteger as informações enviadas.

🖼️ Captura de tela: Incluir um recurso para tirar screenshots periodicamente.

🎤 Gravação de áudio: Implementar um módulo para capturar áudio do microfone.

📁 Armazenamento alternativo: Permitir o envio dos logs para um servidor remoto ou salvar em um banco de dados.

⚠️ Aviso
Esse código é apenas para fins educacionais e testes de segurança ofensiva (pentest). Não use para fins ilegais.
