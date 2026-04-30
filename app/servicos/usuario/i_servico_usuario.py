from abc import ABC, abstractmethod

from app.servicos.mensagens.servico_usuario import RespLocalizarUsuario


class ServicoUsuario(ABC):
    @abstractmethod
    def localizarUsuario(self, identificador_usuario: str) -> RespLocalizarUsuario:
        raise NotImplementedError()
