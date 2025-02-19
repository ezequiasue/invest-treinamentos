import imaplib
import email
import os
import re
from dotenv import load_dotenv
from textblob import TextBlob  # Biblioteca para análise de sentimentos

# Carregar variáveis de ambiente
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def get_email_body(msg):
    body = None
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                body = part.get_payload(decode=True).decode(errors="ignore")
                break
            elif content_type == "text/html" and not body:
                body = part.get_payload(decode=True).decode(errors="ignore")
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")

    return body.strip() if body else None

def extract_email(from_field):
    match = re.search(r'<(.*?)>', from_field)
    return match.group(1) if match else from_field

def analyze_sentiment(text):
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity

    if sentiment_score > 0:
        return "POSITIVO 😊"
    elif sentiment_score < 0:
        return "NEGATIVO 😡"
    else:
        return "NEUTRO 😐"

try:
    print("🔄 Tentando conectar ao Gmail...")
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL_USER, EMAIL_PASS)
    print("✅ Login bem-sucedido!")

    mail.select("inbox")
    
    # 🔴 BUSCANDO APENAS E-MAILS NÃO LIDOS (UNSEEN)
    status, messages = mail.search(None, 'UNSEEN')

    mail_ids = messages[0].split()
    print(f"📩 E-mails NÃO LIDOS encontrados: {len(mail_ids)}")

    if not mail_ids:
        print("⚠️ Nenhum e-mail não lido encontrado. Verifique sua caixa de entrada.")
    
    for mail_id in mail_ids:
        mail_id = mail_id.decode()
        status, msg_data = mail.fetch(mail_id, '(RFC822)')

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                sender_email = extract_email(msg["From"])
                subject = msg["Subject"] or "Sem Assunto"

                body = get_email_body(msg)

                if not body:
                    print(f"⚠️ E-mail de {sender_email} sem corpo legível.")
                    continue

                print(f"\n📩 Novo e-mail de: {sender_email}")
                print(f"📝 Assunto: {subject}")
                print(f"📜 Mensagem: {body[:300]}")  # Exibir apenas os primeiros 300 caracteres
                print(f"🧐 Sentimento detectado: {analyze_sentiment(body)}")

except imaplib.IMAP4.error as e:
    print(f"❌ Erro IMAP: {e}")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
finally:
    if 'mail' in locals():
        mail.logout()
