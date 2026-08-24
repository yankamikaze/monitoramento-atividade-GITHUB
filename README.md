# GitHub PR Heatmap

Uma aplicação web simples em Python (Flask) que gera um heatmap (gráfico de contribuições) semelhante ao do GitHub, focado exclusivamente nas Pull Requests de um usuário específico.

## Funcionalidades
- Heatmap de PRs por usuário e ano.
- Tema Dark Mode.
- Tooltips detalhados ao passar o mouse sobre os dias, mostrando o estado e título das PRs.

## Requisitos
- Python 3.8+

## Como Rodar Localmente

1. **Clone o repositório:**
   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd "Monitoramento Deploys Git Hub"
   ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure a Variável de Ambiente (Token do GitHub):**
   - O GitHub limita requisições sem autenticação (10 requisições por minuto na Search API). Para uso contínuo, é altamente recomendado criar um [Personal Access Token (PAT) no GitHub](https://github.com/settings/tokens) (apenas permissão de `public_repo` ou nenhuma permissão se for só consultar dados públicos).
   - Copie o arquivo `.env.example` para `.env` e insira seu token:
     ```bash
     cp .env.example .env
     ```
   - No `.env`: `GITHUB_TOKEN=ghp_seu_token_aqui`

5. **Inicie o Servidor:**
   ```bash
   python app.py
   # ou
   flask run
   ```

6. Acesse a aplicação em `http://127.0.0.1:5000`

## Como Fazer o Deploy (Nuvem)

### ▲ Deploy no Vercel (Recomendado)
O projeto já inclui o arquivo `vercel.json` configurado, portanto o deploy é simples:

1. Crie uma conta no [Vercel](https://vercel.com/) usando sua conta GitHub.
2. Clique em **Add New → Project**.
3. Importe o repositório **`monitoramento-atividade-GITHUB`**.
4. (Importante) Na seção **Environment Variables**, adicione:
   - `GITHUB_TOKEN` = seu [Personal Access Token do GitHub](https://github.com/settings/tokens)
5. Clique em **Deploy**. Em poucos segundos a aplicação estará no ar!

> **Nota:** O Vercel executa a aplicação Flask como uma **serverless function** via `@vercel/python`. O `gunicorn` **não é necessário** no Vercel, apenas para o Render.

---

### Deploy no Render (Alternativa)
1. Crie uma conta no [Render](https://render.com/).
2. Conecte sua conta do GitHub.
3. Clique em **New** > **Web Service**.
4. Selecione este repositório.
5. Em **Build Command**, insira: `pip install -r requirements.txt`
6. Em **Start Command**, insira: `gunicorn app:app`
7. (Importante) Vá em **Environment Variables** e adicione a variável `GITHUB_TOKEN`.
8. Clique em **Create Web Service**.
