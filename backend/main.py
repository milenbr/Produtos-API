from fastapi import FastAPI, HTTPException
from database import collection
from models import Produto
from utils import gerar_novo_id

app = FastAPI()

@app.post("/produtos")
def adicionar_produto(produto: Produto):
    if collection.find_one({"nome": produto.nome}):
        raise HTTPException(status_code=400, detail="Produto já cadastrado")

    if collection.count_documents({}) >= 500:
        raise HTTPException(status_code=400, detail="Limite de 500 produtos atingido")

    novo_id = gerar_novo_id()
    if not novo_id:
        raise HTTPException(status_code=400, detail="Não foi possível gerar ID")

    produto_dict = produto.dict()
    produto_dict["id"] = novo_id
    collection.insert_one(produto_dict)
    return {"mensagem": "Produto adicionado com sucesso", "id": novo_id}

@app.get("/produtos")
def listar_produtos(ordenar_por: str = "id", busca: str = None):
    query = {}
    if busca:
        query["nome"] = {"$regex": busca, "$options": "i"}

    produtos = list(collection.find(query, {"_id": 0}).sort(ordenar_por))
    return produtos

@app.put("/produtos/{id}")
def atualizar_produto(id: int, produto: Produto):
    if not collection.find_one({"id": id}):
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if collection.find_one({"nome": produto.nome, "id": {"$ne": id}}):
        raise HTTPException(status_code=400, detail="Outro produto já tem esse nome")

    collection.update_one({"id": id}, {"$set": produto.dict()})
    return {"mensagem": "Produto atualizado com sucesso"}

@app.delete("/produtos/{id}")
def deletar_produto(id: int):
    resultado = collection.delete_one({"id": id})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"mensagem": "Produto deletado com sucesso"}
