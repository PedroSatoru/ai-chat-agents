# ai-chat-agents — Entrega Parcial 1

## Integrantes
- Pedro Henrique Satoru Lima Takahashi — 22.123.019-6
- Pedro Henrique Correia de Oliveira — 22.222.009-7
- Hugo Emílio Nomura — 22.123.051-9
- Vitor Monteiro Vianna — 22.223.085-6

## Objetivo desta entrega
Implementar **2 componentes com dependência entre si**, garantindo comunicação apenas por interfaces e com injeção de dependência.

Toda a documentação do trabalho está centralizada na pasta `docs/`.

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

## Como ocorre a comunicação entre os componentes

A comunicação entre os dois componentes implementados segue um fluxo em camadas, mediado exclusivamente pelas interfaces:

```
HTTP Request
    │
    ▼
Router (app/chat/router.py)
    │  chama service.send_message() ou service.get_history()
    │  referência do tipo: IChatService
    ▼
ChatService (app/chat/service/chat_service.py)
    │  chama self._repository.get_conversation() / save_conversation()
    │  referência do tipo: IChatRepository
    ▼
MongoChatRepository (app/chat/repository/mongo_chat_repository.py)
    │  executa operações reais no MongoDB
    ▼
MongoDB (chat_db → chat_conversations)
```

**Passo a passo de uma requisição `POST /api/chat/send`:**

1. O `router` recebe a requisição HTTP com o payload e o header `x-user-id`.
2. O FastAPI resolve `IChatService` via `Depends(get_chat_service)` — o router nunca sabe qual classe concreta está sendo usada.
3. O router chama `service.send_message(user_id, payload)` no contrato de `IChatService`.
4. O `ChatService` executa a regra de negócio: gera ou recupera o `conversation_id`, monta as mensagens e chama `self._repository.get_conversation()` e `self._repository.save_conversation()` no contrato de `IChatRepository`.
5. O `MongoChatRepository` traduz essas chamadas para operações MongoDB (`find_one` e `update_one` com `upsert`).
6. O resultado sobe pela cadeia de volta ao router, que serializa e devolve ao cliente.

Em nenhum momento o router conhece `ChatService` nem `MongoChatRepository`; em nenhum momento o `ChatService` conhece `MongoChatRepository`. Toda a comunicação ocorre pelos contratos definidos nas interfaces.

---

## Justificativa do desacoplamento direto

O acoplamento direto foi evitado por três decisões arquiteturais combinadas:

### 1. Interfaces como único contrato de comunicação

Cada camada depende apenas da abstração da camada seguinte, nunca da implementação concreta:

| Quem chama | Depende de | Nunca importa |
|---|---|---|
| `router.py` | `IChatService` | `ChatService` |
| `ChatService` | `IChatRepository` | `MongoChatRepository` |

Isso significa que trocar `MongoChatRepository` por, por exemplo, um `InMemoryChatRepository` para testes exige alterar **apenas** a fábrica em `startup.py`, sem tocar no `ChatService` nem no `router`.

### 2. Injeção de dependência via construtor

O `ChatService` recebe o repositório pelo construtor:

```python
# app/chat/service/chat_service.py
class ChatService(IChatService):
    def __init__(self, repository: IChatRepository):  # tipo: interface
        self._repository = repository
```

Ele nunca instancia `MongoChatRepository` diretamente. Quem decide qual implementação usar é o `Startup`, que concentra toda a lógica de montagem do grafo de dependências em um único lugar (`app/startup.py`).

### 3. Composition root centralizado

O único ponto onde classes concretas são referenciadas entre si é `app/startup.py`:

```python
# app/startup.py
class Startup:
    def get_chat_repository(self) -> IChatRepository:      # retorna interface
        return MongoChatRepository(mongo_db)               # única menção à classe concreta

    def build_chat_service(self) -> IChatService:          # retorna interface
        return ChatService(repository=self.get_chat_repository())
```

Todo o restante do código (router, service, testes futuros) trabalha apenas com as interfaces — se o banco mudar de MongoDB para outro, o impacto fica restrito a este arquivo e à nova classe que implementar `IChatRepository`.

---

## Endpoints desta entrega

- `POST /api/chat/send`
  - Header obrigatório: `x-user-id`
  - Body: prompt + parâmetros de geração
- `GET /api/chat/{conversation_id}/history`
  - Header obrigatório: `x-user-id`

## Estrutura criada

```
ai-chat-agents/
  docs/
    uses-cases.md
    documentacao_tecnologias.md
    pontos-de-reuso.md
  app/
    main.py
    startup.py
    .env.example
    requirements.txt
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
```

## Como executar

1. Instalar dependências
  - `pip install -r app/requirements.txt`
2. Criar `.env` na raiz a partir de `app/.env.example`
  - `cp app/.env.example .env`
3. Subir API a partir da raiz do projeto
  - `uvicorn app.main:app --reload`

A revisão do modelo arquitetural foi consolidada em:
- `docs/uses-cases.md`

Nesta revisão, os contratos foram atualizados para as interfaces implementadas na entrega parcial:
- `IChatService` (fornecida por `ChatService`)
- `IChatRepository` (fornecida por `MongoChatRepository`)

Também foi documentado o fluxo de dependências via DI entre Router -> IChatService -> IChatRepository.

## Observação acadêmica

Para esta **primeira entrega parcial**, o foco foi comprovar:
- desacoplamento por interface;
- injeção de dependência;
- comunicação entre 2 componentes.

A integração com provedores reais de LLM e autenticação completa fica para as próximas entregas incrementais.
