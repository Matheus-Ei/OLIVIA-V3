# Imports
from win10toast import ToastNotifier
import time



# Exibir Notificações
def exibir_notificacao(titulo, mensagem):
    toaster = ToastNotifier()
    toaster.show_toast(titulo, mensagem, duration=2, threaded=True)





# Monitorar Notificações(EM FASE DE TESTES)
def monitorar_notificacoes():
    def imprimir_notificacao(titulo, mensagem):
        print("Notificação Recebida:")
        print("Título:", titulo)
        print("Mensagem:", mensagem)
        print("----------------------")

    while True:
        # Código para verificar as notificações
        # Para Windows:
        toaster = ToastNotifier()
        toaster.show_toast("Monitor de Notificações", "Aguardando notificações...")
        time.sleep(5)

        # Para macOS e Linux:
        # notification = Notification(title="Monitor de Notificações", description="Aguardando notificações...", duration=5)
        # notification.send()

        # Exemplo de notificação recebida (substitua com o código de acesso às notificações do seu sistema operacional):
        titulo = "Notificação do WhatsApp"
        mensagem = "Você tem uma nova mensagem."

        # Chame a função para imprimir a notificação recebida
        imprimir_notificacao(titulo, mensagem)