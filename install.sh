#!/usr/bin/env bash
# Consulting Deck Studio installer: puts the skill where every detected AI agent can find it.
#
#   ./install.sh                  # global install, symlinked, into every detected agent
#   ./install.sh --copy           # copy instead of symlink (use on Windows/WSL or if you will delete the clone)
#   ./install.sh --project        # install into ./.agents/skills and ./.claude/skills of the current folder
#   ./install.sh --agents claude,codex,gemini   # only these
#   ./install.sh --all            # every known location, detected or not
#   ./install.sh --dry-run        # show what would happen
#   ./install.sh --uninstall      # remove what this script installed
#
# One-liner (clones to ~/.consulting-deck-studio, then installs):
#   curl -fsSL https://raw.githubusercontent.com/ali-lari1/consulting-deck-studio/main/install.sh | bash
set -euo pipefail

NAME="consulting-deck-studio"
REPO="https://github.com/ali-lari1/consulting-deck-studio.git"
HOME_CLONE="${CDS_HOME:-$HOME/.consulting-deck-studio}"
MODE="symlink"; SCOPE="global"; ONLY=""; ALL=0; DRY=0; UNINSTALL=0; FORCE=0

while [ $# -gt 0 ]; do
  case "$1" in
    --copy) MODE="copy" ;;
    --project) SCOPE="project" ;;
    --agents) ONLY=",$2,"; shift ;;
    --all) ALL=1 ;;
    --dry-run) DRY=1 ;;
    --uninstall) UNINSTALL=1 ;;
    --force) FORCE=1 ;;
    -h|--help) sed -n '2,14p' "$0" 2>/dev/null || true; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

# Locate the skill source: this checkout, or clone/update one.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || echo "")"
if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/skills/$NAME/SKILL.md" ]; then
  ROOT="$SCRIPT_DIR"
else
  command -v git >/dev/null || { echo "git is required for the one-line install" >&2; exit 1; }
  if [ -d "$HOME_CLONE/.git" ]; then
    echo "updating $HOME_CLONE"; [ $DRY = 1 ] || git -C "$HOME_CLONE" pull --ff-only --quiet
  else
    echo "cloning into $HOME_CLONE"; [ $DRY = 1 ] || git clone --depth 1 --quiet "$REPO" "$HOME_CLONE"
  fi
  ROOT="$HOME_CLONE"
fi
SRC="$ROOT/skills/$NAME"

if [ "$SCOPE" = "project" ]; then BASE="$PWD"; else BASE="$HOME"; fi

# id | path under BASE | detectors (commands or ~/.dirs) | scopes
TARGETS="
agents|.agents/skills|codex gemini opencode goose cursor copilot amp grok cline windsurf|global project
claude|.claude/skills|claude .claude|global project
gemini|.gemini/skills|gemini .gemini|global
opencode|.config/opencode/skills|opencode .config/opencode|global
hermes|.hermes/skills|hermes .hermes|global
grok|.grok/skills|grok .grok|global
codex-legacy|.codex/skills|.codex|global
cursor|.cursor/skills|cursor .cursor|global
copilot|.copilot/skills|copilot .copilot|global
kiro|.kiro/skills|kiro kiro-cli .kiro|global project
cline|.cline/skills|cline .cline|global
windsurf|.codeium/windsurf/skills|windsurf .codeium/windsurf|global
amp|.config/agents/skills|amp .config/amp|global
antigravity|.gemini/antigravity-cli/skills|agy .gemini/antigravity-cli|global
"

detected() {
  for d in $1; do
    case "$d" in
      .*) [ -d "$HOME/$d" ] && return 0 ;;
      *) command -v "$d" >/dev/null 2>&1 && return 0 ;;
    esac
  done
  return 1
}

act() { if [ $DRY = 1 ]; then echo "  would: $*"; else "$@"; fi; }
count=0
echo "Consulting Deck Studio: $([ $UNINSTALL = 1 ] && echo uninstall || echo "install ($MODE, $SCOPE)")"
while IFS='|' read -r id path dets scopes; do
  [ -z "$id" ] && continue
  case " $scopes " in *" $SCOPE "*) ;; *) continue ;; esac
  if [ -n "$ONLY" ]; then case "$ONLY" in *",$id,"*) ;; *) [ "$id" = agents ] || continue ;; esac; fi
  # .agents/skills is the cross-agent standard: always installed. Others only if the tool is detected (or --all).
  if [ "$id" != "agents" ] && [ $ALL = 0 ] && [ -z "$ONLY" ] && ! detected "$dets"; then continue; fi
  dest="$BASE/$path/$NAME"
  if [ $UNINSTALL = 1 ]; then
    if [ -L "$dest" ] || [ -f "$dest/.cds-installed" ]; then act rm -rf "$dest"; echo "  removed  $dest"; count=$((count+1)); fi
    continue
  fi
  if [ -e "$dest" ] && [ ! -L "$dest" ] && [ ! -f "$dest/.cds-installed" ] && [ $FORCE = 0 ]; then
    echo "  skipped  $dest (exists and was not installed by this script; use --force)"; continue
  fi
  if [ "$(cd "$dest" 2>/dev/null && pwd -P)" = "$(cd "$SRC" && pwd -P)" ] && [ ! -L "$dest" ]; then
    echo "  skipped  $dest (is the source)"; continue
  fi
  act mkdir -p "$BASE/$path"
  act rm -rf "$dest"
  if [ "$MODE" = "copy" ]; then act cp -R "$SRC" "$dest"; act touch "$dest/.cds-installed"; else act ln -s "$SRC" "$dest"; fi
  echo "  $id → $dest"
  count=$((count+1))
done <<EOF
$TARGETS
EOF

if [ $UNINSTALL = 1 ]; then echo "done ($count removed)"; exit 0; fi
echo
echo "Installed into $count location(s). Restart your agent sessions, then ask:"
echo '  "Build the October SteerCo status report from these files"   or   /consulting-deck-studio'
command -v python3 >/dev/null || echo "Note: python3 is required to build decks. Install Python 3.8+."
if [ "$MODE" = "symlink" ]; then echo "Update later with: git -C \"$ROOT\" pull"; fi
