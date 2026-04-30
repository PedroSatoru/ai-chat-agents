from typing import Annotated

from fastapi import Depends, Header

from app.servicos.usuario.i_servico_usuario import ServicoUsuario
from app.servicos.validacao_identidade.i_servico_validacao_identidade import (
    ServicoValidacaoIdentidade,
)
from app.servicos.verificacao_solicitacao.i_servico_verificacao_solicitacao import (
    ServicoVerificacaoSolicitacao,
)
from app.startup import startup


def get_current_token(authorization: Annotated[str | None, Header()] = None) -> str:
    return authorization or ""


def get_servico_usuario() -> ServicoUsuario:
    return startup.build_servico_usuario()


def get_servico_validacao_identidade() -> ServicoValidacaoIdentidade:
    return startup.build_servico_validacao_identidade()


def get_servico_verificacao_solicitacao() -> ServicoVerificacaoSolicitacao:
    return startup.build_servico_verificacao_solicitacao()


def get_token_ou_credencial(
    token: Annotated[str, Depends(get_current_token)],
) -> str:
    return token
