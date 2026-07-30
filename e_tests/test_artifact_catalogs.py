from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "b_skills"
DOCS_DIR = ROOT / "docs"

REQUIRED_SKILL_FIELDS = [
    "id:",
    "versão:",
    "categoria:",
    "objetivo:",
    "entrada esperada:",
    "saída esperada:",
    "parâmetros:",
    "validações:",
    "dependências:",
    "exceções:",
    "retry:",
    "idempotência:",
    "efeitos colaterais:",
    "limitações:",
    "testes:",
    "agentes consumidores:",
    "origem:",
    "licença:",
]

CORE_DOCS = [
    "agent_catalog.md",
    "skill_catalog.md",
    "workflow_catalog.md",
    "requirements_coverage.md",
    "sources_and_licenses.md",
    "research_report.md",
    "decisions.md",
    "security.md",
    "observability.md",
    "limitations.md",
]

EXPECTED_AGENTS = [
    "de.orchestrator.agent",
    "de.ingestion.agent",
    "de.etl_elt.agent",
    "de.spark.agent",
    "de.quality.agent",
    "de.delta_lake.agent",
    "de.schema_contract.agent",
    "de.batch.agent",
    "de.streaming.agent",
    "de.observability.agent",
    "de.performance.agent",
    "de.lineage.agent",
    "de.database.agent",
    "de.files.agent",
    "de.delivery.agent",
]


def test_skills_have_required_metadata() -> None:
    skill_files = sorted(SKILL_DIR.glob("*.md"))
    assert skill_files, "Nenhuma skill Markdown encontrada em b_skills/"

    for skill_file in skill_files:
        content = skill_file.read_text(encoding="utf-8").lower()
        assert "## metadados" in content, f"{skill_file.name} não possui seção de metadados"
        missing = [field for field in REQUIRED_SKILL_FIELDS if field not in content]
        assert not missing, f"{skill_file.name} não possui campos: {missing}"


def test_core_docs_exist() -> None:
    for doc_name in CORE_DOCS:
        doc_path = DOCS_DIR / doc_name
        assert doc_path.exists(), f"Documento obrigatório ausente: {doc_name}"
        assert doc_path.read_text(encoding="utf-8").strip(), f"Documento vazio: {doc_name}"


def test_agent_catalog_lists_expected_agents() -> None:
    content = (DOCS_DIR / "agent_catalog.md").read_text(encoding="utf-8")
    missing = [agent_id for agent_id in EXPECTED_AGENTS if agent_id not in content]
    assert not missing, f"Agentes esperados ausentes do catálogo: {missing}"


def test_security_doc_mentions_guardrails() -> None:
    content = (DOCS_DIR / "security.md").read_text(encoding="utf-8").lower()
    for term in ["credenciais", "operações destrutivas", "mcp", "logging"]:
        assert term in content
