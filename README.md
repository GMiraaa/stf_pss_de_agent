# STF PSS — Data Engineering Agent

Agente de IA especializado em **Engenharia de Dados** com arquitetura extensível por **skills** e **ferramentas**.
O agente usa o padrão ReAct (Raciocínio + Ação) sobre um LLM (padrão: `gpt-4o-mini`) e cresce gradualmente à medida que novas skills de domínio são adicionadas.

---

## Estrutura do projeto

```
stf_pss_de_agent/
│
├── a_agent/                        # Núcleo do agente (loop ReAct)
│   ├── __init__.py
│   └── agent.py                    # Classe Agent
│
├── b_skills/                       # Skills de domínio — apenas arquivos .md
│   └── engenharia_dados_basico.md  # Skill de exemplo
│
├── c_tools/                        # Ferramentas que o agente pode executar
│   ├── __init__.py
│   ├── base_tool.py                # Interface BaseTool
│   └── busca_informacao_tool.py    # Ferramenta de exemplo (mock)
│
├── d_config/                       # Configurações centralizadas
│   ├── __init__.py
│   └── settings.py                 # Lê variáveis do .env via Pydantic Settings
│
├── e_tests/                        # Testes automatizados
│   └── __init__.py                 # Testes do agente, skills e ferramentas
│
├── main.py                         # Ponto de entrada (chat interativo no terminal)
├── requirements.txt
├── .env.example                    # Modelo de variáveis de ambiente
└── .gitignore
```

---

## Pré-requisitos

- Python **3.11+**
- Chave de API do **Google AI Studio** — obtenha gratuitamente em [aistudio.google.com](https://aistudio.google.com/app/apikey)

---

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/stf_pss_de_agent.git
cd stf_pss_de_agent

# 2. Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite .env e insira sua OPENAI_API_KEY
```

---

## Uso

```bash
python main.py
```

O agente inicia um chat interativo no terminal:

```
============================================================
  STF PSS — Data Engineering Agent
  Digite 'sair' para encerrar | 'reset' para limpar contexto
============================================================

Você: O que é um Data Lakehouse?

Agente: Um Data Lakehouse combina...
```

---

## Adicionando uma nova Skill

Skills são arquivos **Markdown** em `b_skills/`. O agente carrega todos os `.md` do diretório automaticamente na inicialização — nenhuma linha de código é necessária.

1. Crie um arquivo em `b_skills/`, por exemplo `sql_avancado.md`:

```markdown
# SQL Avançado para Engenharia de Dados

## Window Functions
- `RANK()`, `ROW_NUMBER()`, `LAG()`, `LEAD()`

## Otimização
- Particionamento e clusterização de tabelas
- `EXPLAIN ANALYZE` para diagnóstico de queries
```

2. Reinicie o agente — a skill será carregada automaticamente.

---

## Adicionando uma nova Ferramenta

1. Crie um arquivo em `c_tools/`, por exemplo `executar_sql_tool.py`:

```python
from c_tools.base_tool import BaseTool

class ExecutarSqlTool(BaseTool):
    @property
    def name(self) -> str:
        return "executar_sql"

    @property
    def description(self) -> str:
        return "Executa uma query SQL em um banco de dados e retorna os resultados."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Query SQL a executar."}
            },
            "required": ["query"],
        }

    def run(self, query: str) -> str:
        # Implemente a conexão com o banco aqui
        ...
```

2. Registre a ferramenta em `main.py`:

```python
from c_tools.executar_sql_tool import ExecutarSqlTool

agent.register_tool(ExecutarSqlTool())
```

---

## Testes

```bash
pytest e_tests/ -v
```

---

## Variáveis de ambiente

| Variável         | Obrigatória | Padrão              | Descrição                               |
|------------------|-------------|---------------------|-----------------------------------------|
| `GOOGLE_API_KEY` | Sim         | —                   | Chave de API do Google AI Studio        |
| `MODEL`          | Não         | `gemini-1.5-flash`  | Modelo Gemini                           |
| `TEMPERATURE`    | Não         | `0.2`               | Temperatura de geração (0–2)            |
| `MAX_ITERATIONS` | Não         | `10`                | Máximo de iterações do loop ReAct       |

---

## Licença

Veja [LICENSE](LICENSE).

