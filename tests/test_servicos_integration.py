from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_api_localizar_usuario() -> None:
    response = client.post(
        "/api/usuario/localizar",
        json={"identificadorUsuario": "user-001"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["usuarioLocalizado"]["id"] == "user-001"


def test_api_validar_identidade() -> None:
    response = client.post(
        "/api/identidade/validar",
        json={
            "tokenOuCredencial": "header.payload.signature",
            "identificadorCanal": "web",
        },
        headers={"authorization": "header.payload.signature"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["usuarioValidado"]["status"] == "VALIDADO"


def test_api_verificar_solicitacao() -> None:
    response = client.post(
        "/api/solicitacao/verificar",
        json={"mensagem": "ola", "parametrosOpcionais": {"foo": "bar"}},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["solicitacaoVerificada"] is True


def test_fluxo_orquestrado_validacao_e_verificacao() -> None:
    from app.servicos.validacao_identidade.servico_validacao_identidade import (
        ServicoValidacaoIdentidadeImpl,
    )
    from app.servicos.verificacao_solicitacao.servico_verificacao_solicitacao import (
        ServicoVerificacaoSolicitacaoImpl,
    )

    servico_validacao = ServicoValidacaoIdentidadeImpl()
    servico_verificacao = ServicoVerificacaoSolicitacaoImpl()

    resposta_validacao = servico_validacao.validarIdentidadeUsuario(
        "header.payload.signature",
        "web",
    )
    assert resposta_validacao.usuarioValidado is not None

    resposta_verificacao = servico_verificacao.verificarConteudoSolicitacao(
        "mensagem valida",
        {"canal": "web"},
    )
    assert resposta_verificacao.solicitacaoVerificada is True
