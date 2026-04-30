from dataclasses import dataclass
from typing import Iterable

from app.servicos.mensagens.servico_usuario import RespLocalizarUsuario, UsuarioLocalizado
from app.servicos.usuario.i_servico_usuario import ServicoUsuario


@dataclass(frozen=True)
class _Usuario:
    id: str
    status_cadastro: str


class ServicoUsuarioImpl(ServicoUsuario):
    def __init__(self, usuarios: Iterable[_Usuario] | None = None):
        self._usuarios = {usuario.id: usuario for usuario in (usuarios or [])}

    def localizarUsuario(self, identificador_usuario: str) -> RespLocalizarUsuario:
        if not identificador_usuario.strip():
            return RespLocalizarUsuario(
                usuarioLocalizado=None,
                motivoNaoLocalizado="Identificador de usuario vazio.",
            )

        usuario = self._usuarios.get(identificador_usuario)
        if not usuario:
            return RespLocalizarUsuario(
                usuarioLocalizado=None,
                motivoNaoLocalizado="Usuario nao localizado.",
            )

        return RespLocalizarUsuario(
            usuarioLocalizado=UsuarioLocalizado(
                id=usuario.id,
                statusCadastro=usuario.status_cadastro,
            ),
            motivoNaoLocalizado=None,
        )
