# 📦 API de Cadastro de Produtos

Este projeto é uma API completa com frontend para cadastro e gerenciamento de produtos. Usa **FastAPI**, **MongoDB** e **Streamlit**.

---

## ⚙️ Tecnologias Utilizadas

- **FastAPI** – para construção da API
- **MongoDB** – banco de dados NoSQL
- **Streamlit** – interface gráfica para o usuário
- **Pydantic** – validação de dados
- **Requests / Pandas** – no frontend

---

## 📁 Estrutura de Pastas

```
produto_api/
├── backend/
│   ├── main.py          # Código principal da API
│   ├── database.py      # Conexão com MongoDB
│   ├── models.py        # Modelos de dados
│   └── utils.py         # Funções auxiliares
│
├── frontend/
│   └── frontend.py      # Interface visual (Streamlit)
│
├── requirements.txt     # Dependências
└── README.md            # Instruções de uso
```

---

## 🚀 Como Rodar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/produto_api.git
cd produto_api
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Inicie o servidor FastAPI

```bash
uvicorn backend.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

Documentação automática: `http://localhost:8000/docs`

### 4. Inicie o frontend Streamlit

```bash
streamlit run frontend/frontend.py
```

---

## 🧪 Teste com API (Exemplo)

```bash
curl http://localhost:8000/produtos
```

---

## ✅ Funcionalidades

- Cadastro, leitura, atualização e exclusão de produtos (CRUD)
- Limite de 500 produtos
- IDs recicláveis
- Busca por nome
- Ordenação por campo
- Prevenção de duplicatas
- Campos obrigatórios
- Confirmações visuais de exclusão e atualização

---

## 📌 Observação

Certifique-se de que o MongoDB esteja em execução localmente (`localhost:27017`). Pode ser usado Atlas (MongoDB Cloud) com ajustes no `database.py`.

---
