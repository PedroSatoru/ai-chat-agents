from functools import lru_cache

from app.chat.interfaces.i_chat_service import IChatService
from app.chat.interfaces.repository.i_chat_repository import IChatRepository
from app.chat.repository.mongo_chat_repository import MongoChatRepository
from app.chat.service.chat_service import ChatService
from app.core.config import mongo_db
from app.servicos.usuario.i_servico_usuario import ServicoUsuario
from app.servicos.usuario.servico_usuario import ServicoUsuarioImpl, _Usuario
from app.servicos.validacao_identidade.i_servico_validacao_identidade import (
    ServicoValidacaoIdentidade,
)
from app.servicos.validacao_identidade.servico_validacao_identidade import (
    ServicoValidacaoIdentidadeImpl,
)
from app.servicos.verificacao_solicitacao.i_servico_verificacao_solicitacao import (
    ServicoVerificacaoSolicitacao,
)
from app.servicos.verificacao_solicitacao.servico_verificacao_solicitacao import (
    ServicoVerificacaoSolicitacaoImpl,
)


class Startup:
    @lru_cache
    def get_chat_repository(self) -> IChatRepository:
        return MongoChatRepository(mongo_db)

    def build_chat_service(self) -> IChatService:
        return ChatService(repository=self.get_chat_repository())

    @lru_cache
    def get_servico_usuario(self) -> ServicoUsuario:
        usuarios = [
            _Usuario(id="user-001", status_cadastro="ATIVO"),
            _Usuario(id="user-002", status_cadastro="INATIVO"),
        ]
        return ServicoUsuarioImpl(usuarios=usuarios)

    @lru_cache
    def get_servico_validacao_identidade(self) -> ServicoValidacaoIdentidade:
        return ServicoValidacaoIdentidadeImpl()

    @lru_cache
    def get_servico_verificacao_solicitacao(self) -> ServicoVerificacaoSolicitacao:
        return ServicoVerificacaoSolicitacaoImpl()

    def build_servico_usuario(self) -> ServicoUsuario:
        return self.get_servico_usuario()

    def build_servico_validacao_identidade(self) -> ServicoValidacaoIdentidade:
        return self.get_servico_validacao_identidade()

    def build_servico_verificacao_solicitacao(self) -> ServicoVerificacaoSolicitacao:
        return self.get_servico_verificacao_solicitacao()


startup = Startup()
