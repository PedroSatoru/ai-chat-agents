from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.servicos.dependencies import (
    get_servico_usuario,
    get_servico_validacao_identidade,
    get_servico_verificacao_solicitacao,
    get_token_ou_credencial,
)
from app.servicos.mensagens.servico_usuario import (
    ReqLocalizarUsuario,
    RespLocalizarUsuario,
)
from app.servicos.mensagens.servico_validacao_identidade import (
    ReqValidarIdentidadeUsuario,
    RespValidarIdentidadeUsuario,
)
from app.servicos.mensagens.servico_verificacao_solicitacao import (
    ReqVerificarConteudoSolicitacao,
    RespVerificarConteudoSolicitacao,
)
from app.servicos.usuario.i_servico_usuario import ServicoUsuario
from app.servicos.validacao_identidade.i_servico_validacao_identidade import (
    ServicoValidacaoIdentidade,
)
from app.servicos.verificacao_solicitacao.i_servico_verificacao_solicitacao import (
    ServicoVerificacaoSolicitacao,
)

router = APIRouter()


@router.post("/usuario/localizar")
def localizar_usuario(
    payload: ReqLocalizarUsuario,
    servico: Annotated[ServicoUsuario, Depends(get_servico_usuario)],
) -> RespLocalizarUsuario:
    return servico.localizarUsuario(payload.identificadorUsuario)


@router.post("/identidade/validar")
def validar_identidade_usuario(
    payload: ReqValidarIdentidadeUsuario,
    servico: Annotated[
        ServicoValidacaoIdentidade,
        Depends(get_servico_validacao_identidade),
    ],
    token_ou_credencial: Annotated[str, Depends(get_token_ou_credencial)],
) -> RespValidarIdentidadeUsuario:
    token = payload.tokenOuCredencial or token_ou_credencial
    return servico.validarIdentidadeUsuario(token, payload.identificadorCanal)


@router.post("/solicitacao/verificar")
def verificar_conteudo_solicitacao(
    payload: ReqVerificarConteudoSolicitacao,
    servico: Annotated[
        ServicoVerificacaoSolicitacao,
        Depends(get_servico_verificacao_solicitacao),
    ],
) -> RespVerificarConteudoSolicitacao:
    parametros: dict[str, Any] | None = payload.parametrosOpcionais
    return servico.verificarConteudoSolicitacao(payload.mensagem, parametros)
