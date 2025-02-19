import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do Gmail
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Obter lista de destinatários do .env
destinatarios_raw = os.getenv("EMAIL_DESTINATARIOS", "")  # Se não existir, retorna uma string vazia
destinatarios_lista = [email.strip() for email in destinatarios_raw.split(",") if email.strip()]  # Limpa espaços extras

# Verificar se há destinatários válidos
if not destinatarios_lista:
    print("⚠ Nenhum destinatário encontrado. Verifique sua variável EMAIL_DESTINATARIOS no .env.")
    exit()

# Função para enviar e-mails personalizados
def enviar_email(destinatario, nome, assunto, mensagem):
    msg = EmailMessage()
    msg["From"] = EMAIL_USER
    msg["To"] = destinatario
    msg["Subject"] = assunto

    # Personalizar a mensagem
    corpo_email = f"""
    Olá {nome},

    {mensagem}

    Atenciosamente,
    [Seu Nome]
    """

    msg.set_content(corpo_email)

    # Conectar ao servidor SMTP do Gmail
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
        print(f"✅ E-mail enviado para {destinatario} com sucesso!")
    except smtplib.SMTPException as e:
        print(f"❌ Erro ao enviar e-mail para {destinatario}: {e}")

# Assunto e mensagem do e-mail
assunto = "Bem-vindo ao Nosso Serviço!"
mensagem = "Estamos felizes por você estar conosco. Se precisar de algo, estamos à disposição."

# Enviar e-mail para cada destinatário
for email in destinatarios_lista:
    enviar_email(email, "Cliente", assunto, mensagem)
