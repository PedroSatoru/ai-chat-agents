# TEMPLATE - LABORATORIO LPS

## Dominio do Sistema:
AgentIA - plataforma de atendimento conversacional com agentes especializados e integracao a LLM.

## Subdominios

| Subdominio | Responsabilidades | Tipo |
| --- | --- | --- |
| Atendimento Conversacional | Orquestrar atendimento, encaminhar solicitacao e consolidar resposta | Core |
| Identidade e Validacao | Localizar usuario, validar credencial e verificar solicitacao | Suporte |
| Conversa e Historico | Persistir conversas, registrar mensagens e recuperar historico | Generico |

## Requisitos da LPS (comum, opcional, alternativo)

| ID | Requisito | Tipo de Feature |
| --- | --- | --- |
| LPS-01 | Orquestrar o atendimento conversacional do inicio ao fim | Comum |
| LPS-02 | Validar identidade do usuario antes de processar a solicitacao | Comum |
| LPS-03 | Verificar conteudo minimo da solicitacao (mensagem e parametros) | Comum |
| LPS-04 | Registrar conversa e historico de mensagens | Comum |
| LPS-05 | Integrar com provedor de LLM para gerar respostas | Comum |
| LPS-06 | Expor API HTTP para consumo dos canais | Comum |
| LPS-07 | Gerenciar agentes personalizados (criar/editar) | Opcional |
| LPS-08 | Gerenciar contexto pessoal do usuario | Opcional |
| LPS-09 | Consultar historico completo da conversa | Opcional |
| LPS-10 | Suporte a multicanal (web e mobile) | Opcional |
| LPS-11 | Auditar eventos de autenticacao e validacao | Opcional |
| LPS-12 | Autenticacao via JWT ou API Key | Alternativo |
| LPS-13 | Provedor LLM OpenRouter ou LLM local/privado | Alternativo |
| LPS-14 | Persistencia de conversa em MongoDB ou Postgres | Alternativo |

## Modelo de Features

Legenda: [M] obrigatoria, [O] opcional, [A] alternativa (exclusiva)

```mermaid
mindmap
  root((AgentIA LPS))
    Core[M]
      OrquestracaoAtendimento[M]
      IdentidadeValidacao[M]
        ServicoUsuario[M]
        ServicoValidacaoIdentidade[M]
        ServicoVerificacaoSolicitacao[M]
      ConversaHistorico[M]
        ChatService[M]
        RepositorioConversa[M]
      APIHTTP[M]
      IntegracaoLLM[M]
    Variabilidades
      Autenticacao[A]
        JWT
        APIKey
      ProvedorLLM[A]
        OpenRouter
        LLM_Local
      PersistenciaConversa[A]
        MongoDB
        Postgres
      AgentesPersonalizados[O]
      ContextoPessoal[O]
      ConsultaHistorico[O]
      Multicanal[O]
      AuditoriaAutenticacao[O]
```

## Diagrama de Casos de Uso

Legenda: (C) comum, (O) opcional, (A) alternativo

```mermaid
flowchart LR
    U[Usuario]
    LLM[Provedor LLM]

    subgraph S[System AgentIA LPS]
        UC1["Submeter solicitacao de atendimento (C)"]
        UC2["Validar identidade (C)"]
        UC3["Verificar conteudo da solicitacao (C)"]
        UC4["Registrar conversa e historico (C)"]
        UC5["Enviar mensagem ao LLM (C)"]
        UC6["Receber resposta e apresentar retorno (C)"]

        UC7["Criar agente personalizado (O)"]
        UC8["Editar agente personalizado (O)"]
        UC9["Gerenciar contexto pessoal (O)"]
        UC10["Consultar historico (O)"]
        UC11["Selecionar agente para conversa (O)"]

        UC12["Autenticar via JWT (A)"]
        UC13["Autenticar via API Key (A)"]
        UC14["Atender via OpenRouter (A)"]
        UC15["Atender via LLM local (A)"]
    end

    U --> UC1
    U --> UC2
    U --> UC3
    U --> UC4
    U --> UC6

    U --> UC7
    U --> UC8
    U --> UC9
    U --> UC10
    U --> UC11

    UC2 -.alternativa.-> UC12
    UC2 -.alternativa.-> UC13

    UC5 --> LLM
    UC5 -.alternativa.-> UC14
    UC5 -.alternativa.-> UC15

    UC1 --> UC2 --> UC3 --> UC4 --> UC5 --> UC6
```

## Produtos da LPS

### Produto 1:
Basico (Atendimento Essencial)

**Features incluidas:**
- Core assets completos.
- Autenticacao JWT.
- Provedor LLM OpenRouter.
- Persistencia de conversa em MongoDB.

### Produto 2:
Premium (Atendimento Personalizado)

**Features incluidas:**
- Core assets completos.
- Autenticacao API Key.
- Provedor LLM local/privado.
- Persistencia de conversa em Postgres.
- Agentes personalizados.
- Contexto pessoal.
- Consulta historico.
- Multicanal (web e mobile).
- Auditoria de autenticacao e validacao.
