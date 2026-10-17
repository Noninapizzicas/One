#!/usr/bin/env python3
"""
Importa skills y agents desde el fork local de ECC al repo One.

Uso:
  python scripts/import-from-ecc.py                # importa todos
  python scripts/import-from-ecc.py --only NAME    # importa uno
  python scripts/import-from-ecc.py --dry-run      # muestra qué haría

El importador NO sobrescribe archivos existentes a menos que pases --force.
"""
from __future__ import annotations
import argparse
import shutil
import sys
from pathlib import Path

ONE_ROOT = Path(__file__).resolve().parent.parent
ECC_ROOT = Path("/home/user/ecc")


def import_skills(only: str | None, dry_run: bool, force: bool) -> int:
    src = ECC_ROOT / "skills"
    dst = ONE_ROOT / "skills"
    count = 0
    for skill_dir in sorted(src.iterdir()):
        if not skill_dir.is_dir():
            continue
        if only and skill_dir.name != only:
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        target = dst / skill_dir.name
        if target.exists() and not force:
            print(f"skip (exists): {target}")
            continue
        if dry_run:
            print(f"would import skill: {skill_dir.name}")
        else:
            shutil.copytree(skill_dir, target, dirs_exist_ok=force)
            print(f"imported skill: {skill_dir.name}")
        count += 1
    return count


def import_agents(only: str | None, dry_run: bool, force: bool) -> int:
    src = ECC_ROOT / "agents"
    dst = ONE_ROOT / "agents"
    count = 0
    for agent_file in sorted(src.glob("*.md")):
        name = agent_file.stem
        if only and name != only:
            continue
        target = dst / agent_file.name
        if target.exists() and not force:
            print(f"skip (exists): {target}")
            continue
        if dry_run:
            print(f"would import agent: {name}")
        else:
            shutil.copy2(agent_file, target)
            print(f"imported agent: {name}")
        count += 1
    return count


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--only", help="Importar solo un skill/agent por nombre")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true", help="Sobrescribe destino si existe")
    p.add_argument("--skip-skills", action="store_true")
    p.add_argument("--skip-agents", action="store_true")
    args = p.parse_args()

    if not ECC_ROOT.exists():
        print(f"error: {ECC_ROOT} no existe. Clona el fork primero.", file=sys.stderr)
        return 2

    skills = 0 if args.skip_skills else import_skills(args.only, args.dry_run, args.force)
    agents = 0 if args.skip_agents else import_agents(args.only, args.dry_run, args.force)
    print(f"\nSkills: {skills}  Agents: {agents}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
