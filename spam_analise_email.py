import imaplib
import email
import os
import re
import joblib
import numpy as np
from dotenv import load_dotenv
from email.header import decode_header
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do Gmail
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Conectar ao Gmail via IMAP
def conectar_gmail():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")
        return mail
    except imaplib.IMAP4.error as e:
        print(f"Erro ao conectar ao Gmail: {e}")
        return None

# Função para decodificar cabeçalhos MIME corretamente
def decode_mime_header(header_value):
    if not header_value:
        return "Sem Assunto"
    
    decoded_parts = decode_header(header_value)
    decoded_string = ""
    
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            decoded_string += part.decode(encoding or "utf-8", errors="ignore")
        else:
            decoded_string += part
            
    return decoded_string.strip()

# Extrair o corpo do e-mail
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

# Extrair somente o e-mail do remetente
def extract_email(from_field):
    match = re.search(r'<(.*?)>', from_field)
    return match.group(1) if match else from_field

# Carregar modelo treinado (se existir), caso contrário, treinar
def carregar_ou_treinar_modelo():
    if os.path.exists("spam_model.pkl") and os.path.exists("vectorizer.pkl"):
        print("🔄 Carregando modelo de SPAM treinado...")
        model = joblib.load("spam_model.pkl")
        vectorizer = joblib.load("vectorizer.pkl")
    else:
        print("🛠️ Treinando modelo de SPAM...")

        # Dados de exemplo para treinamento (idealmente use um dataset real)
        emails = [
            "Você ganhou um prêmio! Clique aqui para resgatar.",
            "Parabéns! Você foi selecionado para um prêmio especial.",
            "Quer ganhar dinheiro rápido? Responda este e-mail!",
            "Promoção imperdível! Última chance de comprar com desconto.",
            "Oi João, como você está? Podemos marcar uma reunião?",
            "Segue a proposta solicitada para análise.",
            "Confirmação de pagamento realizada com sucesso.",
            "Aqui está o documento que você pediu."
        ]
        labels = [1, 1, 1, 1, 0, 0, 0, 0]  # 1 = SPAM, 0 = NÃO SPAM

        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(emails)

        model = MultinomialNB()
        model.fit(X, labels)

        # Salvar o modelo treinado
        joblib.dump(model, "spam_model.pkl")
        joblib.dump(vectorizer, "vectorizer.pkl")

    return model, vectorizer

# Classificar se o e-mail é SPAM ou não usando o modelo treinado
def verificar_spam_ml(texto_email, model, vectorizer):
    X_test = vectorizer.transform([texto_email])
    prediction = model.predict(X_test)
    return "SPAM" if prediction[0] == 1 else "NÃO SPAM"

# Processar os e-mails e verificar SPAM
def verificar_emails():
    mail = conectar_gmail()
    if not mail:
        return

    # Carregar o modelo de SPAM
    model, vectorizer = carregar_ou_treinar_modelo()

    # Buscar e-mails não lidos
    status, messages = mail.search(None, 'UNSEEN')
    mail_ids = messages[0].split()

    if not mail_ids:
        print("📭 Nenhum e-mail não lido encontrado.")
        return

    for mail_id in mail_ids:
        mail_id = mail_id.decode()
        status, msg_data = mail.fetch(mail_id, '(RFC822)')

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                sender_email = extract_email(msg["From"])
                subject = decode_mime_header(msg["Subject"])

                body = get_email_body(msg)
                if not body:
                    print(f"E-mail de {sender_email} sem corpo legível.")
                    continue

                print(f"\n📩 Novo e-mail de: {sender_email}")
                print(f"📌 Assunto: {subject}")

                # Usar Machine Learning para classificar SPAM
                classificacao = verificar_spam_ml(body, model, vectorizer)

                if classificacao == "SPAM":
                    print("🚨 Classificado como: SPAM")
                    # Mover para a pasta SPAM em vez de excluir
                    mail.store(mail_id, '+X-GM-LABELS', '\\Spam')
                else:
                    print("✅ Classificado como: NÃO SPAM")

    # Fechar a conexão
    mail.logout()

# Executar o script
verificar_emails()
