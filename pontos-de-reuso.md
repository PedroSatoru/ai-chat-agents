# Linguagens e Frameworks utilizados

* **Python**
* **FastAPI**
* **PostgreSQL**
* **MongoDB**
* **ChromaDB**

---

# Arquitetura Geral

A arquitetura foi projetada com foco em **modularidade, segurança e reuso de software**, adotando uma abordagem baseada em serviços especializados e múltiplos modelos de persistência (*polyglot persistence*).

O sistema é composto por uma **API desenvolvida em Python com FastAPI**, responsável por:

* Expor endpoints REST
* Autenticar usuários via JWT
* Intermediar requisições para múltiplos modelos de LLM por meio do OpenRouter

A aplicação utiliza diferentes bancos de dados conforme a natureza da informação:

* **PostgreSQL (via Supabase)** → dados relacionais
* **MongoDB** → histórico de chats
* **ChromaDB** → armazenamento vetorial e embeddings

Essa arquitetura separa responsabilidades por tipo de dado, reduz acoplamento e permite que cada tecnologia seja utilizada de acordo com sua especialidade.

---

# Justificativa das Tecnologias Utilizadas

## Backend – Python com FastAPI

O **FastAPI** foi escolhido por ser um framework moderno, performático e altamente produtivo para construção de APIs REST.

Ele oferece:

* Validação automática com Pydantic
* Geração automática de documentação (Swagger/OpenAPI)
* Sistema de dependências reutilizável
* Alto desempenho baseado em ASGI

Do ponto de vista arquitetural, o FastAPI favorece organização modular do código, clareza nos contratos de API e reaproveitamento de componentes internos (schemas, dependências, middlewares).

---

## Autenticação – JWT

A autenticação é baseada em **JWT (JSON Web Token)**, utilizando bibliotecas consolidadas do ecossistema Python.

Essa abordagem permite:

* Autenticação stateless
* Baixo acoplamento entre autenticação e persistência
* Escalabilidade sem necessidade de armazenar sessão no servidor

Além disso, a **API Key do OpenRouter é armazenada de forma segura (hash/criptografia)**, seguindo boas práticas de segurança.

---

## Integração com LLMs – OpenRouter

O **OpenRouter** foi adotado como gateway único para múltiplos modelos de linguagem (OpenAI, Claude, Gemini, entre outros).

Essa escolha representa um forte reuso de infraestrutura externa, pois:

* Evita múltiplas integrações diretas com cada provedor
* Padroniza requisições
* Centraliza compatibilidade e atualizações

Arquiteturalmente, isso reduz complexidade e facilita a troca ou adição de novos modelos no futuro.

---

## Banco de Dados Relacional – PostgreSQL (Supabase)

O **PostgreSQL** é utilizado para armazenar dados estruturados, como usuários e credenciais.

Sua utilização via **Supabase** caracteriza reuso de infraestrutura gerenciada, oferecendo:

* Alta disponibilidade
* Pool de conexões
* Segurança integrada
* Redução de esforço operacional

O versionamento do schema é feito com **Alembic**, garantindo controle evolutivo do banco de dados.

---

## Banco NoSQL – MongoDB

O **MongoDB** é utilizado para armazenar o histórico de chats, que possui estrutura flexível e pode variar ao longo do tempo.

A escolha do modelo orientado a documentos permite:

* Armazenar mensagens e metadados de forma natural
* Evitar modelagem relacional complexa para dados conversacionais
* Maior flexibilidade de evolução

---

## Banco Vetorial – ChromaDB

Para armazenamento de embeddings e suporte a **RAG (Retrieval-Augmented Generation)**, a aplicação utiliza um banco vetorial executado localmente (**ChromaDB**).

Essa escolha possibilita:

* Busca semântica eficiente
* Armazenamento de preferências e informações contextuais do usuário
* Independência de serviços externos pagos

---

# Reuso de Artefatos

O projeto aplica reuso de software em múltiplos níveis:

* **Reuso de Frameworks:** FastAPI, SQLAlchemy e bibliotecas de autenticação evitam desenvolvimento do zero.
* **Reuso de Serviços Gerenciados:** Supabase fornece PostgreSQL como serviço.
* **Reuso de APIs Externas:** OpenRouter centraliza acesso a diversos LLMs.
* **Reuso de Motores Especializados:** MongoDB, Redis e bancos vetoriais são utilizados conforme sua especialidade.
* **Reuso de Modelos Pré-Treinados:** Embeddings e LLMs já treinados são utilizados, eliminando a necessidade de treinamento próprio.

Essa estratégia reduz complexidade, melhora a qualidade do sistema e acelera o desenvolvimento.
