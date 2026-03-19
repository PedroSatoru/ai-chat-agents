# Lab de Modelagem TO-BE (BPMN) — AgentIA

## 1. Processo de Negócio Selecionado

**Processo:** Atendimento de Mensagem no Chat com Agente Especializado.

**Motivo da escolha:** o processo possui múltiplas etapas, decisões de fluxo, manipulação de dados (conversa/mensagens/configuração), regras de negócio e integração externa com provedor de LLM.

**Escopo:** do envio da mensagem pelo usuário até o retorno da resposta e persistência do histórico.

---

## 2. Diagrama BPMN TO-BE

![Diagrama BPMN TO-BE](img/Diagrama%20BPMN%20TO-BE.png)

### 2.1 Descrição das Tarefas do Processo

| ID | Tarefa | Descrição |
|---|---|---|
| T01 | Receber requisição de envio | O sistema recebe a chamada de envio de mensagem e identifica usuário, conversa e parâmetros da interação. |
| T02 | Validar autenticação | O sistema valida o identificador/autenticação do usuário antes de permitir o processamento do fluxo. |
| T03 | Validar payload | O sistema valida campos obrigatórios, limites e formato dos parâmetros de envio da mensagem. |
| T04 | Definir conversation_id | O sistema reutiliza o chat_id informado ou cria um novo identificador único para a conversa. |
| T05 | Consultar conversa atual | O sistema busca a conversa do usuário para continuar um histórico existente ou iniciar um novo. |
| T06 | Criar conversa inicial | Quando não há conversa prévia, o sistema cria o documento inicial com metadados e estrutura de mensagens. |
| T07 | Registrar mensagem do usuário | A mensagem enviada é registrada no histórico da conversa com seus metadados de contexto. |
| T08 | Montar prompt final para IA | O sistema compõe o conteúdo final para inferência unindo contexto, especialidade do agente e mensagem atual. |
| T09 | Chamar provedor de LLM | O sistema envia a requisição ao provedor externo de IA e aguarda retorno da resposta gerada. |
| T10 | Registrar resposta e persistir conversa | O sistema grava a resposta do assistente, atualiza a conversa e retorna o resultado ao cliente. |

---

## 3. Regras de Negócio (RN)

- **RN01:** Toda requisição de envio de mensagem deve conter `x-user-id` válido.
- **RN02:** O campo `prompt` é obrigatório e não pode ser vazio.
- **RN03:** `temperature` deve estar no intervalo de $0.0$ a $1.0$; valores válidos são normalizados para 1 casa decimal.
- **RN04:** Se `chat_id` não for informado, o sistema deve gerar um novo `conversation_id` único.
- **RN05:** O histórico de conversa só pode ser acessado pelo mesmo `user_id` dono da conversa.
- **RN06:** Se a conversa não existir, deve ser criada com título padrão "Nova conversa" quando não houver título informado.
- **RN07:** Cada envio deve registrar duas entradas no histórico: mensagem do usuário e resposta do assistente.
- **RN08:** Em falha de integração com LLM, a operação deve retornar erro técnico sem quebrar consistência dos dados já persistidos.

---

## 4. Diagrama de Casos de Uso (UML)

![Diagrama de Casos de Uso](img/Diagrama%20de%20casos%20de%20uso.png)

---

## 5. Requisitos Não Funcionais (RNF)

- **RNF01 (Segurança):** Todas as rotas de chat devem exigir autenticação por identificador de usuário e rejeitar acessos não autorizados com HTTP 401.
- **RNF02 (Segurança):** O sistema deve usar JWT como método de criptografia/assinatura do token de autenticação, validando o token em todas as rotas protegidas do chat.
- **RNF03 (Validação):** O sistema deve rejeitar payloads inválidos com mensagens padronizadas de erro e código HTTP apropriado, sem executar persistência parcial da operação.
- **RNF04 (Confiabilidade):** O sistema deve garantir persistência atômica da conversa por operação de atualização (`upsert`) para evitar perda de histórico.
- **RNF05 (Interoperabilidade):** A integração com provedores de IA deve ser feita por API HTTP padronizada com payload JSON, permitindo troca de provedor com baixo impacto.
