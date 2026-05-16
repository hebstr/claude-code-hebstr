#!/usr/bin/env bash
# sanitize-bash-history.sh — Extract command patterns from ~/.bash_history
# without leaking sensitive arguments.
#
# TRUST BOUNDARY: this script is the only path through which shell history
# reaches Claude. It runs locally and emits abstracted frequency tables only.
# Raw history never enters API context.
#
# Security-critical. Review changes carefully. Claude may invoke this script
# but must never modify it without explicit user approval.
#
# Usage: ./sanitize-bash-history.sh [history-file] [max-lines]
# Defaults: ~/.bash_history, last 10000 entries

set -Eeuo pipefail

HISTORY_FILE="${1:-$HOME/.bash_history}"
MAX_LINES="${2:-10000}"

if [[ ! -f "$HISTORY_FILE" ]]; then
  echo "ERROR: history file not found: $HISTORY_FILE" >&2
  exit 1
fi

SENSITIVE_PATTERNS=(
  '[Kk][Ee][Yy]='
  '[Tt][Oo][Kk][Ee][Nn]='
  '[Ss][Ee][Cc][Rr][Ee][Tt]='
  '[Pp][Aa][Ss][Ss][Ww][Oo][Rr][Dd]='
  'Authorization:'
  'Bearer '
  'export [A-Z_]*=.'
  'ssh-keygen'
  'openssl.*-pass'
  'mysql.*-p'
  'psql.*password'
  'gh auth'
  'vault '
  '1password'
  'op '
  'aws configure'
  'AWS_ACCESS'
  'ANTHROPIC_API'
  'OPENAI_API'
  'GITHUB_TOKEN'
  'HF_TOKEN'
  'mongodb://'
  'postgres://'
  'mysql://'
  'redis://'
  'cat.*\.env'
  'less.*\.env'
  'source.*\.env'
  '\. .*\.env'
)

GREP_ARGS=()
for pat in "${SENSITIVE_PATTERNS[@]}"; do
  GREP_ARGS+=(-e "$pat")
done

filter_history() {
  tail -n "$MAX_LINES" "$HISTORY_FILE" |
    grep -v '^#[0-9]\+' |
    grep -v '^\s*$' |
    { grep -iv "${GREP_ARGS[@]}" || true; }
}

echo "# Command frequency (last $MAX_LINES entries, arguments abstracted)"
echo "# Generated: $(date -Iseconds)"
echo "# Source: $HISTORY_FILE"
echo ""

filter_history |
  awk '{
		cmd = $1
		if (cmd == "git" || cmd == "docker" || cmd == "kubectl" || \
		    cmd == "uv" || cmd == "pip" || cmd == "cargo" || cmd == "npm" || \
		    cmd == "yarn" || cmd == "pnpm" || cmd == "pak" || cmd == "rv" || \
		    cmd == "systemctl" || cmd == "stow" || cmd == "gh" || \
		    cmd == "apt" || cmd == "snap" || cmd == "brew" || cmd == "claude") {
			if (NF >= 2) pattern = cmd " " $2
			else pattern = cmd
		}
		else if (cmd == "cd" || cmd == "cat" || cmd == "less" || cmd == "bat" || \
		         cmd == "head" || cmd == "tail" || cmd == "wc" || cmd == "file" || \
		         cmd == "stat" || cmd == "chmod" || cmd == "chown" || \
		         cmd == "source" || cmd == "." || cmd == "rg" || cmd == "grep" || \
		         cmd == "fd" || cmd == "fdfind" || cmd == "find" || cmd == "vi" || \
		         cmd == "vim" || cmd == "nano" || cmd == "code" || cmd == "positron" || \
		         cmd == "quarto" || cmd == "Rscript" || cmd == "python" || cmd == "R") {
			pattern = cmd " <arg>"
		}
		else if (cmd == "ssh" || cmd == "scp" || cmd == "rsync" || \
		         cmd == "ping" || cmd == "dig" || cmd == "nslookup") {
			pattern = cmd " <target>"
		}
		else if (cmd == "curl" || cmd == "wget" || cmd == "http" || cmd == "httpie") {
			pattern = cmd " <url>"
		}
		else if (NF == 1) {
			pattern = cmd
		}
		else {
			pattern = cmd " ..."
		}
		counts[pattern]++
	}
	END {
		for (p in counts) printf "%6d\t%s\n", counts[p], p
	}' |
  sort -rn |
  head -80

echo ""
echo "---"
echo "# Repeated multi-command chains (alias/function candidates)"
echo "# Only command names shown; arguments stripped"
echo ""

filter_history |
  grep -E '&&|\|' |
  sed -E '
		s/"[^"]*"//g
		s/'"'"'[^'"'"']*'"'"'//g
		s/([a-zA-Z0-9_.-]+)[[:space:]]+[^|&]*/\1 /g
		s/[[:space:]]+/ /g
		s/^ //
		s/ $//
	' |
  awk '{ counts[$0]++ } END { for (c in counts) if (counts[c] > 2) printf "%6d\t%s\n", counts[c], c }' |
  sort -rn |
  head -20
