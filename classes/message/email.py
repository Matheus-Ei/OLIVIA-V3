import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Enviar Email(AINDA NÃO FUNCIONANDO)
def enviar_email(destinatario, Assunto, message):
    # Configurações do servidor SMTP do Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    username = 'eickoffmatheus@gmail.com'
    password = '123@Matheuse'
    # Crie uma instância da mensagem
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = destinatario
    msg['Subject'] = Assunto
    # Corpo do e-mail
    msg.attach(MIMEText(message, 'plain'))
    # Conecte-se ao servidor SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username, password)
    # Envie o e-mail
    server.send_message(msg)
    server.quit()