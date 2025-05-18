from database import collection

def gerar_novo_id():
    produtos = list(collection.find({}, {"_id": 0, "id": 1}))
    usados = {produto["id"] for produto in produtos}
    
    for i in range(1, 501):
        if i not in usados:
            return i
    return None  
