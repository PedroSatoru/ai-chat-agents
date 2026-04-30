from app.servicos.usuario.servico_usuario import ServicoUsuarioImpl, _Usuario
from app.servicos.validacao_identidade.servico_validacao_identidade import (
    ServicoValidacaoIdentidadeImpl,
)
from app.servicos.verificacao_solicitacao.servico_verificacao_solicitacao import (
    ServicoVerificacaoSolicitacaoImpl,
)


def test_servico_usuario_localizar_usuario_encontrado() -> None:
    servico = ServicoUsuarioImpl(usuarios=[_Usuario(id="user-001", status_cadastro="ATIVO")])
    resposta = servico.localizarUsuario("user-001")

    assert resposta.usuarioLocalizado is not None
    assert resposta.usuarioLocalizado.id == "user-001"
    assert resposta.usuarioLocalizado.statusCadastro == "ATIVO"
    assert resposta.motivoNaoLocalizado is None


def test_servico_usuario_localizar_usuario_nao_encontrado() -> None:
    servico = ServicoUsuarioImpl(usuarios=[])
    resposta = servico.localizarUsuario("user-999")

    assert resposta.usuarioLocalizado is None
    assert resposta.motivoNaoLocalizado == "Usuario nao localizado."


def test_servico_validacao_identidade_bloqueio_por_tentativas() -> None:
    servico = ServicoValidacaoIdentidadeImpl()

    for _ in range(3):
        resposta = servico.validarIdentidadeUsuario("token-invalido", "web")
        assert resposta.usuarioValidado is None

    resposta = servico.validarIdentidadeUsuario("token-invalido", "web")
    assert resposta.usuarioValidado is None
    assert "bloqueado" in (resposta.motivoNegacao or "").lower()


def test_servico_verificacao_solicitacao_rejeita_mensagem_vazia() -> None:
    servico = ServicoVerificacaoSolicitacaoImpl()
    resposta = servico.verificarConteudoSolicitacao("   ", None)

    assert not resposta.solicitacaoVerificada
    assert "Mensagem vazia" in " ".join(resposta.listaInconsistencias)
