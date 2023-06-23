import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import re
import webbrowser
import urllib.parse


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



# Check if have emails from some people in box of gmail
def checkSpecifyEmail(remetente):
    # Configurações do servidor IMAP do Gmail
    imap_server = 'imap.gmail.com'
    imap_port = 993

    # Credenciais de login
    email = 't4igacomercial@gmail.com'
    password = 'xmqiwucnotxthrvh'

    # Conectando-se ao servidor IMAP
    imap = imaplib.IMAP4_SSL(imap_server, imap_port)

    # Efetuando login
    imap.login(email, password)

    # Selecionando a caixa de entrada (INBOX por padrão)
    imap.select()

    # Procurando por e-mails do remetente específico
    search_criteria = 'FROM ' + remetente
    status, data = imap.search(None, search_criteria)

    if status == 'OK':
        email_ids = data[0].split()  # Lista de IDs de e-mails correspondentes

        if email_ids:
            # Obtendo o ID do primeiro e-mail correspondente
            #first_email_id = email_ids[0]

            print("Emails Encontrados!")
            
            # Gerando o link do e-mail
            #email_link = f"https://mail.google.com/mail/u/0/#inbox/"

            # Abrindo o link no navegador
            #webbrowser.open(email_link)

            return True

    # Fechando a conexão com o servidor IMAP
    imap.logout()


# Checks if have unreaded emails
def checkEmailBox():
    # Configurações do servidor IMAP do Gmail
    imap_server = 'imap.gmail.com'
    imap_port = 993

    # Credenciais de login
    email = 't4igacomercial@gmail.com'
    password = 'xmqiwucnotxthrvh'

    # Conectando-se ao servidor IMAP
    imap = imaplib.IMAP4_SSL(imap_server, imap_port)

    # Efetuando login
    imap.login(email, password)

    # Selecionando a caixa de entrada primária
    imap.select('INBOX')

    # Procurando por e-mails não lidos na caixa de entrada primária
    search_criteria = '(UNSEEN)'
    status, data = imap.search(None, search_criteria)

    if status == 'OK':
        email_ids = data[0].split()  # Lista de IDs de e-mails não lidos

        if email_ids:
            print("Existem e-mails não lidos na caixa de entrada.")
        else:
            print("Não existem e-mails não lidos na caixa de entrada.")

    # Fechando a conexão com o servidor IMAP
    imap.logout()