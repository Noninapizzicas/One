#!/usr/bin/env python3
"""
Importa skills y agents desde el fork local de ECC al repo One.

Crea automáticamente los symlinks en ~/.hermes/skills/ para que Hermes
los vea sin pasos manuales. Una sola fuente de verdad: ~/One/.

Uso:
  python scripts/import-from-ecc.py                     # importa todos
  python scripts/import-from-ecc.py --only NAME         # importa uno
  python scripts/import-from-ecc.py --dry-run           # muestra qué haría
  python scripts/import-from-ecc.py --no-symlink        # solo copia, sin symlinkear
  python scripts/import-from-ecc.py --ecc-root /ruta    # otra ruta de ECC
  ECC_ROOT=/ruta python scripts/import-from-ecc.py      # via env var

El importador NO sobrescribe archivos existentes a menos que pases --force.
"""
from __future__ import annotations
import argparse
import os
import shutil
import sys
from pathlib import Path

ONE_ROOT = Path(__file__).resolve().parent.parent

# Candidatos por defecto para ECC_ROOT, en orden de preferencia.
ECC_CANDIDATES = [
    os.environ.get("ECC_ROOT", ""),
    str(Path.home() / "ecc"),
    str(ONE_ROOT.parent / "ecc"),
    "/home/user/ecc",
]

HERMES_HOME = Path(os.environ.get("HERMES_HOME", str(Path.home() / ".hermes")))
HERMES_SKILLS_DIR = HERMES_HOME / "skills"


def resolve_ecc_root(cli_arg: str | None) -> Path | None:
    """Devuelve la primera ruta ECC existente, o None si no encuentra ninguna."""
    candidates = [cli_arg] if cli_arg else []
    candidates.extend(ECC_CANDIDATES)
    for c in candidates:
        if c and Path(c).exists():
            return Path(c)
    return None


def symlink_skill(name: str, dry_run: bool) -> None:
    """Crea ~/.hermes/skills/<name> → ~/One/skills/<name>."""
    if not HERMES_HOME.exists():
        print(f"  warn: {HERMES_HOME} no existe, salto symlink (¿Hermes instalado?)")
        return
    HERMES_SKILLS_DIR.mkdir(exist_ok=True)
    src = ONE_ROOT / "skills" / name
    dst = HERMES_SKILLS_DIR / name
    if dst.is_symlink() and dst.resolve() == src.resolve():
        print(f"  ok symlink: {dst} → {src}")
        return
    if dst.exists() or dst.is_symlink():
        print(f"  skip symlink (destino existe, no es nuestro): {dst}")
        return
    if dry_run:
        print(f"  would symlink: {dst} → {src}")
    else:
        dst.symlink_to(src)
        print(f"  symlinked: {dst} → {src}")


def symlink_agent(name: str, dry_run: bool) -> None:
    """Crea ~/.hermes/skills/<name>/SKILL.md → ~/One/agents/<name>.md.

    Hermes espera SKILL.md dentro de una carpeta; el agent es un .md plano,
    así que creamos la carpeta y symlinkeamos el SKILL.md dentro.
    """
    if not HERMES_HOME.exists():
        print(f"  warn: {HERMES_HOME} no existe, salto symlink (¿Hermes instalado?)")
        return
    HERMES_SKILLS_DIR.mkdir(exist_ok=True)
    src = ONE_ROOT / "agents" / f"{name}.md"
    dst_dir = HERMES_SKILLS_DIR / name
    dst_file = dst_dir / "SKILL.md"
    if dst_file.is_symlink() and dst_file.resolve() == src.resolve():
        print(f"  ok symlink: {dst_file} → {src}")
        return
    if dst_file.exists() or dst_file.is_symlink():
        print(f"  skip symlink (destino existe, no es nuestro): {dst_file}")
        return
    if dry_run:
        print(f"  would symlink: {dst_file} → {src}")
    else:
        dst_dir.mkdir(exist_ok=True)
        dst_file.symlink_to(src)
        print(f"  symlinked: {dst_file} → {src}")


def import_skills(ecc: Path, only: str | None, dry_run: bool,
                  force: bool, no_symlink: bool) -> int:
    src_root = ecc / "skills"
    dst_root = ONE_ROOT / "skills"
    count = 0
    for skill_dir in sorted(src_root.iterdir()):
        if not skill_dir.is_dir():
            continue
        if only and skill_dir.name != only:
            continue
        if not (skill_dir / "SKILL.md").exists():
            continue
        target = dst_root / skill_dir.name
        if target.exists() and not force:
            print(f"skip (exists): {target}")
        elif dry_run:
            print(f"would import skill: {skill_dir.name}")
        else:
            shutil.copytree(skill_dir, target, dirs_exist_ok=force)
            print(f"imported skill: {skill_dir.name}")
        if not no_symlink:
            symlink_skill(skill_dir.name, dry_run)
        count += 1
    return count


def import_agents(ecc: Path, only: str | None, dry_run: bool,
                  force: bool, no_symlink: bool) -> int:
    src_root = ecc / "agents"
    dst_root = ONE_ROOT / "agents"
    count = 0
    for agent_file in sorted(src_root.glob("*.md")):
        name = agent_file.stem
        if only and name != only:
            continue
        target = dst_root / agent_file.name
        if target.exists() and not force:
            print(f"skip (exists): {target}")
        elif dry_run:
            print(f"would import agent: {name}")
        else:
            shutil.copy2(agent_file, target)
            print(f"imported agent: {name}")
        if not no_symlink:
            symlink_agent(name, dry_run)
        count += 1
    return count


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--only", help="Importar solo un skill/agent por nombre")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true",
                   help="Sobrescribe destino si existe")
    p.add_argument("--skip-skills", action="store_true")
    p.add_argument("--skip-agents", action="store_true")
    p.add_argument("--no-symlink", action="store_true",
                   help="No crear symlinks en ~/.hermes/skills/")
    p.add_argument("--ecc-root",
                   help="Ruta al fork local de ECC (o usa env ECC_ROOT)")
    args = p.parse_args()

    ecc = resolve_ecc_root(args.ecc_root)
    if ecc is None:
        print("error: no encuentro el fork de ECC. Pasa --ecc-root <ruta>,",
              file=sys.stderr)
        print("       setea ECC_ROOT, o clónalo en ~/ecc.", file=sys.stderr)
        return 2
    print(f"ECC_ROOT = {ecc}")
    print(f"HERMES_HOME = {HERMES_HOME}")
    print()

    skills = 0 if args.skip_skills else import_skills(
        ecc, args.only, args.dry_run, args.force, args.no_symlink)
    agents = 0 if args.skip_agents else import_agents(
        ecc, args.only, args.dry_run, args.force, args.no_symlink)
    print(f"\nSkills: {skills}  Agents: {agents}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
