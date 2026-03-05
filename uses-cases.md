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

Cada interface identificada é realizada por um componente com responsabilidade única:

| Interface | Componente | Responsabilidade |
|---|---|---|
| `MensagemService` | **ChatComponent** | Orquestra o envio de mensagens, monta o prompt final e persiste o histórico de conversas. |
| `AgenteService` | **AgenteComponent** | Gerencia o ciclo de vida dos agentes personalizados (criação, edição, consulta e exclusão). |
| `ContextoPessoalService` | **ContextoComponent** | Mantém o contexto pessoal persistente do usuário para enriquecimento automático dos prompts. |

---

### 5.2 Interfaces Fornecidas e Contratos das Operações

#### ChatComponent — fornece `MensagemService`

```text
<<interface>>
MensagemService
----------------------------------------
+ enviar_mensagem(usuario_id: int, agente_id: str, mensagem: str, modelo: str, max_tokens: int, temperature: float) -> dict
+ consultar_historico(usuario_id: int, chat_id: str) -> list[dict]
+ listar_chats(usuario_id: int) -> list[dict]
+ deletar_chat(usuario_id: int, chat_id: str) -> bool
```

**Contrato: `enviar_mensagem`**

Pré-condições:
- `usuario_id` deve referenciar um usuário autenticado e ativo.
- `agente_id` deve referenciar um agente existente pertencente ao usuário.
- `mensagem` não pode ser vazia.
- `temperature` deve estar no intervalo `[0.0, 1.0]`.

Pós-condições:
- A interação é persistida no histórico do chat no MongoDB.
- O retorno contém a resposta do modelo e os metadados de consumo de tokens.

---

#### AgenteComponent — fornece `AgenteService`

```text
<<interface>>
AgenteService
----------------------------------------
+ criar_agente(usuario_id: int, nome: str, especialidade: str, tom: str, estilo: str) -> dict
+ editar_agente(usuario_id: int, agente_id: str, nome: str | None, especialidade: str | None, tom: str | None, estilo: str | None) -> dict
+ buscar_agente_por_id(usuario_id: int, agente_id: str) -> dict
+ listar_agentes(usuario_id: int) -> list[dict]
+ deletar_agente(usuario_id: int, agente_id: str) -> bool
```

**Contrato: `criar_agente`**

Pré-condições:
- `usuario_id` deve referenciar um usuário existente.
- `nome` não pode ser vazio e deve ser único por usuário.
- `especialidade` não pode ser vazia.

Pós-condições:
- O agente é persistido no MongoDB associado ao `usuario_id`.
- O retorno contém os dados do agente criado, incluindo o `agente_id` gerado.

---

#### ContextoComponent — fornece `ContextoPessoalService`

```text
<<interface>>
ContextoPessoalService
----------------------------------------
+ criar_contexto(usuario_id: int, preferencias: str, nivel_tecnico: str, objetivos: str, instrucoes_permanentes: str) -> dict
+ atualizar_contexto(usuario_id: int, preferencias: str | None, nivel_tecnico: str | None, objetivos: str | None, instrucoes_permanentes: str | None) -> dict
+ buscar_contexto(usuario_id: int) -> dict
+ deletar_contexto(usuario_id: int) -> bool
```

**Contrato: `criar_contexto`**

Pré-condições:
- `usuario_id` deve referenciar um usuário existente.
- Não deve existir contexto previamente cadastrado para o usuário.
- `instrucoes_permanentes` não pode ultrapassar o limite de caracteres definido.

Pós-condições:
- O contexto é persistido no MongoDB associado ao `usuario_id`.
- O retorno contém os dados do contexto criado.

---

### 5.3 Dependências entre Componentes

| Componente | Requer | Motivo |
|---|---|---|
| **ChatComponent** | `AgenteService` (AgenteComponent) | Precisa recuperar a especialidade e as configurações do agente selecionado para compor o prompt final. |
| **ChatComponent** | `ContextoPessoalService` (ContextoComponent) | Precisa recuperar o contexto pessoal do usuário para enriquecer o prompt antes do envio ao provedor. |
| **AgenteComponent** | — | Não requer nenhum outro componente do sistema. |
| **ContextoComponent** | — | Não requer nenhum outro componente do sistema. |

---

### 5.4 Diagrama de Componentes

```mermaid
flowchart LR
    subgraph ChatComponent
        MS["<<fornece>>\nMensagemService"]
        MS_req1["<<requer>>\nAgenteService"]
        MS_req2["<<requer>>\nContextoPessoalService"]
    end

    subgraph AgenteComponent
        AS["<<fornece>>\nAgenteService"]
    end

    subgraph ContextoComponent
        CS["<<fornece>>\nContextoPessoalService"]
    end

    OR[Provedor LLM OpenRouter]

    MS_req1 -->|"buscar_agente_por_id()"| AS
    MS_req2 -->|"buscar_contexto()"| CS
    MS -->|"envia prompt montado"| OR
```
 
