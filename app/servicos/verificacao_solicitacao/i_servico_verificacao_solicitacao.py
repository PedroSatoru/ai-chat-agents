from abc import ABC, abstractmethod
from typing import Any

from app.servicos.mensagens.servico_verificacao_solicitacao import RespVerificarConteudoSolicitacao


class ServicoVerificacaoSolicitacao(ABC):
    @abstractmethod
    def verificarConteudoSolicitacao(
        self,
        mensagem: str,
        parametros_opcionais: dict[str, Any] | None,
    ) -> RespVerificarConteudoSolicitacao:
        raise NotImplementedError()
