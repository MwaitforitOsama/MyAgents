#!/usr/bin/env bash
# Installs Mr. Plumb and Mason into Claude Code (user level).
#
#   ./install.sh              install (symlinks + guard hooks), then run guard tests
#   ./install.sh --uninstall  remove symlinks and the guard hooks
#
# Safe to re-run. Never overwrites files it didn't create. Asks before changing
# ~/.claude/settings.json and keeps a backup.

set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd -P)"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
SETTINGS="$CLAUDE_DIR/settings.json"
AGENTS="plumb mason"

say()  { printf '%s\n' "$*"; }
fail() { printf 'Error: %s\n' "$*" >&2; exit 1; }

confirm() {
  local answer=""
  # Open the terminal on fd 3 first; only that step's errors are silenced, so the prompt stays visible.
  if ! { exec 3</dev/tty; } 2>/dev/null; then
    say "No terminal available to confirm; skipping. Re-run ./install.sh in a terminal."
    return 1
  fi
  printf '%s [y/N] ' "$1" >/dev/tty
  read -r answer <&3 || answer=""
  exec 3<&-
  [ "$answer" = "y" ] || [ "$answer" = "Y" ]
}

check_deps() {
  command -v python3 >/dev/null || fail "python3 is required (the guard hook is written in Python)."
  command -v jq >/dev/null || fail "jq is required to edit $SETTINGS safely."
}

link() {  # link SRC DST
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [ -L "$dst" ]; then
    if [ "$(readlink "$dst")" = "$src" ]; then
      say "  ok      $dst"
      return
    fi
    fail "$dst is a symlink to $(readlink "$dst"), not to this repo. Remove it yourself if that's intended."
  elif [ -e "$dst" ]; then
    fail "$dst already exists and is not a symlink. Move it away first; nothing was changed."
  fi
  ln -s "$src" "$dst"
  say "  linked  $dst -> $src"
}

unlink_ours() {  # unlink_ours SRC DST
  local src="$1" dst="$2"
  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
    rm "$dst"
    say "  removed $dst"
  else
    say "  skip    $dst (not a link to this repo)"
  fi
}

apply_settings() {  # apply_settings NEW_JSON_FILE DESCRIPTION
  local new="$1" what="$2" backup
  say ""
  say "Proposed change to $SETTINGS ($what):"
  diff <(jq -S . "$SETTINGS") <(jq -S . "$new") || true
  say ""
  if confirm "Apply this change?"; then
    backup="$SETTINGS.bak-plumb-$(date +%Y%m%d-%H%M%S)"
    [ -e "$backup" ] || cp "$SETTINGS" "$backup"  # same second: keep the earlier (original) backup
    mv "$new" "$SETTINGS"
    say "  updated $SETTINGS (backup: $backup)"
  else
    rm -f "$new"
    say "  settings unchanged"
  fi
}

hook_registered() {  # hook_registered GUARD_FILE_NAME
  jq -e --arg g "$1" \
    '[.hooks.PreToolUse[]?.hooks[]?.command // empty] | any(contains($g))' "$SETTINGS" >/dev/null
}

hook_entry() {  # hook_entry GUARD_FILE_NAME -> the matching entry from settings-hook.json
  sed "s|__REPO__|$REPO|" "$REPO/claude/settings-hook.json" \
    | jq --arg g "$1" '.hooks.PreToolUse[] | select(any(.hooks[]; .command | contains($g)))'
}

install() {
  check_deps
  say "Installing Mr. Plumb and Mason from $REPO"
  [ -f "$SETTINGS" ] || echo '{}' > "$SETTINGS"
  local a guard entry tmp
  for a in $AGENTS; do
    guard="${a}_guard.py"
    chmod +x "$REPO/claude/hooks/$guard"
    link "$REPO/skills/$a" "$CLAUDE_DIR/skills/$a"
    link "$REPO/claude/agents/$a.md" "$CLAUDE_DIR/agents/$a.md"
    if hook_registered "$guard"; then
      say "  ok      $guard already registered in $SETTINGS"
    else
      entry="$(hook_entry "$guard")"
      tmp="$(mktemp)"
      jq --argjson entry "$entry" '.hooks = (.hooks // {}) | .hooks.PreToolUse = ((.hooks.PreToolUse // []) + [$entry])' \
        "$SETTINGS" > "$tmp"
      apply_settings "$tmp" "register $guard; it only acts when agent_type is \"$a\""
    fi
  done

  say ""
  say "Running guard tests..."
  python3 "$REPO/claude/hooks/tests/run_guard_tests.py"
  python3 "$REPO/claude/hooks/tests/run_mason_tests.py"
  say ""
  say "Done. In your project directory, start each agent in its own terminal:"
  say "  claude --agent plumb -n plumb     # plans and reviews (Fable)"
  say "  claude --agent mason -n mason     # implements (Opus)"
  say "In regular chats, the plumb and mason skills trigger automatically or via /plumb, /mason (soft rules only)."
}

uninstall() {
  check_deps
  say "Uninstalling Mr. Plumb and Mason"
  local a guard tmp
  for a in $AGENTS; do
    guard="${a}_guard.py"
    unlink_ours "$REPO/skills/$a" "$CLAUDE_DIR/skills/$a"
    unlink_ours "$REPO/claude/agents/$a.md" "$CLAUDE_DIR/agents/$a.md"
    if [ -f "$SETTINGS" ] && hook_registered "$guard"; then
      tmp="$(mktemp)"
      jq --arg g "$guard" '
      .hooks.PreToolUse |= map(.hooks |= map(select((.command // "") | contains($g) | not)))
      | .hooks.PreToolUse |= map(select((.hooks | length) > 0))
      | if (.hooks.PreToolUse | length) == 0 then del(.hooks.PreToolUse) else . end
      | if (.hooks | length) == 0 then del(.hooks) else . end' "$SETTINGS" > "$tmp"
      apply_settings "$tmp" "remove $guard"
    else
      say "  ok      $guard not registered"
    fi
  done
}

case "${1:-}" in
  "") install ;;
  --uninstall) uninstall ;;
  *) fail "unknown option: $1 (use --uninstall or nothing)" ;;
esac
