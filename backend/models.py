from pydantic import BaseModel, Field

class Produto(BaseModel):
    nome: str = Field(..., min_length=5)
    categoria: str = Field(..., min_length=5)
    preco: float = Field(..., gt=0)
    quantidade: int = Field(..., ge=0)