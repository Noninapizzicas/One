# Bridge

Scripts que conectan cada agente a la carpeta común `skills/` + `agents/` de este repo.

| Agente | Script | Qué hace |
|---|---|---|
| Hermes | `hermes-link.sh` | Exporta `HERMES_OPTIONAL_SKILLS` apuntando a `../skills` |
| Claude Code + ECC | `claude-code-link.sh` | Crea symlinks desde `~/.claude/{skills,agents}` a este repo |

## Verificar

```bash
# Hermes
hermes skills   # debería listar los skills de este repo

# Claude Code (dentro de una sesión)
/skills         # debería mostrar los mismos skills
```
