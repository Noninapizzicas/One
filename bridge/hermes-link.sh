#!/usr/bin/env bash
# Conecta Hermes a la carpeta common skills/ de este repo.
# Añade la variable a tu shell rc file (bashrc / zshrc).

set -euo pipefail

ONE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$ONE_ROOT/skills"

echo "export HERMES_OPTIONAL_SKILLS=\"$SKILLS_DIR\""
echo ""
echo "# Añade la línea anterior a ~/.bashrc o ~/.zshrc y recarga:"
echo "#   source ~/.bashrc"
echo "#"
echo "# Luego verifica:"
echo "#   hermes skills"
