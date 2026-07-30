# Decisões Arquiteturais

## ADR-001 - Preservar estrutura existente

Contexto: O projeto já separa agente, skills, tools, config e testes.

Decisão: Manter `a_agent/`, `b_skills/`, `c_tools/`, `d_config/` e `e_tests/`, adicionando `docs/` e `workflows/` para documentação e evolução.

Consequências: Menor risco de quebrar o carregamento automático de skills. A estrutura sugerida pelo prompt mestre fica representada por catálogos e pode evoluir gradualmente.

## ADR-002 - Não adotar framework multiagente externo agora

Contexto: CrewAI, LangChain, AutoGen e LlamaIndex são robustos, mas adicionam dependências e abstrações.

Decisão: Representar agentes como perfis documentados do agente ReAct atual, usando skills Markdown.

Consequências: O MVP permanece simples e executável. Uma migração futura deve ser motivada por necessidade real de roteamento, memória, runtime distribuído ou avaliação.

## ADR-003 - Usar fontes externas apenas como referência

Contexto: O prompt exige pesquisa e licença, mas a estrutura local é simples.

Decisão: Não copiar código/prompts/documentação de terceiros. Criar artefatos originais inspirados por práticas gerais e registrar fontes.

Consequências: Reduz risco de licença e propriedade intelectual. Exige implementação futura de tools quando houver ambiente e requisitos executáveis.

## ADR-004 - Estatística limitada a operação e qualidade

Contexto: O prompt pede estatística, outliers, correlação, A/B, clustering e previsão, mas o repositório é de Data Engineering.

Decisão: Documentar essas capacidades como apoio a profiling, observabilidade, drift, performance e capacity planning, não como Data Science.

Consequências: Mantém separação entre Data Engineering, Analytics e Science.
