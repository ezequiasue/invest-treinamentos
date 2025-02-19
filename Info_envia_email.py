
Este código **envia e-mails personalizados** para uma lista de destinatários usando o **Gmail e SMTP**. Ele carrega os destinatários de um arquivo **`.env`**, personaliza a mensagem e envia o e-mail para cada um.

---

### **🔍 Explicação do Código**
#### 1️⃣ **Carrega as credenciais do Gmail e os destinatários**
- Usa **dotenv** para carregar variáveis do arquivo **`.env`**, incluindo:
  ```python
  EMAIL_USER = os.getenv("EMAIL_USER")  # E-mail do remetente
  EMAIL_PASS = os.getenv("EMAIL_PASS")  # Senha do e-mail
  ```
- Obtém a lista de destinatários da variável **`EMAIL_DESTINATARIOS`** no **`.env`**:
  ```python
  destinatarios_raw = os.getenv("EMAIL_DESTINATARIOS", "")
  destinatarios_lista = [email.strip() for email in destinatarios_raw.split(",") if email.strip()]
  ```
- Se não houver destinatários, o programa **exibe um aviso e encerra**:
  ```python
  if not destinatarios_lista:
      print("⚠ Nenhum destinatário encontrado. Verifique sua variável EMAIL_DESTINATARIOS no .env.")
      exit()
  ```

---

#### 2️⃣ **Define a função para enviar e-mails**
```python
def enviar_email(destinatario, nome, assunto, mensagem):
```
- Personaliza a mensagem com o nome do destinatário:
  ```python
  corpo_email = f"""
  Olá {nome},

  {mensagem}

  Atenciosamente,
  [Seu Nome]
  """
  ```
- **Autentica no servidor SMTP do Gmail** e envia o e-mail:
  ```python
  with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
      smtp.login(EMAIL_USER, EMAIL_PASS)
      smtp.send_message(msg)
  ```
- Exibe uma mensagem de sucesso ou erro:
  ```python
  print(f"✅ E-mail enviado para {destinatario} com sucesso!")
  except smtplib.SMTPException as e:
      print(f"❌ Erro ao enviar e-mail para {destinatario}: {e}")
  ```

---

#### 3️⃣ **Define a mensagem e envia para cada destinatário**
```python
assunto = "Bem-vindo ao Nosso Serviço!"
mensagem = "Estamos felizes por você estar conosco. Se precisar de algo, estamos à disposição."
```
- Percorre a lista de destinatários e envia os e-mails um por um:
  ```python
  for email in destinatarios_lista:
      enviar_email(email, "Cliente", assunto, mensagem)
  ```

---

### **⚙ Como configurar o `.env`?**
Crie um arquivo chamado **`.env`** no mesmo diretório e adicione:
```
EMAIL_USER=seuemail@gmail.com
EMAIL_PASS=suasenha
EMAIL_DESTINATARIOS=email1@gmail.com,email2@gmail.com,email3@gmail.com
```
🔴 **Importante:** Se o Gmail bloquear o acesso, gere uma **senha de aplicativo** em [Configurações do Google](https://myaccount.google.com/security).

---

### **📌 Resumo**
✅ **Envia e-mails personalizados** via **Gmail SMTP**  
✅ **Carrega lista de destinatários do `.env`**  
✅ **Personaliza a mensagem para cada destinatário**  
✅ **Garante segurança ao usar credenciais ocultas**  

