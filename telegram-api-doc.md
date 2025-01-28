### **URLs Básicas da API do Telegram**
1. **Obter informações sobre o bot**
   - Método: `getMe`
   - Descrição: Retorna informações básicas sobre o bot.
   - URL:
     ```
     https://api.telegram.org/bot<SEU_TOKEN>/getMe
     ```

2. **Receber atualizações (mensagens, comandos, etc.)**
   - Método: `getUpdates`
   - Descrição: Retorna uma lista de atualizações (mensagens, comandos, etc.) recebidas pelo bot.
   - URL:
     ```
     https://api.telegram.org/bot<SEU_TOKEN>/getUpdates
     ```

3. **Enviar uma mensagem**
   - Método: `sendMessage`
   - Descrição: Envia uma mensagem de texto para um chat específico.
   - URL:
     ```
     https://api.telegram.org/bot<SEU_TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=<TEXTO>
     ```

4. **Enviar uma foto**
   - Método: `sendPhoto`
   - Descrição: Envia uma foto para um chat específico.
   - URL:
     ```
     https://api.telegram.org/bot<SEU_TOKEN>/sendPhoto?chat_id=<CHAT_ID>&photo=<URL_DA_FOTO>
     ```

5. **Enviar um documento**
   - Método: `sendDocument`
   - Descrição: Envia um documento (arquivo) para um chat específico.
   - URL:
     ```
     https://api.telegram.org/bot<SEU_TOKEN>/sendDocument?chat_id=<CHAT_ID>&document=<URL_DO_DOCUMENTO>
     ```

6. **Enviar uma localização**
   - Método: `sendLocation`
   - Descrição: Envia uma localização (latitude e longitude) para um chat específico.
   - URL:
     ```
     https://api.telegram.org/bot<SEU_TOKEN>/sendLocation?chat_id=<CHAT_ID>&latitude=<LATITUDE>&longitude=<LONGITUDE>
     ```

7. **Obter informações sobre um chat**
   - Método: `getChat`
   - Descrição: Retorna informações sobre um chat (usuário, grupo, canal, etc.).
   - URL:
     ```
     https://api.telegram.org/bot<SEU_TOKEN>/getChat?chat_id=<CHAT_ID>
     ```

8. **Obter a lista de administradores de um grupo**
   - Método: `getChatAdministrators`
   - Descrição: Retorna a lista de administradores de um grupo ou supergrupo.
   - URL:
     ```
     https://api.telegram.org/bot<SEU_TOKEN>/getChatAdministrators?chat_id=<CHAT_ID>
     ```

9. **Obter o número total de membros de um chat**
   - Método: `getChatMembersCount`
   - Descrição: Retorna o número total de membros em um chat.
   - URL:
     ```
     https://api.telegram.org/bot<SEU_TOKEN>/getChatMembersCount?chat_id=<CHAT_ID>
     ```

10. **Obter informações sobre um membro específico de um chat**
    - Método: `getChatMember`
    - Descrição: Retorna informações sobre um membro específico de um chat.
    - URL:
      ```
      https://api.telegram.org/bot<SEU_TOKEN>/getChatMember?chat_id=<CHAT_ID>&user_id=<USER_ID>
      ```

---

### **URLs para Gerenciamento de Webhooks**
11. **Definir um webhook**
    - Método: `setWebhook`
    - Descrição: Define uma URL para receber atualizações em tempo real.
    - URL:
      ```
      https://api.telegram.org/bot<SEU_TOKEN>/setWebhook?url=<URL_DO_WEBHOOK>
      ```

12. **Remover um webhook**
    - Método: `deleteWebhook`
    - Descrição: Remove o webhook configurado.
    - URL:
      ```
      https://api.telegram.org/bot<SEU_TOKEN>/deleteWebhook
      ```

13. **Obter informações sobre o webhook atual**
    - Método: `getWebhookInfo`
    - Descrição: Retorna informações sobre o webhook configurado.
    - URL:
      ```
      https://api.telegram.org/bot<SEU_TOKEN>/getWebhookInfo
      ```

---

### **URLs para Gerenciamento de Comandos**
14. **Definir comandos do bot**
    - Método: `setMyCommands`
    - Descrição: Define uma lista de comandos que o bot suporta.
    - URL:
      ```
      https://api.telegram.org/bot<SEU_TOKEN>/setMyCommands?commands=[{"command":"start","description":"Iniciar o bot"}]
      ```

15. **Obter comandos do bot**
    - Método: `getMyCommands`
    - Descrição: Retorna a lista de comandos configurados para o bot.
    - URL:
      ```
      https://api.telegram.org/bot<SEU_TOKEN>/getMyCommands
      ```

---

### **URLs para Gerenciamento de Arquivos**
16. **Obter informações sobre um arquivo**
    - Método: `getFile`
    - Descrição: Retorna informações sobre um arquivo enviado ao bot.
    - URL:
      ```
      https://api.telegram.org/bot<SEU_TOKEN>/getFile?file_id=<FILE_ID>
      ```

17. **Baixar um arquivo**
    - Método: `getFile` + URL de download
    - Descrição: Baixa um arquivo enviado ao bot.
    - URL de download:
      ```
      https://api.telegram.org/file/bot<SEU_TOKEN>/<CAMINHO_DO_ARQUIVO>
      ```

---

### **Exemplos Práticos**
- **Exemplo 1: Receber atualizações**
  ```
  https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/getUpdates
  ```

- **Exemplo 2: Enviar uma mensagem**
  ```
  https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/sendMessage?chat_id=123456789&text=Olá,%20mundo!
  ```

- **Exemplo 3: Definir um webhook**
  ```
  https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/setWebhook?url=https://seusite.com/webhook
  ```

---

### **Observações**
- Substitua `<SEU_TOKEN>` pelo token do seu bot.
- Substitua `<CHAT_ID>`, `<USER_ID>`, `<FILE_ID>`, etc., pelos valores apropriados.
- Para URLs com parâmetros complexos (como JSON), você pode usar ferramentas como `Postman` ou `curl` para enviar requisições POST.

Essa lista cobre as operações mais comuns da API do Telegram e pode ser usada como referência para documentação ou testes.