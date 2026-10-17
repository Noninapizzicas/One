#!/usr/bin/env bash
# Linkea las skills y agents compartidos a ~/.claude/
# Idempotente: salta si el symlink ya existe y apunta aquí.

set -euo pipefail

ONE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"

mkdir -p "$CLAUDE_HOME"

link_if_needed() {
  local src="$1"
  local dst="$2"
  if [[ -L "$dst" ]] && [[ "$(readlink "$dst")" == "$src" ]]; then
    echo "ok: $dst → $src (ya linkeado)"
    return
  fi
  if [[ -e "$dst" ]]; then
    echo "warn: $dst existe y no es nuestro symlink. Muévelo o bórralo manualmente."
    return 1
  fi
  ln -s "$src" "$dst"
  echo "linked: $dst → $src"
}

link_if_needed "$ONE_ROOT/skills" "$CLAUDE_HOME/skills"
link_if_needed "$ONE_ROOT/agents" "$CLAUDE_HOME/agents"

echo ""
echo "Listo. Verifica dentro de Claude Code: /skills"
