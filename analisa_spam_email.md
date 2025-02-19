### **📧 O que este código faz?**
Este código **acessa sua conta do Gmail via IMAP, verifica os e-mails não lidos e classifica se são SPAM ou NÃO SPAM** usando um **modelo de Machine Learning (Naive Bayes)**.

---

### **🔍 Explicação do Código**
#### 1️⃣ **Autenticação no Gmail**
- Carrega as credenciais do e-mail do arquivo **`.env`**:
  ```python
  EMAIL_USER = os.getenv("EMAIL_USER")
  EMAIL_PASS = os.getenv("EMAIL_PASS")
  ```
- Conecta ao **servidor IMAP do Gmail** para acessar a caixa de entrada:
  ```python
  mail = imaplib.IMAP4_SSL("imap.gmail.com")
  mail.login(EMAIL_USER, EMAIL_PASS)
  ```

---

#### 2️⃣ **Busca apenas os e-mails não lidos**
- Seleciona a caixa de entrada:
  ```python
  mail.select("inbox")
  ```
- Procura mensagens **não lidas**:
  ```python
  status, messages = mail.search(None, 'UNSEEN')
  ```

---

#### 3️⃣ **Decodifica cabeçalhos de e-mails**
Como os assuntos de e-mails podem conter caracteres especiais, o código decodifica corretamente o **assunto do e-mail**:
```python
def decode_mime_header(header_value):
    decoded_parts = decode_header(header_value)
```

---

#### 4️⃣ **Extrai o conteúdo do e-mail**
- Obtém o **corpo da mensagem** (texto simples ou HTML):
  ```python
  def get_email_body(msg):
      if msg.is_multipart():
          for part in msg.walk():
              if part.get_content_type() == "text/plain":
                  body = part.get_payload(decode=True).decode(errors="ignore")
  ```

---

#### 5️⃣ **Treina ou carrega um modelo de Machine Learning (Naive Bayes)**
- Se o modelo **já existir**, ele carrega:
  ```python
  if os.path.exists("spam_model.pkl"):
      model = joblib.load("spam_model.pkl")
  ```
- Se não existir, ele **treina um modelo de SPAM básico** com **exemplos pré-definidos**:
  ```python
  emails = [
      "Você ganhou um prêmio! Clique aqui para resgatar.",
      "Promoção imperdível! Última chance de comprar com desconto.",
      "Oi João, como você está? Podemos marcar uma reunião?",
      "Confirmação de pagamento realizada com sucesso."
  ]
  labels = [1, 1, 0, 0]  # 1 = SPAM, 0 = NÃO SPAM
  ```
- Treina o **Naive Bayes** com `CountVectorizer()`:
  ```python
  vectorizer = CountVectorizer()
  X = vectorizer.fit_transform(emails)
  model = MultinomialNB()
  model.fit(X, labels)
  ```
- Salva o modelo:
  ```python
  joblib.dump(model, "spam_model.pkl")
  joblib.dump(vectorizer, "vectorizer.pkl")
  ```

---

#### 6️⃣ **Classifica o e-mail como SPAM ou NÃO SPAM**
- Converte o texto do e-mail em um formato que o modelo entende:
  ```python
  X_test = vectorizer.transform([texto_email])
  prediction = model.predict(X_test)
  ```
- Se a predição for `1`, classifica como **SPAM**, senão **NÃO SPAM**.

---

#### 7️⃣ **Marca o e-mail como SPAM no Gmail**
Se o e-mail for identificado como SPAM, o código **move para a pasta SPAM do Gmail**:
```python
mail.store(mail_id, '+X-GM-LABELS', '\\Spam')
```

---

### **📌 Resumo**
✅ **Acessa sua conta do Gmail**  
✅ **Lê apenas e-mails não lidos**  
✅ **Treina um modelo de Machine Learning para detectar SPAM**  
✅ **Classifica os e-mails automaticamente**  
✅ **Move SPAM para a pasta correta no Gmail**  

🔹 **Se quiser um modelo mais preciso, pode treinar com mais dados reais!** 🚀  
Se precisar de ajustes, me avise! 😊
