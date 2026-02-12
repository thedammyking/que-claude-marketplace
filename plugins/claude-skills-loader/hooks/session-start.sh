#!/usr/bin/env bash
set -euo pipefail

# ──────────────────────────────────────────────────────────────
# Claude Skills Loader — session-start hook
#
# Scans the project tree for SKILL.md files and symlinks their
# parent directories into this plugin's skills/ folder so Claude
# Code can discover them.
#
# Compatibility: macOS bash 3.2+ (no mapfile, no associative arrays)
# ──────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILLS_DIR="${PLUGIN_ROOT}/skills"
PROJECT_ROOT="${PWD}"

EXCLUDE_DIRS="node_modules|\.git|dist|build|\.next|\.turbo|coverage|\.cache"

# Ensure plugin skills dir exists
mkdir -p "$SKILLS_DIR"

# Clean old symlinks (only symlinks, never real files/dirs)
find "$SKILLS_DIR" -maxdepth 1 -type l -delete

# ── I2 fix: exclude the plugin's own skills directory ──
# Resolve SKILLS_DIR to an absolute path for reliable exclusion.
# Also exclude common noise directories via grep.
# ── I4 fix: do NOT suppress find stderr; let errors surface naturally ──

skill_files=()
while IFS= read -r line; do
    skill_files+=("$line")
done < <(
    find "$PROJECT_ROOT" -maxdepth 5 -name "SKILL.md" -type f \
        -not -path "${SKILLS_DIR}/*" \
        | grep -vE "/(${EXCLUDE_DIRS})/" || true
)

# If no skills found, exit silently
[ ${#skill_files[@]} -gt 0 ] || exit 0

# ── C1 fix: collision detection without associative arrays ──
# Write every base skill name to a temp file, then count duplicates.
# A name appearing more than once means there is a collision.

name_list_file="$(mktemp)"
trap 'rm -f "$name_list_file"' EXIT

for skill_file in "${skill_files[@]}"; do
    skill_dir="$(dirname "$skill_file")"
    basename "$skill_dir"
done > "$name_list_file"

# ── I1 fix: multi-level collision resolution ──
# When two skills share the same base name we need a unique link name.
# Strategy: use the relative path from PROJECT_ROOT with '/' → '--'.
# This guarantees uniqueness even when parent dirs also collide
# (e.g. apps/billing/utils and libs/billing/utils both become unique).

for skill_file in "${skill_files[@]}"; do
    skill_dir="$(dirname "$skill_file")"
    skill_name="$(basename "$skill_dir")"

    # Count how many times this base name appears
    # (sort | uniq -c is bash-3.2-safe)
    count="$(grep -cxF "$skill_name" "$name_list_file")"

    if [ "$count" -gt 1 ]; then
        # Collision — derive link name from the full relative path
        # e.g. apps/billing/utils → apps--billing--utils
        rel_path="${skill_dir#"${PROJECT_ROOT}"/}"
        link_name="$(printf '%s' "$rel_path" | sed 's|/|--|g')"
    else
        link_name="$skill_name"
    fi

    ln -sf "$skill_dir" "${SKILLS_DIR}/${link_name}"
done

exit 0
