# One — Puente de agentes

Repo-puente que permite a **Hermes Agent** (Nous Research) y a **Claude Code
+ ECC** compartir las mismas skills y subagentes.

## Qué contiene

- `skills/` — Skills en formato `SKILL.md` compatibles con ambos agentes.
- `agents/` — Subagentes de Claude Code (plugin ECC).
- `bridge/` — Scripts para enganchar cada agente a este repo.
- `scripts/import-from-ecc.py` — Importa skills y agents desde `../ecc`.
- `docs/SKILL-FORMAT.md` — Convención del frontmatter compartido.

## Setup rápido

### Hermes

```bash
./bridge/hermes-link.sh
```

Exporta `HERMES_OPTIONAL_SKILLS=/home/user/One/skills` en tu shell.

### Claude Code + ECC

```bash
./bridge/claude-code-link.sh
```

Crea symlinks `~/.claude/skills` → `/home/user/One/skills`
y `~/.claude/agents` → `/home/user/One/agents`.

## Primer caso de uso

Importar `code-reviewer` de ECC → disponible en Hermes vía Telegram.

```bash
python scripts/import-from-ecc.py --only code-reviewer
```
