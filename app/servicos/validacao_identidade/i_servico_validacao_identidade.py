from abc import ABC, abstractmethod

from app.servicos.mensagens.servico_validacao_identidade import RespValidarIdentidadeUsuario


class ServicoValidacaoIdentidade(ABC):
    @abstractmethod
    def validarIdentidadeUsuario(
        self,
        token_ou_credencial: str,
        identificador_canal: str,
    ) -> RespValidarIdentidadeUsuario:
        raise NotImplementedError()
