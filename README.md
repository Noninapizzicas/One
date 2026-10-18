# One — Puente de agentes

Repo-puente que permite a **Hermes Agent** (Nous Research) y a **Claude Code
+ ECC** compartir las mismas skills y subagentes. Una sola fuente de verdad,
dos interfaces.

## Estructura

```
One/
├── skills/                   # Skills en formato SKILL.md (fuente única)
├── agents/                   # Subagentes formato ECC/Claude Code
├── bridge/                   # Scripts de conexión
├── scripts/
│   └── import-from-ecc.py    # Trae skills/agents desde el fork de ECC
└── docs/
    └── SKILL-FORMAT.md       # Convención del frontmatter compartido
```

## Cómo funciona realmente

### Hermes

Hermes busca skills en `~/.hermes/skills/`. Para que vea las de este repo
**sin duplicar**, se crean symlinks:

```bash
ln -s ~/One/skills/<skill-name>  ~/.hermes/skills/<skill-name>
ln -s ~/One/agents/<agent>.md    ~/.hermes/skills/<agent>/SKILL.md
```

> ⚠️ La variable `HERMES_OPTIONAL_SKILLS` **NO** alimenta `hermes skills list`.
> Solo sirve al sistema de Hub (skills opcionales empaquetadas). Los
> symlinks a `~/.hermes/skills/` son el camino correcto.

### Claude Code + ECC

Claude Code lee skills de `~/.claude/skills/`. El script
`bridge/claude-code-link.sh` crea los symlinks equivalentes.

## Setup

### 1. Clonar

```bash
git clone https://github.com/Noninapizzicas/One.git ~/One
cd ~/One
git checkout ccr-cb23ee59-r8t4pg
```

### 2. Importar skills desde ECC (opcional)

Requiere tener el fork de ECC clonado:

```bash
# En el VPS/máquina
git clone https://github.com/Noninapizzicas/ecc.git ~/ecc

# Importar algunos skills
cd ~/One
python3 scripts/import-from-ecc.py --only code-reviewer
python3 scripts/import-from-ecc.py --only agentic-engineering
# ... o sin --only para importar todos
```

### 3. Conectar a Hermes

Crea los symlinks (uno por skill/agent):

```bash
for d in ~/One/skills/*/; do
  name=$(basename "$d")
  ln -sfn "$d" ~/.hermes/skills/"$name"
done

# Para los agents (Hermes espera SKILL.md en una carpeta)
for f in ~/One/agents/*.md; do
  name=$(basename "$f" .md)
  mkdir -p ~/.hermes/skills/"$name"
  ln -sfn "$f" ~/.hermes/skills/"$name"/SKILL.md
done
```

Verifica:

```bash
hermes skills list | grep -E "agentic|code-review|coding-standards"
```

### 4. Conectar a Claude Code (opcional)

```bash
./bridge/claude-code-link.sh
```

## Demo verificado — 2026-10-18

End-to-end probado desde Telegram con el modelo gratuito `upstage/solar-mini4:free`
vía Nous Portal:

**Pedido** (desde Telegram, celular):
> Usa el skill `code-reviewer` para revisar este código Python...
> (snippet con `TypeError` y `ZeroDivisionError`)

**Respuesta** (Hermes aplicó el checklist completo del skill):
- Pre-Report Gate aplicado
- 2 bugs HIGH identificados con línea y causa
- Fixes propuestos con código ejecutable
- Sección "Seguridad" explícita
- Verdict final estructurado

Conclusión: el bridge funciona, el skill se invoca correctamente, y hasta
un modelo pequeño gratuito aplica bien skills bien escritas.

## Troubleshooting

| Síntoma | Causa probable | Solución |
|---|---|---|
| `hermes skills list` no muestra las skills del repo | Las skills no están en `~/.hermes/skills/` (o no vía symlink) | Crear symlinks como en Setup #3 |
| Editar `~/One/skills/X/SKILL.md` no se refleja | Hay copia en vez de symlink | `rm -rf ~/.hermes/skills/X && ln -s ~/One/skills/X ~/.hermes/skills/X` |
| Hermes carga pero no invoca el skill | El skill no tiene `name` + `description` en frontmatter | Ver `docs/SKILL-FORMAT.md` |

## Fuentes

- Hermes Agent: https://github.com/NousResearch/hermes-agent
- ECC: https://github.com/affaan-m/ecc
