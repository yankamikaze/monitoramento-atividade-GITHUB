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

Você pode publicar esta aplicação facilmente e de forma gratuita em serviços como Render ou Railway, já que utilizamos o framework leve Flask e `gunicorn`.

### Deploy no Render
1. Crie uma conta no [Render](https://render.com/).
2. Conecte sua conta do GitHub.
3. Clique em **New** > **Web Service**.
4. Selecione este repositório.
5. Em **Build Command**, insira: `pip install -r requirements.txt`
6. Em **Start Command**, insira: `gunicorn app:app`
7. (Importante) Vá em **Environment Variables** e adicione a variável `GITHUB_TOKEN` com o seu token gerado.
8. Clique em **Create Web Service**. A aplicação será construída e ficará disponível em uma URL pública!
