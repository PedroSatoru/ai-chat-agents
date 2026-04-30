# ai-chat-agents — Entrega Parcial (Serviços)

## Integrantes
- Pedro Henrique Satoru Lima Takahashi — 22.123.019-6
- Pedro Henrique Correia de Oliveira — 22.222.009-7
- Hugo Emílio Nomura — 22.123.051-9
- Vitor Monteiro Vianna — 22.223.085-6

## Objetivo desta entrega
Implementar serviços em arquitetura orientada a serviços, definir estilo de coordenação e estratégias de testes, com endpoints funcionais.

Esta entrega reutiliza a base do projeto anterior (`API_polyglot-persistence`) e mantém os mesmos bancos já reativados:
- PostgreSQL (mesma `DATABASE_URL`)
- MongoDB (`chat_db`, coleção `chat_conversations`)

## Serviços implementados

### 1) ServicoUsuario
- Implementação: [app/servicos/usuario/servico_usuario.py](app/servicos/usuario/servico_usuario.py)
- Interface: [app/servicos/usuario/i_servico_usuario.py](app/servicos/usuario/i_servico_usuario.py)

### 2) ServicoValidacaoIdentidade
- Implementação: [app/servicos/validacao_identidade/servico_validacao_identidade.py](app/servicos/validacao_identidade/servico_validacao_identidade.py)
- Interface: [app/servicos/validacao_identidade/i_servico_validacao_identidade.py](app/servicos/validacao_identidade/i_servico_validacao_identidade.py)

### 3) ServicoVerificacaoSolicitacao
- Implementação: [app/servicos/verificacao_solicitacao/servico_verificacao_solicitacao.py](app/servicos/verificacao_solicitacao/servico_verificacao_solicitacao.py)
- Interface: [app/servicos/verificacao_solicitacao/i_servico_verificacao_solicitacao.py](app/servicos/verificacao_solicitacao/i_servico_verificacao_solicitacao.py)

## Estilo de coordenação
**Orquestração** via API (FastAPI), centralizando a sequência das chamadas e políticas.

## Arquitetura adotada
Arquitetura orientada a serviços (SOA) com orquestração na camada de API. Os serviços são expostos por endpoints HTTP e organizados por interfaces e implementações com injeção de dependência.

## Injeção de dependência
- Fábrica: [app/startup.py](app/startup.py)
- Dependências: [app/servicos/dependencies.py](app/servicos/dependencies.py)
- Rotas: [app/servicos/router.py](app/servicos/router.py)

## Endpoints desta entrega
- `POST /api/usuario/localizar`
- `POST /api/identidade/validar`
- `POST /api/solicitacao/verificar`

## Documentação
- [docs/entrega-servicos.md](docs/entrega-servicos.md)

```
ai-chat-agents/
  app/
    main.py
    startup.py
    core/config.py
    shared/utils.py
    chat/
      router.py
      dependencies.py
      model.py
      interfaces/
        i_chat_service.py
        repository/i_chat_repository.py
      repository/mongo_chat_repository.py
      service/chat_service.py
      messages/
        message.py
        user_message.py
        assistant_message.py
  requirements.txt
  .env.example
```

## Como executar

1. Instalar dependências
  - `pip install -r app/requirements.txt`
2. Criar `.env` a partir de `.env.example`
3. Subir API
   - `uvicorn app.main:app --reload`

## Testes
1. Instalar dependências
  - `pip install -r app/requirements.txt`
2. Executar testes
  - `pytest`
