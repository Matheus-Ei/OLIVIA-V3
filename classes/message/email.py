import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Send a Email
def sendEmail(destinatario, Assunto, message):
    # Configurações do servidor SMTP do Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    username = 't4igacomercial@gmail.com'
    password = 'xmqiwucnotxthrvh'
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