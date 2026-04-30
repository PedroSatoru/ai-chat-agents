from typing import Any
from pydantic import BaseModel


class ReqVerificarConteudoSolicitacao(BaseModel):
    mensagem: str
    parametrosOpcionais: dict[str, Any] | None = None


class RespVerificarConteudoSolicitacao(BaseModel):
    solicitacaoVerificada: bool
    listaInconsistencias: list[str]
