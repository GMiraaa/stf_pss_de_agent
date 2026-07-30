# STF PSS — Data Engineering Agent

Agente de IA especializado em **Engenharia de Dados** com arquitetura extensível por **skills**, **ferramentas**, catálogos e workflows documentados.
O agente usa o padrão ReAct (Raciocínio + Ação) sobre o **Gemini 2.5 Flash** e cresce gradualmente à medida que novas skills de domínio são adicionadas.

O escopo deste repositório é Data Engineering: ingestão, ETL/ELT, PySpark/Spark, qualidade, profiling técnico, Delta Lake, Lakehouse, contratos, batch, streaming, observabilidade, bancos, MCP e entrega técnica de dados. Dashboards executivos, storytelling de negócio e modelagem preditiva avançada pertencem aos repositórios de Data Analytics ou Data Science.

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
├── docs/                           # Catálogos, pesquisa, decisões e matriz de cobertura
│   ├── agent_catalog.md
│   ├── skill_catalog.md
│   ├── workflow_catalog.md
│   ├── requirements_coverage.md
│   ├── research_report.md
│   ├── sources_and_licenses.md
│   ├── decisions.md
│   ├── security.md
│   ├── observability.md
│   └── limitations.md
│
├── workflows/                      # Espaço para workflows executáveis futuros
│   └── README.md
│
├── f_vscode_extension/             # Chat participant do VS Code
│   ├── src/extension.ts            # Lógica da extensão (TypeScript)
│   ├── package.json
│   └── tsconfig.json
│
├── main.py                         # Chat interativo no terminal
├── main_api.py                     # Servidor HTTP (usado pelo VS Code)
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
# Edite .env e insira sua GOOGLE_API_KEY
```

---

## Uso

### Terminal (simples)

```bash
python main.py
```

### Chat do VS Code (recomendado)

O agente aparece no chat do VS Code como `@de-agent`. **Instale a extensão uma única vez:**

```bash
cd f_vscode_extension
npm install
npm run package           # gera stf-de-agent-0.1.0.vsix
code --install-extension stf-de-agent-0.1.0.vsix
```

> Requisito: Node.js 18+ instalado.

Depois é só usar o chat (`Ctrl+Alt+I`). A extensão gerencia o servidor automaticamente:

| Comando | Ação |
|---|---|
| `@de-agent /start` | Instala dependências e inicia o servidor |
| `@de-agent /stop` | Encerra o servidor |
| `@de-agent /reset` | Limpa o histórico da conversa |
| `@de-agent <pergunta>` | Conversa com o agente |

---

## Adicionando uma nova Skill

Skills são arquivos **Markdown** em `b_skills/`. O agente carrega todos os `.md` do diretório automaticamente na inicialização — nenhuma linha de código é necessária.

As skills atuais cobrem:

| Skill | Finalidade |
|---|---|
| `engenharia_dados_basico.md` | Fundamentos e limites de escopo |
| `ingestao_arquivos_csv.md` | Ingestão de arquivos, CSV, schema, encoding e quarentena |
| `etl_elt_pyspark.md` | ETL/ELT, PySpark, batch/incremental e performance Spark |
| `qualidade_observabilidade.md` | Qualidade, profiling técnico, estatística operacional e observabilidade |
| `lakehouse_delta_schema_contracts.md` | Lakehouse, Delta Lake, schemas e contratos |
| `integracao_bancos_mcp_entrega.md` | Bancos, APIs, MCP e entrega técnica para consumo |
| `batch_streaming_orquestracao.md` | Batch, streaming, checkpoint, backfill e orquestração |

O contrato mínimo de metadados das skills está em [docs/skill_catalog.md](docs/skill_catalog.md).

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

Ferramentas registradas atualmente:

| Tool | Finalidade | Guardrails |
|---|---|---|
| `buscar_informacao` | Busca mock de conhecimento interno | Não acessa fonte externa real |
| `validar_csv` | Valida CSV local, schema simples, contagens e rejeições | Não descarta dados; reporta erros |
| `executar_sqlite` | Executa SQL parametrizado em SQLite local | Bloqueia SQL destrutivo e escrita por padrão |
| `perfil_csv_pyspark` | Perfil técnico de CSV com Spark local opcional | Importa PySpark somente quando chamado |

---

## Workflows executáveis

### CSV para Bronze local

```bash
python3 -m workflows.csv_to_bronze \
  --source-path examples/input.csv \
  --output-dir data/bronze/input \
  --schema '{"id":"integer","nome":"string","valor":"float"}'
```

Gera `data.jsonl`, `quarantine.jsonl` e `metadata.json` de forma atômica.

### SQLite incremental para CSV

```bash
python3 -m workflows.sqlite_incremental_to_csv \
  --database-path data/source.db \
  --query "select id, updated_at, amount from events where updated_at > ? order by updated_at" \
  --output-path data/export/events.csv \
  --state-path data/state/events.json \
  --watermark-column updated_at
```

Mantém watermark em arquivo de estado JSON.

---

## Testes

```bash
pytest e_tests/ -v
```

Os testes atuais validam a integridade dos catálogos, metadados das skills, tools de CSV/SQLite e workflows locais com datasets sintéticos. PySpark é validado como dependência opcional: se não estiver instalado, a tool falha com mensagem acionável.

---

## Catálogos e rastreabilidade

- [Catálogo de agentes](docs/agent_catalog.md)
- [Catálogo de skills](docs/skill_catalog.md)
- [Catálogo de workflows](docs/workflow_catalog.md)
- [Matriz de cobertura](docs/requirements_coverage.md)
- [Relatório da pesquisa](docs/research_report.md)
- [Fontes e licenças](docs/sources_and_licenses.md)
- [Decisões arquiteturais](docs/decisions.md)
- [Segurança](docs/security.md)
- [Observabilidade](docs/observability.md)
- [Limitações](docs/limitations.md)

Nenhum código, prompt ou documentação de terceiros foi copiado para este repositório. As fontes open source pesquisadas foram usadas como referência conceitual e estão registradas em `docs/sources_and_licenses.md`.

---

## Variáveis de ambiente

| Variável         | Obrigatória | Padrão              | Descrição                               |
|------------------|-------------|---------------------|-----------------------------------------|
| `GOOGLE_API_KEY` | Sim         | —                   | Chave de API do Google AI Studio        |
| `MODEL`          | Não         | `gemini-2.5-flash`  | Modelo Gemini                           |
| `TEMPERATURE`    | Não         | `0.2`               | Temperatura de geração (0–2)            |
| `MAX_ITERATIONS` | Não         | `10`                | Máximo de iterações do loop ReAct       |

---

## Licença

Veja [LICENSE](LICENSE).
