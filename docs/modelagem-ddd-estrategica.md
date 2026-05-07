# Modelagem DDD Estrategica do ai-chat-agents

## 1. Identificacao do dominio

O dominio do sistema foi reduzido para tres subdominios principais, o suficiente para expressar o negocio do atendimento em chat sem fragmentar demais a analise.

| Subdominio | Classificacao | Justificativa |
|---|---|---|
| Atendimento Conversacional | Core | E o fluxo que entrega valor direto ao usuario e concentra a experiencia principal do sistema. |
| Identidade e Validacao | Suporte | Garante que apenas usuarios validos entrem no fluxo e que a mensagem tenha condicoes minimas de processamento. |
| Conversa e Historico | Generico | Sustenta persistencia e rastreabilidade das interacoes sem definir o valor central do negocio. |

## 2. Definicao de Bounded Contexts

| Bounded Context | Responsabilidades | Relacao com o repositorio |
|---|---|---|
| Orquestracao de Atendimento | Receber a mensagem, coordenar validacoes, decidir o proximo passo e consolidar a resposta final. | `app/servicos/router.py`, `app/chat/router.py`, `app/chat/service/chat_service.py` |
| Identidade e Validacao | Localizar usuario, validar credencial, confirmar o canal e verificar a consistencia da solicitacao. | `app/servicos/usuario/*`, `app/servicos/validacao_identidade/*`, `app/servicos/verificacao_solicitacao/*` |
| Conversa e Historico | Manter conversa atual, registrar mensagens e recuperar historico de interacoes do usuario. | `app/chat/model.py`, `app/chat/service/chat_service.py`, `app/chat/repository/*`, `app/chat/messages/*` |

## 3. Linguagem Ubiqua

O termo escolhido foi `usuario`, porque ele aparece nos tres subdominios e muda de significado conforme o contexto de negocio.

| Contexto | Significado de "usuario" |
|---|---|
| Orquestracao de Atendimento | Pessoa que inicia o atendimento, envia a mensagem e recebe a resposta final. |
| Identidade e Validacao | Titular da credencial que deve ser localizado, autenticado e autorizado para seguir no fluxo. |
| Conversa e Historico | Proprietario da conversa e dos registros associados, com acesso restrito ao proprio historico. |

## 4. Context Map

O diagrama C4 foi registrado em Drawio em [docs/img/Mapa-Contexto-C4.drawio](img/Mapa-Contexto-C4.drawio).

| Origem | Destino | Padrao de relacionamento | Leitura do relacionamento |
|---|---|---|---|
| Canal do usuario | Orquestracao de Atendimento | Customer/Supplier | O canal consome o fluxo orquestrado e recebe o retorno final. |
| Orquestracao de Atendimento | Identidade e Validacao | Customer/Supplier | A orquestracao depende da validacao para permitir a continuidade do atendimento. |
| Orquestracao de Atendimento | Conversa e Historico | Customer/Supplier | A orquestracao depende do contexto de conversa para registrar e recuperar interacoes. |

## 5. Proposta de Microservicos

| Microservico | Responsabilidade | Bounded Context principal |
|---|---|---|
| ServicoOrquestracaoAtendimento | Coordenar o atendimento completo, chamar validacoes e consolidar a resposta final. | Orquestracao de Atendimento |
| ServicoIdentidadeValidacao | Localizar usuario, validar credencial e verificar a consistencia da solicitacao. | Identidade e Validacao |
| ServicoConversaHistorico | Criar conversa, registrar mensagens e recuperar o historico do usuario. | Conversa e Historico |

Os servicos existentes no repositorio podem ser vistos como partes internas do microservico de Identidade e Validacao: `ServicoUsuario`, `ServicoValidacaoIdentidade` e `ServicoVerificacaoSolicitacao`. O componente de chat atual (`app/chat/*`) representa o nucleo de Conversa e Historico.

## 6. Evolucao do servico SOA

O servico escolhido para evolucao foi o `ServicoValidacaoIdentidade`, por ser um ponto sensivel do fluxo e por exigir separacao clara entre autenticacao, validacao de entrada e orquestracao.

### Antes

No desenho SOA, a validacao aparecia como uma utilidade isolada, com pouca delimitacao entre identidade, regra de entrada e decisao de continuidade do atendimento.

### Depois

Na evolucao guiada por DDD, o que antes era tratado como uma unica responsabilidade passa a ser dividido em tres contextos coerentes:

1. `Identidade e Validacao` trata usuario, credencial e aceitacao da solicitacao.
2. `Orquestracao de Atendimento` decide o fluxo e integra as respostas dos contextos.
3. `Conversa e Historico` preserva o historico sem contaminar a regra de identidade.

### Ajustes de responsabilidade

| Responsabilidade | Mantida no contexto de Identidade e Validacao | Movida para outro contexto |
|---|---|---|
| Localizacao do usuario | Sim | Nao |
| Validacao de credencial | Sim | Nao |
| Verificacao de conteudo minimo | Sim | Nao |
| Controle de fluxo do atendimento | Nao | Orquestracao de Atendimento |
| Persistencia de conversa | Nao | Conversa e Historico |

### Integracao com outros contextos

O contexto de Identidade e Validacao passa a ser consumido pela orquestracao como fornecedor especializado. Isso reduz acoplamento, simplifica testes e permite evolucao independente dos tres subdominios sem espalhar regras de autenticacao pelo restante do sistema.
