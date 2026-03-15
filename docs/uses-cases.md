# AgentIA — Diagrama de Casos de Uso e Fluxos Principais

## 1. Visão Geral do Sistema

O AgentIA é uma plataforma de assistentes virtuais inteligentes com orquestração de agentes de IA especializados. O objetivo é permitir conversas mais precisas e personalizadas, combinando:
- contexto pessoal do usuário;
- especialidade do agente selecionado;
- processamento de mensagens via provedor de LLM.

## 2. Atores

- **Usuário Comum:** cria conta, configura preferências, cria agentes e conversa com a IA.
- **Provedor de LLM (OpenRouter):** processa prompts e retorna respostas geradas.

### 2.1 Infraestrutura de Persistência (não são atores)

- **PostgreSQL:** armazenamento de dados de identidade, autenticação e credenciais do usuário.
- **MongoDB:** armazenamento de agentes, contexto pessoal e histórico de conversas.

---

## 3. Diagrama de Casos de Uso

```mermaid
flowchart LR
    U[Usuário Comum]
    OR[Provedor LLM OpenRouter]

    subgraph I["Infraestrutura de Persistência (não atores)"]
        PG[(PostgreSQL)]
        MG[(MongoDB)]
    end

    subgraph S[System AgentIA]
        UC1["Cadastrar conta"]
        UC2["Autenticar login"]
        UC3["Gerenciar perfil e credenciais"]
        UC4["Criar agente personalizado"]
        UC5["Editar agente personalizado"]
        UC6["Gerenciar contexto pessoal"]
        UC7["Selecionar agente para conversa"]
        UC8["Enviar mensagem no chat"]
        UC9["Receber resposta especializada"]
        UC10["Consultar histórico de conversa"]
    end

    U --> UC1
    U --> UC2
    U --> UC3
    U --> UC4
    U --> UC5
    U --> UC6
    U --> UC7
    U --> UC8
    U --> UC9
    U --> UC10

    UC1 -. persistência .-> PG
    UC2 -. consulta/autenticação .-> PG
    UC3 -. atualização .-> PG

    UC4 -. persistência .-> MG
    UC5 -. atualização .-> MG
    UC6 -. persistência .-> MG

    UC8 --> OR
    UC9 --> OR
    UC10 -. consulta .-> MG
```

---

## 4. Detalhamento dos Fluxos Principais

## Fluxo 1 — Envio e Processamento de Mensagem

**Objetivo:** gerar uma resposta de IA contextualizada para a mensagem do usuário.

**Entrada:** mensagem do usuário, agente selecionado, parâmetros de geração e token de autenticação.  
**Saída:** resposta da IA, metadados de consumo e registro da interação.  
**Atores:** Usuário Comum e Provedor de LLM (OpenRouter).

### Passo a passo
1. Usuário seleciona o agente e envia a mensagem no chat.
2. Sistema autentica o usuário e valida os dados da requisição.
3. Sistema recupera contexto pessoal do usuário.
4. Sistema recupera a definição de especialidade do agente.
5. Sistema monta o prompt final (contexto + especialidade + mensagem atual).
6. Sistema envia o prompt ao provedor de LLM.
7. Sistema recebe a resposta, registra histórico e retorna o resultado ao usuário.

### Fluxos de Exceção

**Exceção 1.1 — Falha de autenticação**
1. Sistema identifica token inválido, expirado ou ausente.
2. Sistema interrompe o processamento da mensagem.
3. Sistema retorna erro de autenticação ao usuário.

**Exceção 1.2 — Indisponibilidade do OpenRouter**
1. Sistema envia requisição ao provedor de LLM.
2. OpenRouter retorna erro ou indisponibilidade de serviço.
3. Sistema registra falha técnica e retorna erro de integração ao usuário.

---

## Fluxo 2 — Criação de Novo Agente

**Objetivo:** permitir a criação de agentes especializados reutilizáveis.

**Entrada:** nome do agente, descrição da especialidade, tom e estilo de resposta.  
**Saída:** agente criado e disponível para seleção no chat.  
**Atores:** Usuário Comum.

### Passo a passo
1. Usuário acessa a funcionalidade de criação de agente.
2. Sistema recebe e valida os campos obrigatórios.
3. Sistema aplica regras de negócio (unicidade de nome por usuário, limites de tamanho e formato).
4. Sistema persiste o agente.
5. Sistema confirma o cadastro e disponibiliza o agente no catálogo.

### Fluxos de Exceção

**Exceção 2.1 — Dados obrigatórios inválidos**
1. Sistema valida os campos de criação do agente.
2. Sistema identifica ausência ou formato inválido de dados.
3. Sistema interrompe o cadastro e retorna mensagem de validação.

**Exceção 2.2 — Nome de agente duplicado**
1. Sistema verifica unicidade do nome para o mesmo usuário.
2. Sistema encontra agente já existente com o mesmo nome.
3. Sistema rejeita a criação e solicita outro nome.

---

## Fluxo 3 — Gerenciamento de Contexto Pessoal

**Objetivo:** manter informações persistentes para personalizar respostas futuras.

**Entrada:** preferências de comunicação, nível técnico, objetivos e instruções permanentes.  
**Saída:** contexto pessoal atualizado e pronto para uso no processamento de mensagens.  
**Atores:** Usuário Comum.

### Passo a passo
1. Usuário cria ou atualiza seu contexto pessoal.
2. Sistema valida formato, tamanho e conteúdo permitido.
3. Sistema salva o contexto em armazenamento persistente.
4. Em cada nova conversa, sistema recupera o contexto automaticamente.
5. Sistema incorpora o contexto no prompt antes da chamada ao modelo.

### Fluxos de Exceção

**Exceção 3.1 — Conteúdo inválido ou acima do limite**
1. Sistema valida tamanho e formato do contexto enviado.
2. Sistema identifica conteúdo fora das regras.
3. Sistema bloqueia a atualização e retorna erro de validação.

---

## 5. Componentes, Interfaces e Contratos

### 5.1 Identificação de Componentes

Nesta entrega parcial, os componentes implementados e suas responsabilidades são:

| Interface | Componente | Responsabilidade |
|---|---|---|
| `IChatService` | **ChatService** | Orquestra o envio de mensagens e consulta de histórico, aplicando regras de negócio do chat. |
| `IChatRepository` | **MongoChatRepository** | Persiste e recupera conversas no MongoDB. |

---

### 5.2 Interfaces Fornecidas e Contratos das Operações

#### ChatService — fornece `IChatService`

```text
<<interface>>
IChatService
----------------------------------------
+ send_message(user_id: str, payload: SendMessagePayload) -> dict
+ get_history(user_id: str, conversation_id: str) -> list[dict]
```

**Contrato: `send_message`**

Pré-condições:
- `user_id` deve ser informado no header `x-user-id`.
- `payload.prompt` não pode ser vazio.
- `payload.temperature` deve estar no intervalo `[0.0, 1.0]`.

Pós-condições:
- A conversa é criada/atualizada no MongoDB via `IChatRepository`.
- O retorno contém `conversation_id` e a lista de mensagens da conversa.

---

#### MongoChatRepository — fornece `IChatRepository`

```text
<<interface>>
IChatRepository
----------------------------------------
+ get_conversation(user_id: str, conversation_id: str) -> Optional[dict]
+ save_conversation(conversation: dict) -> None
```

**Contrato: `save_conversation`**

Pré-condições:
- `conversation` deve conter `conversation_id` e `user_id`.

Pós-condições:
- A conversa é persistida/atualizada na coleção `chat_conversations`.

---

### 5.3 Dependências entre Componentes

| Componente | Requer | Motivo |
|---|---|---|
| **Router (camada de API)** | `IChatService` | Consome apenas a abstração do serviço de chat via injeção de dependência. |
| **ChatService** | `IChatRepository` | Persiste e consulta conversas sem depender da implementação concreta de banco. |
| **MongoChatRepository** | — | Implementação concreta que acessa MongoDB. |

---

### 5.4 Diagrama de Componentes

```mermaid
flowchart LR
    subgraph APILayer["Camada API"]
        RT["Router"]
    end

    subgraph ServiceLayer["Camada Serviço"]
        CS["<<fornece>>\nIChatService\nChatService"]
        CSREQ["<<requer>>\nIChatRepository"]
    end

    subgraph RepositoryLayer["Camada Repositório"]
        MONGO["<<implementa>>\nIChatRepository\nMongoChatRepository"]
    end

    RT -->|"Depends(IChatService)"| CS
    CSREQ --> MONGO
```

### 5.5 Mecanismo de Injeção de Dependência

- A resolução de `IChatService` ocorre em `app/chat/dependencies.py` com FastAPI `Depends`.
- A construção do serviço fica centralizada em `app/startup.py`.
- O `Startup` injeta `MongoChatRepository` no construtor de `ChatService`.

Esse arranjo evita acoplamento direto entre endpoint e infraestrutura de persistência.
 
