# ai-chat-agents — Entrega Parcial 1

## Integrantes
- Pedro Henrique Satoru Lima Takahashi — 22.123.019-6
- Pedro Henrique Correia de Oliveira — 22.222.009-7
- Hugo Emílio Nomura — 22.123.051-9
- Vitor Monteiro Vianna — 22.223.085-6

## Objetivo desta entrega
Implementar **2 componentes com dependência entre si**, garantindo comunicação apenas por interfaces e com injeção de dependência.

Esta entrega reutiliza a base do projeto anterior (`API_polyglot-persistence`) e mantém os mesmos bancos já reativados:
- PostgreSQL (mesma `DATABASE_URL`)
- MongoDB (`chat_db`, coleção `chat_conversations`)

## Componentes implementados

### 1) Componente Cliente: `ChatService`
- Arquivo: [app/chat/service/chat_service.py](app/chat/service/chat_service.py)
- Responsabilidade: regra de negócio de chat (`send_message`, `get_history`).
- Dependência requerida: interface `IChatRepository`.

### 2) Componente Fornecedor: `MongoChatRepository`
- Arquivo: [app/chat/repository/mongo_chat_repository.py](app/chat/repository/mongo_chat_repository.py)
- Responsabilidade: persistência e consulta de conversas no MongoDB.
- Interface fornecida: `IChatRepository`.

## Interfaces (fornecidas/requeridas)

- `IChatService`: [app/chat/interfaces/i_chat_service.py](app/chat/interfaces/i_chat_service.py)
- `IChatRepository`: [app/chat/interfaces/repository/i_chat_repository.py](app/chat/interfaces/repository/i_chat_repository.py)

O roteador usa somente `IChatService`, e o `ChatService` usa somente `IChatRepository`.

## Injeção de dependência

Implementada com FastAPI `Depends` e fábrica de objetos:
- Fábrica: [app/startup.py](app/startup.py)
- Dependências: [app/chat/dependencies.py](app/chat/dependencies.py)
- Uso no endpoint: [app/chat/router.py](app/chat/router.py)

Fluxo de DI:
1. `router` pede `IChatService`
2. `dependencies` chama `startup.build_chat_service()`
3. `startup` injeta `MongoChatRepository` no construtor de `ChatService`

## Endpoints desta entrega

- `POST /api/chat/send`
  - Header obrigatório: `x-user-id`
  - Body: prompt + parâmetros de geração
- `GET /api/chat/{conversation_id}/history`
  - Header obrigatório: `x-user-id`

## Estrutura criada

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
   - `pip install -r requirements.txt`
2. Criar `.env` a partir de `.env.example`
3. Subir API
   - `uvicorn app.main:app --reload`

## Observação acadêmica

Para esta **primeira entrega parcial**, o foco foi comprovar:
- desacoplamento por interface;
- injeção de dependência;
- comunicação entre 2 componentes.

A integração com provedores reais de LLM e autenticação completa fica para as próximas entregas incrementais.
