from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Tuple

from app.servicos.mensagens.servico_validacao_identidade import (
    RespValidarIdentidadeUsuario,
    UsuarioValidado,
)
from app.servicos.validacao_identidade.i_servico_validacao_identidade import (
    ServicoValidacaoIdentidade,
)


@dataclass
class _AuditEvent:
    token: str
    canal: str
    status: str
    created_at: datetime


class ServicoValidacaoIdentidadeImpl(ServicoValidacaoIdentidade):
    _max_failures = 3

    def __init__(self) -> None:
        self._failures: Dict[Tuple[str, str], int] = {}
        self._audit_events: list[_AuditEvent] = []

    def validarIdentidadeUsuario(
        self,
        token_ou_credencial: str,
        identificador_canal: str,
    ) -> RespValidarIdentidadeUsuario:
        token = token_ou_credencial.strip()
        canal = identificador_canal.strip()

        if not token or not canal:
            return self._negado(
                token=token,
                canal=canal,
                motivo="Token ou canal nao informado.",
            )

        if self._is_blocked(token, canal):
            return self._negado(
                token=token,
                canal=canal,
                motivo="Token bloqueado por tentativas invalidas sucessivas.",
            )

        if not self._looks_like_jwt(token):
            self._register_failure(token, canal)
            return self._negado(
                token=token,
                canal=canal,
                motivo="Token em formato invalido.",
            )

        usuario_id = self._extract_subject(token)
        self._register_success(token, canal)
        return RespValidarIdentidadeUsuario(
            usuarioValidado=UsuarioValidado(
                id=usuario_id,
                status="VALIDADO",
            ),
            motivoNegacao=None,
        )

    def _register_failure(self, token: str, canal: str) -> None:
        self._failures[(token, canal)] = self._failures.get((token, canal), 0) + 1
        self._audit("NEGADO", token, canal)

    def _register_success(self, token: str, canal: str) -> None:
        self._failures.pop((token, canal), None)
        self._audit("VALIDADO", token, canal)

    def _is_blocked(self, token: str, canal: str) -> bool:
        return self._failures.get((token, canal), 0) >= self._max_failures

    def _looks_like_jwt(self, token: str) -> bool:
        return token.count(".") == 2

    def _extract_subject(self, token: str) -> str:
        return f"user:{abs(hash(token)) % 10_000}"

    def _negado(self, token: str, canal: str, motivo: str) -> RespValidarIdentidadeUsuario:
        self._audit("NEGADO", token, canal)
        return RespValidarIdentidadeUsuario(
            usuarioValidado=None,
            motivoNegacao=motivo,
        )

    def _audit(self, status: str, token: str, canal: str) -> None:
        self._audit_events.append(
            _AuditEvent(
                token=token,
                canal=canal,
                status=status,
                created_at=datetime.now(timezone.utc),
            )
        )
