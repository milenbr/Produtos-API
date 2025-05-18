import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Cadastro de Produtos", layout="centered")

st.title("📦 Produtos")

menu = st.sidebar.selectbox("Menu", ["Cadastrar", "Listar", "Atualizar", "Deletar"])

def exibir_resultado(response):
    if response.status_code in (200, 201):
        st.success(response.json().get("mensagem", "Operação realizada com sucesso!"))
    else:
        erro = response.json().get("detail", "Erro ao processar a solicitação.")
        st.error(erro)

if menu == "Cadastrar":
    st.header("➕ Cadastrar Produto")

    nome = st.text_input("Nome")
    categoria = st.text_input("Categoria")
    preco = st.number_input("Preço", min_value=0.01, format="%.2f")
    quantidade = st.number_input("Quantidade", min_value=0)

    if st.button("Cadastrar"):
        if nome.strip() == "" or categoria.strip() == "":
            st.warning("Todos os campos devem ser preenchidos.")
        else:
            produto = {
                "nome": nome.strip(),
                "categoria": categoria.strip(),
                "preco": preco,
                "quantidade": quantidade
            }
            response = requests.post(f"{API_URL}/produtos", json=produto)
            exibir_resultado(response)


elif menu == "Listar":
    st.header("📋 Lista de Produtos")

    busca = st.text_input("🔍 Buscar por nome")
    ordenar_por = st.selectbox("Ordenar por", ["id", "nome", "categoria", "preco", "quantidade"])

    params = {"ordenar_por": ordenar_por}
    if busca:
        params["busca"] = busca

    response = requests.get(f"{API_URL}/produtos", params=params)

    if response.status_code == 200:
        produtos = response.json()
        if produtos:
            st.write(f"Total de produtos encontrados: {len(produtos)}")

            
            for produto in produtos:
                produto["preco"] = f"R$ {produto['preco']:.2f}".replace(".", ",")

         
            df = pd.DataFrame(produtos)
            df.index = df.index + 1  # índice começa do 1

           
            df.rename(columns={
                "id": "ID",
                "nome": "Nome",
                "categoria": "Categoria",
                "preco": "Preço",
                "quantidade": "Quantidade"
            }, inplace=True)

            st.dataframe(df)
        else:
            st.info("Nenhum produto encontrado.")
    else:
        exibir_resultado(response)



elif menu == "Atualizar":
    st.header("✏️ Atualizar Produto")

    response = requests.get(f"{API_URL}/produtos")
    produtos = response.json()

    ids = [produto["id"] for produto in produtos]
    id_prod = st.selectbox("Selecione o ID do produto", ids)

    produto_info = next((p for p in produtos if p["id"] == id_prod), None)

    if produto_info:
        nome = st.text_input("Nome", value=produto_info["nome"])
        categoria = st.text_input("Categoria", value=produto_info["categoria"])
        preco = st.number_input("Preço", min_value=0.01, format="%.2f", value=float(produto_info["preco"]))
        quantidade = st.number_input("Quantidade", min_value=0, value=int(produto_info["quantidade"]))

        if st.button("Atualizar"):
            if nome.strip() == "" or categoria.strip() == "":
                st.warning("Todos os campos devem ser preenchidos.")
            else:
                atualizado = {
                    "nome": nome.strip(),
                    "categoria": categoria.strip(),
                    "preco": preco,
                    "quantidade": quantidade
                }
                response = requests.put(f"{API_URL}/produtos/{id_prod}", json=atualizado)
                exibir_resultado(response)


elif menu == "Deletar":
    st.header("🗑️ Deletar Produto")

    response = requests.get(f"{API_URL}/produtos")
    produtos = response.json()

    if not produtos:
        st.info("Nenhum produto disponível para deletar.")
    else:
        ids = [produto["id"] for produto in produtos]
        id_prod = st.selectbox("Selecione o ID do produto para deletar", ids)

        produto_info = next((p for p in produtos if p["id"] == id_prod), None)

        if produto_info:
            st.markdown("### 📌 Detalhes do Produto Selecionado:")
            st.write(f"**Nome:** {produto_info['nome']}")
            st.write(f"**Categoria:** {produto_info['categoria']}")
            st.write(f"**Preço:** R$ {produto_info['preco']:.2f}".replace(".", ","))
            st.write(f"**Quantidade:** {produto_info['quantidade']}")

            if st.button("✅ Confirmar Deleção"):
                response = requests.delete(f"{API_URL}/produtos/{id_prod}")
                exibir_resultado(response)
