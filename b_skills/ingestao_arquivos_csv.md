# Ingestão de Arquivos e CSV

## Metadados
- **id:** `de.skill.ingestao_arquivos_csv`
- **versão:** `1.0.0`
- **categoria:** ingestão
- **objetivo:** Orientar ingestão idempotente de CSV, TSV, JSON, JSON Lines, Parquet, Avro, ORC, XML quando necessário, diretórios, arquivos compactados e Delta Lake.
- **entrada esperada:** Descrição da origem, caminho, formato, schema esperado, modo de carga e política de erros.
- **saída esperada:** Plano de leitura, validações, metadados mínimos, política de quarentena e cuidados de idempotência.
- **parâmetros:** `source_path`, `format`, `schema`, `mode`, `encoding`, `delimiter`, `checkpoint`, `quarantine_path`.
- **validações:** Existência da origem, formato permitido, encoding, schema obrigatório quando houver risco de inferência instável, volume lido, volume rejeitado e checksum quando disponível.
- **dependências:** Tool de arquivo, Spark ou Python local conforme volume e formato.
- **exceções:** Origem ausente, schema incompatível, encoding inválido, linha corrompida, arquivo vazio, timeout ou permissão negada.
- **retry:** Aplicar retry apenas para falhas transitórias de I/O; falha de schema deve ser tratada por quarentena ou decisão explícita.
- **idempotência:** Usar identificador de execução, checkpoint, controle de partição/destino e evitar reprocessar o mesmo lote sem política.
- **efeitos colaterais:** Pode gerar metadados, logs e arquivos de rejeição quando executada por uma tool.
- **limitações:** Esta skill documenta o comportamento; execução real depende de tools registradas.
- **testes:** `e_tests/test_artifact_catalogs.py`.
- **agentes consumidores:** `de.ingestion.agent`, `de.files.agent`, `de.orchestrator.agent`.
- **origem:** Implementação original baseada em requisitos do prompt mestre e referências conceituais open source.
- **licença:** Mesma licença do repositório.

## Procedimento
1. Classifique a fonte como arquivo único, diretório, object storage, stream de arquivos ou tabela Delta.
2. Defina o formato explicitamente quando possível; use detecção apenas como apoio e registre evidência.
3. Exija schema explícito em produção para CSV, JSON e fontes com evolução instável.
4. Configure opções críticas: encoding, delimitador, header, quote, escape, multiline e modo de linhas corrompidas.
5. Registre origem, horário, tamanho, quantidade de arquivos, linhas lidas, linhas válidas e linhas rejeitadas.
6. Direcione registros inválidos para quarentena com motivo, lote, arquivo, linha quando disponível e regra violada.
7. Defina saída preferencial em formato colunar para camadas processadas.

## Guardrails
- Não descartar colunas ou linhas silenciosamente.
- Não usar inferência automática repetitiva em produção sem justificativa.
- Não fazer overwrite de destino sem política explícita.
- Não registrar dados sensíveis de linhas rejeitadas em logs.

## Exemplo de uso
Pergunta: "Planeje a ingestão de arquivos CSV diários para Bronze."

Resposta esperada: indicar schema explícito, validação de encoding/delimitador, checkpoint por data/arquivo, quarentena de linhas inválidas, metadados de execução e escrita idempotente na zona Bronze.
