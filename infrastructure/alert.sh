#!/bin/zsh
# alert.sh — universal Telegram alert helper for the Acrid fleet.
#
# Usage:
#   scripts/alert.sh <level> <agent_or_job> <message>
#
# Levels:
#   FAIL    — red, oncall worthy: cron failed, secret missing, validator hard-fail
#   WARN    — yellow, degraded: rate-limit hit, partial result, retry succeeded
#   INFO    — green, FYI: pip filled live order, paid customer purchase
#
# Exits 0 on success, 0 on network failure (silent — we never want alert
# delivery to take down the caller's pipeline).
#
# Env required (loaded automatically via scripts/secrets/load.sh):
#   TELEGRAM_BOT_TOKEN
#   TELEGRAM_ALERT_CHAT_ID

set -uo pipefail

LEVEL="${1:-INFO}"
JOB="${2:-acrid}"
shift 2 2>/dev/null || true
MSG="${*:-(no message)}"

REPO_DIR="${ACRID_REPO_ROOT:-$REPO}"

# Load secrets if not already present
if [[ -z "${TELEGRAM_BOT_TOKEN:-}" ]]; then
  # shellcheck disable=SC1091
  source "$REPO_DIR/scripts/secrets/load.sh" 2>/dev/null || true
fi

if [[ -z "${TELEGRAM_BOT_TOKEN:-}" ]] || [[ -z "${TELEGRAM_ALERT_CHAT_ID:-}" ]]; then
  echo "[alert] WARN: TELEGRAM_BOT_TOKEN / TELEGRAM_ALERT_CHAT_ID unset — alert dropped" >&2
  exit 0
fi

case "$LEVEL" in
  FAIL) PREFIX="🔴 FAIL" ;;
  WARN) PREFIX="🟡 WARN" ;;
  INFO) PREFIX="🟢 INFO" ;;
  *)    PREFIX="ℹ️  $LEVEL" ;;
esac

# Telegram message — keep under 4096 chars.
TEXT=$(printf '%s [%s]\n%s' "$PREFIX" "$JOB" "$MSG")
TEXT="${TEXT:0:4000}"

/usr/bin/curl -sS --max-time 10 \
  -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${TELEGRAM_ALERT_CHAT_ID}" \
  --data-urlencode "text=${TEXT}" \
  --data-urlencode "disable_notification=$([[ "$LEVEL" == "INFO" ]] && echo true || echo false)" \
  >/dev/null 2>&1 || true

exit 0
