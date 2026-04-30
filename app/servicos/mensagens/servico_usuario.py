from pydantic import BaseModel


class ReqLocalizarUsuario(BaseModel):
    identificadorUsuario: str


class UsuarioLocalizado(BaseModel):
    id: str
    statusCadastro: str


class RespLocalizarUsuario(BaseModel):
    usuarioLocalizado: UsuarioLocalizado | None = None
    motivoNaoLocalizado: str | None = None
