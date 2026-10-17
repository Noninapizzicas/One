# Convención de SKILL.md compartido

Formato mínimo que ambos (Hermes y Claude Code/ECC) saben leer:

```yaml
---
name: nombre-del-skill
description: "Una línea describiendo cuándo invocarlo."
version: 0.1.0
license: MIT
# --- opcional: metadata específica de cada agente ---
metadata:
  hermes:
    tags: [Productivity, Automation]
  claude-code:
    model: sonnet
    tools: [Read, Grep, Glob, Bash]
---

# Título legible del skill

Descripción humana.

## When to Use

- Caso 1
- Caso 2

## Procedure

### 1. Paso uno
Descripción…

### 2. Paso dos
…
```

## Reglas

1. `name` y `description` son **obligatorios**.
2. El bloque `metadata.hermes` sólo lo lee Hermes.
3. El bloque `metadata.claude-code` sólo lo lee Claude Code / ECC.
4. Las secciones `## When to Use` y `## Procedure` son recomendadas por ambos.
5. Un `SKILL.md` vive en `skills/<nombre-del-skill>/SKILL.md`.
