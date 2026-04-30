from pydantic import BaseModel


class ReqValidarIdentidadeUsuario(BaseModel):
    tokenOuCredencial: str
    identificadorCanal: str


class UsuarioValidado(BaseModel):
    id: str
    status: str


class RespValidarIdentidadeUsuario(BaseModel):
    usuarioValidado: UsuarioValidado | None = None
    motivoNegacao: str | None = None
