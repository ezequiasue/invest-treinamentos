Este código tem duas funções principais:

### **📩 O que ele faz?**
1. **Acessa sua conta do Gmail** usando o protocolo **IMAP**.
2. **Busca apenas os e-mails não lidos** (`UNSEEN`) na caixa de entrada.
3. **Extrai informações de cada e-mail**, incluindo:
   - 📧 **Remetente**
   - 📝 **Assunto**
   - 📜 **Corpo da mensagem**
4. **Analisa o sentimento do e-mail** usando a biblioteca **TextBlob**, categorizando como:
   - **POSITIVO 😊** (mensagem amigável, elogio)
   - **NEGATIVO 😡** (reclamação, insatisfação)
   - **NEUTRO 😐** (mensagem sem emoções claras)
5. **Exibe os resultados no terminal**.

---

### **🔍 Explicação do Código**
#### 1️⃣ **Autenticação e conexão com o Gmail**
- O código carrega as credenciais do e-mail a partir de um arquivo **.env**:
  ```python
  EMAIL_USER = os.getenv("EMAIL_USER")
  EMAIL_PASS = os.getenv("EMAIL_PASS")
  ```
- Conecta ao **servidor IMAP do Gmail**:
  ```python
  mail = imaplib.IMAP4_SSL("imap.gmail.com")
  mail.login(EMAIL_USER, EMAIL_PASS)
  ```

#### 2️⃣ **Busca apenas os e-mails não lidos**
- Seleciona a caixa de entrada:
  ```python
  mail.select("inbox")
  ```
- Procura mensagens **não lidas**:
  ```python
  status, messages = mail.search(None, 'UNSEEN')
  ```

#### 3️⃣ **Processamento de cada e-mail**
- Obtém a lista de e-mails encontrados:
  ```python
  mail_ids = messages[0].split()
  ```
- Para cada e-mail:
  - **Extrai o remetente**:
    ```python
    sender_email = extract_email(msg["From"])
    ```
  - **Extrai o assunto**:
    ```python
    subject = msg["Subject"] or "Sem Assunto"
    ```
  - **Extrai o corpo do e-mail** (mensagem principal):
    ```python
    body = get_email_body(msg)
    ```

#### 4️⃣ **Análise de Sentimento**
- Usa `TextBlob` para classificar o e-mail como **positivo, negativo ou neutro**:
  ```python
  sentimento = analyze_sentiment(body)
  ```
- Baseado na **polaridade** do texto:
  - **Positivo** → `TextBlob` retorna um valor maior que `0`
  - **Negativo** → Retorna um valor menor que `0`
  - **Neutro** → Retorna `0`

#### 5️⃣ **Exibição dos resultados**
Cada e-mail processado será exibido assim:
```
📩 Novo e-mail de: cliente@email.com
📝 Assunto: Reclamação sobre o serviço
📜 Mensagem: Estou muito insatisfeito com o atendimento, não responderam meu pedido.
🧐 Sentimento detectado: NEGATIVO 😡
```

---

### **❌ Possíveis Erros e Soluções**
| Erro                        | Causa Possível                                      | Solução                                          |
|-----------------------------|------------------------------------------------------|-------------------------------------------------|
| `Erro IMAP: LOGIN failed`   | Credenciais erradas ou acesso IMAP bloqueado       | Verificar `.env` e liberar **Acesso IMAP** no Gmail |
| `Nenhum e-mail encontrado`  | Não há e-mails **não lidos** na caixa de entrada   | Enviar um e-mail para si mesmo e testar       |
| `E-mail sem corpo legível`  | Alguns e-mails podem conter **apenas anexos**      | Testar diferentes e-mails com texto simples   |

---

### **📌 Resumo**
✅ **Acessa sua conta do Gmail**  
✅ **Busca apenas e-mails não lidos**  
✅ **Extrai remetente, assunto e mensagem**  
✅ **Analisa o sentimento do e-mail (positivo, negativo ou neutro)**  
✅ **Exibe os resultados no terminal**  

🚀 **Ótimo para criar um sistema automatizado de análise de e-mails!**  

Se precisar de melhorias ou adaptações, me avise! 😊
