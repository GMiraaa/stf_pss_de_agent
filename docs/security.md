# Segurança

## Credenciais

- Não incluir senhas, tokens, chaves privadas ou strings completas de conexão no código.
- Usar variáveis de ambiente ou secret manager quando disponível.
- `.env` real não deve ser versionado.

## Operações destrutivas

Operações como `DROP`, `TRUNCATE`, `DELETE`, overwrite, vacuum agressivo e alteração destrutiva de schema exigem confirmação ou política explícita.

A tool `executar_sqlite` bloqueia comandos destrutivos e multi-statement. Sem `allow_write=True`, apenas `SELECT`, `WITH` e `PRAGMA` são aceitos.

## MCP

- Conectar apenas MCPs confiáveis.
- Restringir roots/diretórios e permissões ao mínimo necessário.
- Documentar ferramentas read/write/destrutivas antes de habilitar.
- Não permitir shell arbitrário sem guardrails.

## Logging

Logs devem conter execução, pipeline, etapa, ambiente, status, duração, volumes e erro técnico. Não devem conter credenciais, dados pessoais desnecessários nem payloads sensíveis completos.

## Dependências

Antes de instalar nova dependência, verificar licença, manutenção, CVEs, telemetria, permissões e necessidade real.
