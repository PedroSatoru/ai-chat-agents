
# 1️⃣ Identificação de Pontos de Reuso no Sistema

O projeto é fortemente baseado em componentes já consolidados no mercado. Os principais pontos de reuso identificados são:

## 🔹 1.1 Framework Web

* **FastAPI**

  * Exposição de endpoints REST
  * Validação automática com Pydantic
  * Geração automática de documentação (Swagger/OpenAPI)
  * Middleware e sistema de dependências reutilizável

✔ Reuso direto de infraestrutura HTTP, validação, serialização e documentação.

---

## 🔹 1.2 Autenticação e Segurança

* **JWT (JSON Web Token)**

  * Biblioteca padrão para geração e validação de tokens
  * Mecanismo reutilizável e amplamente adotado
* Bibliotecas de hash/criptografia para armazenar API Keys

  * Ex: `passlib`, `bcrypt`, `cryptography`

✔ Reuso de padrões consolidados de autenticação stateless.

---

## 🔹 1.3 Integração com LLMs

* **OpenRouter API**

  * Gateway único para múltiplos provedores (OpenAI, Claude, Gemini, etc.)
  * Abstração pronta para evitar múltiplas integrações diretas

✔ Reuso de:

* Infraestrutura de roteamento entre modelos
* Padronização de requisições
* Atualizações e compatibilidade mantidas externamente

---

## 🔹 1.4 Persistência de Dados

### ✔ Banco Relacional

* **PostgreSQL (via Supabase)**

  * Banco relacional pronto
  * Infraestrutura gerenciada
  * Pooler de conexão

### ✔ ORM

* **SQLAlchemy**

  * Mapeamento objeto-relacional
  * Abstração de queries
  * Independência parcial de banco

### ✔ Migrations

* **Alembic**

  * Versionamento de schema
  * Geração automática de scripts

### ✔ Banco NoSQL

* **MongoDB**

  * Armazenamento flexível de chats
  * Modelo orientado a documento

### ✔ Banco Vetorial

* **ChromaDB**

✔ Reuso de motores especializados para busca vetorial e RAG.

---

## 🔹 1.5 Embeddings

* Uso de modelos de embedding via:

  * OpenRouter (indiretamente)
  * Ou bibliotecas locais integráveis

✔ Reuso de modelos já treinados (sem necessidade de treinar embeddings próprios).

---

# 2️⃣ Levantamento de Frameworks, Bibliotecas e APIs Reutilizáveis

Abaixo, a consolidação dos artefatos reutilizáveis identificados:

| Categoria      | Ferramenta        | Tipo             | Finalidade                          |
| -------------- | ----------------- | ---------------- | ----------------------------------- |
| Framework Web  | FastAPI           | Framework        | Exposição de API REST               |
| Validação      | Pydantic          | Biblioteca       | Validação e serialização            |
| Autenticação   | JWT (python-jose) | Biblioteca       | Geração/validação de tokens         |
| Hash de senha  | passlib / bcrypt  | Biblioteca       | Segurança de credenciais            |
| ORM            | SQLAlchemy        | Biblioteca       | Mapeamento relacional               |
| Migration      | Alembic           | Ferramenta       | Controle de versionamento de schema |
| Banco SQL      | PostgreSQL        | SGBD             | Dados relacionais                   |
| Banco NoSQL    | MongoDB           | SGBD             | Histórico de chats                  |
| Vetor DB       | ChromaDB          | Banco vetorial   | Embeddings e RAG                    |
| LLM Gateway    | OpenRouter        | API Externa      | Acesso a múltiplos LLMs             |
| Infraestrutura | Supabase          | BaaS             | Postgres gerenciado                 |

