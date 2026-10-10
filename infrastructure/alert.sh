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

# RECEIPT (2026-10-03). One line per alert with what Telegram answered. Until
# today this script kept no record and threw the answer away, so "was it
# delivered?" had no answer: 21 sales-reply pages were killed by their caller's
# 30s timeout on 10-02 (the secrets load alone took 122s) and nothing said so.
RECEIPT_LOG="$REPO_DIR/infrastructure/local-cron/logs/alert-sent.log"
receipt() {  # plain bash 3.2 syntax: several callers run this file as `bash alert.sh`
  local one_line="${MSG//$'\n'/ ⏎ }"
  printf '%s\t%s\t%s\t%s\t%s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$1" "$LEVEL" "$JOB" \
    "${one_line:0:200}" >> "$RECEIPT_LOG" 2>/dev/null || true
}

# ROUTER (2026-10-08): same policy as tg-send.sh — scripts/notify_route.py says
# PAGE / DIGEST / DROP. Non-pages become a line in state/digest/<ET date>.jsonl
# (read by the 05:50 synopsis email) plus a receipt here; only pages hit
# Telegram. Fail-open: no answer from the router = page.
ROUTE_PY=/usr/local/bin/python3
[[ -x "$ROUTE_PY" ]] || ROUTE_PY=python3
ROUTE=$("$ROUTE_PY" "$REPO_DIR/scripts/notify_route.py" --source alert --level "$LEVEL" --job "$JOB" --body "$MSG" 2>/dev/null | head -n 1)
if [[ "$ROUTE" == "DIGEST" || "$ROUTE" == "DROP" ]]; then
  receipt "ROUTED:$ROUTE"
  exit 0
fi

# Load secrets if not already present. Only the two keys this script needs:
# the full manifest is 53 Keychain reads, and the pager has to answer inside
# its callers' timeouts (knox-prep gives it 10s).
if [[ -z "${TELEGRAM_BOT_TOKEN:-}" ]] || [[ -z "${TELEGRAM_ALERT_CHAT_ID:-}" ]]; then
  ACRID_KEYS_ONLY="TELEGRAM_BOT_TOKEN TELEGRAM_ALERT_CHAT_ID"
  # shellcheck disable=SC1091
  source "$REPO_DIR/scripts/secrets/load.sh" 2>/dev/null || true
  unset ACRID_KEYS_ONLY
fi

if [[ -z "${TELEGRAM_BOT_TOKEN:-}" ]] || [[ -z "${TELEGRAM_ALERT_CHAT_ID:-}" ]]; then
  echo "[alert] WARN: TELEGRAM_BOT_TOKEN / TELEGRAM_ALERT_CHAT_ID unset — alert dropped" >&2
  receipt "DROPPED:no-credentials"
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

RESP=$(/usr/bin/curl -sS --max-time 10 \
  -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${TELEGRAM_ALERT_CHAT_ID}" \
  --data-urlencode "text=${TEXT}" \
  --data-urlencode "disable_notification=$([[ "$LEVEL" == "INFO" ]] && echo true || echo false)" \
  2>/dev/null)
CURL_RC=$?

# An HTTP answer is not a delivery: Telegram says no with a 4xx and a JSON body.
if [[ $CURL_RC -ne 0 ]]; then
  receipt "FAILED:curl-rc-$CURL_RC"
elif [[ "$RESP" == *'"ok":true'* ]]; then
  receipt "OK"
else
  RESP="${RESP//$'\n'/ }"
  receipt "REJECTED:${RESP:0:120}"
fi

exit 0
