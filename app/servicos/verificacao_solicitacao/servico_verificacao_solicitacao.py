from __future__ import annotations

from typing import Any

from app.servicos.mensagens.servico_verificacao_solicitacao import (
    RespVerificarConteudoSolicitacao,
)
from app.servicos.verificacao_solicitacao.i_servico_verificacao_solicitacao import (
    ServicoVerificacaoSolicitacao,
)


class ServicoVerificacaoSolicitacaoImpl(ServicoVerificacaoSolicitacao):
    _max_mensagem_size = 5000

    def verificarConteudoSolicitacao(
        self,
        mensagem: str,
        parametros_opcionais: dict[str, Any] | None,
    ) -> RespVerificarConteudoSolicitacao:
        inconsistencias: list[str] = []
        mensagem_sanitizada = self._sanitize_message(mensagem)

        if not mensagem_sanitizada.strip():
            inconsistencias.append("Mensagem vazia ou somente espacos.")

        if len(mensagem_sanitizada) > self._max_mensagem_size:
            inconsistencias.append("Mensagem acima do limite de 5000 caracteres.")

        if parametros_opcionais is not None and not isinstance(parametros_opcionais, dict):
            inconsistencias.append("Parametros opcionais devem ser um objeto.")
        elif isinstance(parametros_opcionais, dict):
            inconsistencias.extend(self._validate_params(parametros_opcionais))

        return RespVerificarConteudoSolicitacao(
            solicitacaoVerificada=len(inconsistencias) == 0,
            listaInconsistencias=inconsistencias,
        )

    def _sanitize_message(self, mensagem: str) -> str:
        return mensagem.replace("\x00", "").strip()

    def _validate_params(self, parametros: dict[str, Any]) -> list[str]:
        inconsistencias: list[str] = []
        for key in parametros.keys():
            if not isinstance(key, str) or not key.strip():
                inconsistencias.append("Parametro com chave invalida.")
        return inconsistencias
