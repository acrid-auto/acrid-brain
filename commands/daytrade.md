# /daytrade — Acrid Trades day-trade co-pilot + daily lesson (paper, with the operator)

A 1-2 hour learning-by-doing session. **Acrid does all the heavy lifting; the operator learns, decides, and executes (paper).** Acrid checks open trades, scans for setups, teaches ONE concept that builds on past sessions, recommends concrete paper trades (entry, stop, size, the *why*), the operator says yes/no/ask, and **every session is logged to the journal** so the operator can see his own progression. Paper only. Education, never advice. The operator can run this whenever he has time — it adapts to market open or closed.

## Two modes — pick by the clock
- **INTRADAY mode** — best window **~10:00–10:30 ET** (NOT 9:30: ORB/VWAP setups need the first 30 min to form an opening range — before ~10:00 the scanner has nothing to read) and again **~3:00–3:30 ET power hour**. Trade the day's movers, flat by the close. Fast.
- **SWING mode** (market closed / pre-market / teaching): the daily-signal co-pilot + lesson. The default when intraday has no clean trigger.
- **Cadence:** optional — the autonomous swing book trades itself at 9:35 regardless. Run this only to hand-trade/learn; ~10:00 ET and/or ~3:00 ET are the live windows.

Always start with steps 1–2; then branch.

## Run order

1. **Load the journey (so lessons build, not repeat):**
   ```bash
   source scripts/secrets/load.sh; source agents/pip/.venv/bin/activate
   python3 agents/quant/journal.py summary          # concepts already taught + OPEN paper trades to manage
   ```

1b. **INTRADAY setups (run when the market is open):**
   ```bash
   python3 agents/quant/intraday_session.py          # LONG (ORB / VWAP-reclaim / RVOL-momentum) + SHORT (ORB-breakdown / VWAP-reject / parabolic-fade) on 115 names + off-list catalyst movers
   ```
   It prints the RADAR (how many of 115 names + off-list catalyst names scanned, RVOL leaders) then setups, each with side / entry / stop / target / risk-per-share / 2R / suggested shares (already quality-gated: ≥$10, stop ≥1.5% wide, 25% notional cap). Brief per setup: *"X is a [setup]. Trigger $entry, stop $stop (risk ~$R), target $target (2R), N shares ≈ 1% risk."* Shorts: "stop ABOVE, target BELOW." **Entry ONLY on a clean trigger — no chasing. Flat by the close.** If only no-trade/watch-only, say so and fall to SWING mode. (Markets closed → skip to step 3.)

1c. **CRYPTO setups (24/7 — always runnable, even when stocks are closed):**
   ```bash
   python3 agents/quant/crypto_session.py            # rolling-24h VWAP + breakout, long-only, BTC/ETH/SOL/etc
   ```
   Long-only (Alpaca won't short crypto) and **NO broker bracket** — crypto exits are software/manual, so a crypto trade must be watched, not fire-and-forgotten. Same entry/stop/target/fractional-size shape. Surface any setup; note "no auto-stop on the broker — we manage the exit."

1d. **VELEZ open-range co-pilot (market open, 9:30–9:50 window):**
   ```bash
   python3 agents/velez/copilot.py scan 25000          # surface the day's gappers + their Velez state
   python3 agents/velez/copilot.py TICKER 25000        # full read on the name the operator picks
   ```
   The Velez first-20-min method (`agents/velez/FINDINGS.md`) has **no autonomous edge** — backtested 4 ways, all OOS-negative, because the bot traded ~70% of days while the edge is the human discretion to sit out. So it's **human-in-the-loop**. `scan` does the mechanical part (Velez starts from a list too): pulls the day's gappers-on-volume and shows each one's STATE (narrow/wide), LOCATION (above/below the MAs), and whether a volume-confirmed trigger (elephant / tail / lone-red color-game near the 20MA) has formed — flagging the few that are `PICKABLE`. The **operator picks** one from the shortlist and reads the tape; `copilot.py TICKER` then gives the exact 1c entry / 1-bar stop / size (capped at ½ the sleeve, never levered) + live trail. Most names show wide / no-trigger → "SIT OUT," and most days nothing is actionable — honor that. The agent never auto-enters; the pick + the sit-out call are the operator's. Flat by the close.

2. **Manage open trades FIRST.** For any open paper trade from the summary: pull its current price, check it against its stop. If it hit/neared the stop or the thesis is done, walk the operator through closing it (the exit is the trade most people fluff). This is real position management — teach it.

3. **Scan for new setups (Acrid does this — operator does NO analysis):**
   ```bash
   python3 agents/quant/daytrade_session.py
   ```
   Prints the account, high-conviction setups, and the full watchlist read (trend, how stretched, RSI2, ATR%). Each candidate already carries a **volatility-scaled stop (≈2×ATR, floored 2% / capped 8%)** and the **concrete trade pre-sized to 1% risk** (`suggested_shares`, `dollar_risk`, `position_notional`) — read those off directly; no manual math. An overbought name (RSI2 > 97) is flagged "don't chase," not offered as a candidate.

4. **Teach ONE concept, building on the journey.** Pick a concept the operator hasn't covered yet (see the `concepts taught` list from step 1) OR the next layer of one he has. Tie it to what's literally on screen today. Plain English, no jargon, define every term on the spot. One lesson per session — depth over breadth. Examples in rough order: what an uptrend/200-day means → RSI2 oversold → position sizing & the 1% rule → stops & where to put them → why most days you don't trade → reading a setup's risk/reward → managing the exit.

5. **Brief + recommend.** Lead with the account + market open/closed.
   - Candidates exist: for EACH, recommend a concrete paper trade — *"Buy N shares of X at ~$P, stop at $S (you risk ~$R = 1% of the account), because [setup in plain words]."* Size so dollar risk ≈ 1% of equity (shares = 0.01 × equity ÷ risk-per-share). The operator never does the math.
   - No candidates: say so honestly. "No edge today — patience is the trade." Explain why forcing trades loses. That's a real lesson, log it too.

6. **Operator decides + executes.** They approve, veto, or ask. Answer plainly; recompute on request. On an explicit yes, place the PAPER trade:
   - **SWING** (daily setup, stop tracked, may hold days) — simple market order:
     ```bash
     python3 -c "import sys; sys.path.insert(0,'agents/quant'); from alpaca_client import AlpacaClient; print(AlpacaClient().submit_order(symbol='TICKER', side='buy', qty=N))"
     ```
   - **INTRADAY** (ORB/VWAP setup) — bracket order so the stop + target are LIVE on the broker (fire even if nothing's watching):
     ```bash
     python3 -c "import sys; sys.path.insert(0,'agents/quant'); from alpaca_client import AlpacaClient; print(AlpacaClient().submit_bracket(symbol='TICKER', side='buy', qty=N, take_profit=TARGET, stop_loss=STOP))"
     ```
   Confirm the fill + that the bracket legs are working.

7. **Log the session to the journal (REQUIRED — this is the operator's record):**
   ```bash
   python3 agents/quant/journal.py add - <<'JSON'
   {"market":"open|closed",
    "concept_taught":"<the plain-English lesson taught today>",
    "concept_key":"<short-slug e.g. position-sizing>",
    "trades":[{"ticker":"X","side":"buy","qty":N,"entry":P,"stop":S,"risk_dollars":R,"rationale":"...","status":"open"}],
    "passed_on":"<what we skipped + why>",
    "operator_note":"<anything the operator felt/asked worth remembering>",
    "lesson":"<one-line takeaway>"}
   JSON
   ```
   If no trade: omit `trades` (or `[]`). Always capture the concept + the lesson — even no-trade days are progression. The journal lives at `agents/quant/state/trade-journal.md` (the operator can open it any time) and feeds "an AI teaching a human to trade in public."

8. **Recap + progression.** What we did, what we passed on and why, the one concept to remember, and where he is in the journey ("that's N sessions, M concepts — next we'll cover X").

## Hard rules
- **Paper only.** `AlpacaClient` hard-asserts the paper host. No real-money path in this skill.
- **Acrid recommends; operator approves + executes.** Never place a trade without an explicit yes.
- **Risk first.** Every recommendation carries a stop + the dollar risk (~1% of equity). No clean stop → no recommendation.
- **Education, not advice (HARD).** "Here's what I'd do and why in OUR paper account" — teach. Outcomes, not predictions. Never "you should buy ___," no price targets, no tips. Past tense for anything published.
- **No hype. Show the losses.** Most days have no setup — say so. The honesty is the brand.
- **Intraday discipline (HARD):** entry ONLY on a clean trigger through the level (never chase a gap). On a fill, place a REAL protective stop order at the setup's stop (don't just "track" it). **Flat by the close** — close any open intraday paper position before 4:00pm ET; intraday risk does not sleep overnight.
- **Always log (step 7).** A session that isn't journaled didn't teach the operator anything he can see later. Tag intraday sessions with the setup concept (opening-range-breakout, vwap-reclaim) so the journey shows both lanes.
