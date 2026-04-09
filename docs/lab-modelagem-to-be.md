# Lab de Modelagem TO-BE (BPMN) — AgentIA

## 1. Processo de Negócio Selecionado

**Processo:** Atendimento de Mensagem no Chat com Agente Especializado.

**Motivo da escolha:** o processo possui múltiplas etapas, decisões de fluxo, manipulação de dados (conversa/mensagens/configuração), regras de negócio e integração externa com provedor de LLM.

**Escopo:** do envio da mensagem pelo usuário até o retorno da resposta e persistência do histórico.

---

## 2. Diagrama BPMN TO-BE

![Diagrama BPMN TO-BE](img/Diagrama%20BPMN%20TO-BE.png)

As tarefas abaixo representam o fluxo operacional do processo TO-BE e devem estar refletidas no diagrama (incluindo início pelo usuário e resposta final ao usuário).

### 2.1 Descrição das Tarefas do Processo

| ID | Tarefa | Descrição |
|---|---|---|
| T01 | Enviar mensagem ao atendimento | O usuário inicia o processo enviando sua solicitação no chat para o agente escolhido. |
| T02 | Confirmar identificação do usuário | O sistema confirma se o usuário pode utilizar o atendimento. Em caso negativo, o processo é encerrado com orientação adequada. |
| T03 | Verificar dados mínimos da solicitação | O sistema verifica se a mensagem possui conteúdo mínimo para prosseguir. Em caso de inconsistência, solicita correção ao usuário. |
| T04 | Identificar conversa em andamento | O sistema verifica se o atendimento continua uma conversa existente ou se deve iniciar uma nova conversa. |
| T05 | Registrar solicitação no histórico | O sistema registra a mensagem do usuário para manter rastreabilidade do atendimento. |
| T06 | Encaminhar solicitação ao agente especializado | O sistema envia a solicitação para processamento do agente responsável pelo tema. |
| T07 | Receber resposta do agente | O sistema recebe a resposta gerada pelo agente especializado. |
| T08 | Tratar indisponibilidade de atendimento | Se o agente estiver indisponível, o sistema informa a situação e orienta o usuário a tentar novamente. |
| T09 | Registrar resposta no histórico | O sistema registra a resposta no histórico da conversa, mantendo o contexto completo. |
| T10 | Apresentar resposta ao usuário | O sistema retorna ao usuário uma resposta final (conteúdo gerado ou mensagem de indisponibilidade), encerrando o ciclo da solicitação. |

---

## 3. Regras de Negócio (RN)

- **RN01:** Somente usuários identificados podem iniciar e continuar atendimentos no chat.
- **RN02:** Toda solicitação deve conter uma mensagem com conteúdo mínimo para análise; mensagens vazias não são aceitas.
- **RN03:** Cada conversa pertence a um único usuário e não pode ser compartilhada com outros usuários.
- **RN04:** Quando não houver conversa em andamento, o sistema deve abrir uma nova conversa automaticamente.
- **RN05:** Toda interação deve registrar a solicitação do usuário e a respectiva resposta do atendimento.
- **RN06:** O usuário deve sempre receber um retorno final da solicitação, seja resposta do agente ou aviso de indisponibilidade.
- **RN07:** O histórico de conversa deve ser consultado apenas pelo usuário proprietário da conversa.
- **RN08:** Em indisponibilidade do atendimento especializado, o sistema deve informar o motivo de forma clara e orientar nova tentativa.

---

## 4. Diagrama de Casos de Uso (UML)

![Diagrama de Casos de Uso](img/Diagrama%20de%20casos%20de%20uso.png)

### 4.1 Consistência com o Processo TO-BE

- **UC Enviar mensagem ao agente** corresponde às tarefas **T01, T02 e T03**.
- **UC Processar solicitação no atendimento** corresponde às tarefas **T04, T05, T06 e T07**.
- **UC Tratar indisponibilidade** corresponde à tarefa **T08**.
- **UC Manter histórico da conversa** corresponde à tarefa **T09**.
- **UC Exibir resposta ao usuário** corresponde à tarefa **T10**.

---

## 5. Requisitos Não Funcionais (RNF)

- **RNF01 (Segurança):** Todas as rotas de chat devem exigir autenticação por identificador de usuário e rejeitar acessos não autorizados com HTTP 401.
- **RNF02 (Segurança):** O sistema deve usar JWT como método de criptografia/assinatura do token de autenticação, validando o token em todas as rotas protegidas do chat.
- **RNF03 (Validação):** O sistema deve rejeitar payloads inválidos com mensagens padronizadas de erro e código HTTP apropriado, sem executar persistência parcial da operação.
- **RNF04 (Confiabilidade):** O sistema deve garantir persistência atômica da conversa por operação de atualização (`upsert`) para evitar perda de histórico.
- **RNF05 (Interoperabilidade):** A integração com provedores de IA deve ser feita por API HTTP padronizada com payload JSON, permitindo troca de provedor com baixo impacto.
