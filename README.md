# Jump Street Pokerbot: Imperial AI Hack 2026 (Track 04: AI Poker Bots)

**Winning bot** of the Imperial AI Hack "AI Poker Bots" track (Optiver · Jump Trading · AlgoSoc), built by team **Jump Street**.

One file (`Winning Bot.py`, ~1,500 lines, 65 KB), pure Python standard library (3.9+), playing 7–8-handed No-Limit Texas Hold'em against the other teams' bots. It is an **opponent-model-first exploitative bot**: it doesn't try to play "perfect" poker. It works out what each opponent at the table does, then plays the most profitable counter-strategy, typically in under a millisecond per decision.

---

## The competition

### The game

| | |
|---|---|
| Game | No-Limit Texas Hold'em, 7 or 8 bots per table |
| Round | 1,000 hands at one table; every hand starts every bot on 2,000 chips (100 bb) with blinds 10/20, so nobody busts and every table deals the same number of hands |
| Actions | `act(state)` returns `fold`, `check`, `call`, `raise` (with a "raise to" amount) or `all_in`; you can always go all in |
| Bot interface | One file, `bot.py`, with a class `Agent`; `on_table_start(info)` and `on_hand_end(summary)` are optional |
| Bot lifecycle | A fresh `Agent` per table per round: it remembers the 1,000 hands of that round with the same opponents, nothing more |
| Limits | 25 ms per decision, 10 s thinking bank per round, standard library only, 512 MB, file ≤ 200 KB, no files or network |
| Failure mode | Errors, timeouts and illegal actions become a check if allowed, otherwise a fold. Running out of memory, crashing or flooding the dealer stops the bot for the rest of that round |
| Hand data | After each round you see every hand at your table: all actions, the board, every seat's result, your own cards, and opponents' cards **only when shown at showdown**. Nothing about other bots' hidden cards, code or timing |
| Uploads | One live bot per team. Every upload is test-loaded in the sandbox first; a new upload plays from the next round, and rounds already played keep their scores |

### Format

Rounds run every 5 minutes, live all weekend.

| Stage | When | What happens |
|---|---|---|
| 1. Practice rounds | Sat 12:35–13:55 | Real games against real bots that don't count |
| 2. Counted rounds | Sat 15:00–19:25 | Everyone reseated each round so you play everyone; ranked by average score. A team needs 12 counted rounds (an hour) to be ranked |
| 3. Buckets | Sat 20:30 | Saturday's ranking is dealt across Sunday's tables like cards, so each table mixes strong and weak bots (31 teams over 4 tables) |
| 4. Bucket tables | Sun 09:00–11:55 | Each table keeps its own score from zero; the top 2 by chips at each table make the final. Uploads close at 12:00 |
| 5. Final table | Sun 12:05 | 8 bots, 5,000 hands, most chips wins; every 100th hand replayed live 12:10–12:35 |

### Scoring

Score is the chips a bot wins, shown as **bb/100** (big blinds won per 100 hands), averaged over every hand it plays. Practice rounds never count. For scale: folding every hand loses about 19 bb/100, so anything above zero is winning.

Jump Street finished Saturday 19th of 31 (+5.7 bb/100), was dealt into Sunday's Table C, and went on to win. The Table C scouting described below was built overnight for exactly that table.

---

## How it works at a glance

```
            ┌──────────────────────────────────────────────────────────────┐
on_hand_end │ OppBook.learn(): replays the hand history and updates ~25    │
──────────► │ stats per seat, plus showdown evidence and bot-type detection│
            └──────────────────────────────┬───────────────────────────────┘
                                           │ per-seat model
            ┌──────────────────────────────▼───────────────────────────────┐
act(state)  │ preflop(): 169-hand equity table × estimated range width     │
──────────► │ postflop(): opponent range pools → Monte Carlo equity →      │
            │             EV of check / each bet size / call / raise       │
            └──────────────────────────────┬───────────────────────────────┘
                                           │
            ┌──────────────────────────────▼───────────────────────────────┐
            │ legal(): clamp and sanitise · safe(): fallback · timing guard│
            └──────────────────────────────────────────────────────────────┘
```

The bot has four layers:
1. **A fast hand evaluator and precomputed preflop tables** (the maths).
2. **An opponent book (`OppBook`)** that learns every seat's tendencies live, hand by hand (the reads).
3. **Decision logic** that turns equity and the reads into expected-value comparisons (the strategy).
4. **A safety and speed shell** so it never times out or makes an illegal move (the robustness).

---

## 1. The maths layer

### 7-card hand evaluator (`ev7`)
A hand-rolled evaluator built for speed in pure Python:
- Each card is an int `rank*4 + suit`.
- **Rank key:** `sum(5**rank)` gives a unique key per rank multiset (no rank can appear more than 4 times, so base 5 never overflows). Non-flush hand values are memoised in a dict `NF` keyed by it, so each distinct rank pattern is computed only once and then looked up.
- **Flush detection:** `sum(8**suit)` packs the suit counts into one integer; the lookup table `FSUIT` says instantly whether any suit has ≥ 5 cards.
- **Flushes and straight flushes:** an 8,192-entry table `FLV` indexed by the 13-bit rank mask of the flush suit.
- **Straights:** an 8,192-entry table `STRAIGHT` (wheel A-2-3-4-5 included).
- Values are packed as `category << 20 | rank nibbles`, so comparing two hands is a single integer comparison.

All tables are built at import time (well inside the 5 s setup allowance), then `gc.freeze()` / `gc.disable()` stop Python's garbage collector from pausing mid-decision.

### Preflop equity table (`_TBL`)
All 169 starting-hand classes, each with its equity against an opponent range of width 2%, 4%, 7%, 11%, 16%, 24%, 35%, 50%, 75% and 100% of hands. `eq_vs(hand, q)` interpolates equity against "the top q% of hands".

The classes are **ordered by equity against a random hand** (the 100% column), which puts high cards ahead of small pairs and suited connectors: **AKs is #8, AKo #12, AQo #14**, 22 is #87 and 76s is #115. `PCT[hand]` gives each class's percentile in combo-weighted order, so "top q%" maps directly to a list of actual card combinations (`COMBOS`). The equity columns themselves are what capture how a hand plays against tighter ranges.

---

## 2. The opponent book: live learning within each round

`OppBook` holds a `Seat` record per opponent and updates it after **every hand** from the full action history and any cards shown at showdown. Since the sandbox creates a fresh bot every round, this is the bot learning *during play*, from zero, in each 1,000-hand round.

### What it tracks per seat
- **Preflop:** VPIP, PFR, 3-bets, shoves; fold to an open, to a 3-bet, to a 4-bet; big-blind defence; open sizes (as a histogram).
- **Postflop:** bet frequency when checked to, raise frequency facing a bet, folds by **commitment state × bet size** (fresh / called earlier / bet earlier × small / medium / big), bet sizes used.
- **Showdowns:** for each preflop line (call, raise, 3-bet, shove), the average strength of the hands shown; how often its postflop bets and calls turned out to be **weak hands**; and, for bets, that weak share split by small vs big bets (a "size tell").
- **Against us specifically:** how this seat answers *our* bets by size, and chips won or lost against it heads-up.

### Shrinkage, not raw percentages
Every frequency is blended with a prior (e.g. fold-to-3-bet starts at 55% with a weight of 6 pseudo-observations), so early reads are sensible and the bot doesn't overreact to three hands. The postflop **fold priors (`FPRI`) were fitted on ~25,000 real tournament decisions**, and each seat's deviation from those priors is learned overall and per street.

### Range width estimates
`open_q`, `tb_q`, `shove_q` convert a seat's frequencies into "this seat raises the top X% of hands", corrected by what it actually showed at showdown (`_sd`). `_line_q` then combines everything a seat did this hand into one range width. This is the key input whenever the bot faces a raise preflop, and the starting point of every postflop range.

### Bot-type detection (`classify` and `station`)
`classify` recognises degenerate or scripted bots and switches to hard exploits:
- `starter`: the organisers' starter template (detected by its exact raise-sizing formula, flagged in `parse`)
- `always_fold`, `always_call`, `always_raise`, `always_allin`, `random`

A separate check, `station()`, flags seats that call too much and rarely raise: against them the bot bets bigger for value and never bluffs.

### Fold probability model (`pfold`)
The central postflop read: *P(this seat folds to a bet of x pots right now)*. It combines:
- the real-data prior, and the seat's personal deviation from it (per street);
- its counts in that exact commitment state and size bucket;
- how it has answered **our** bets of that size (ignored if it has been beating us heads-up);
- on the turn and river, whether it has already checked this hand (gives up more);
- whether it was the preflop raiser (folds less to a lead);
- overbet adjustments.

### Sunday Table C scouting (`identify`)
For the Sunday bucket table, the team studied the opponents' real hands and found **fixed open-size fingerprints**. When a seat repeatedly opens to exactly the same size, the bot tags it and pre-loads what that bot's real hands showed, as pseudo-observations, so the seat's own play still overrides them:

| Tag | Fingerprint | Pre-loaded read |
|---|---|---|
| `J` | Opens exactly 3.0 bb, only from seat 7 when we sit in seat 4 of 8 | Folds ~85% to 3-bets, shoves only QQ+, passive postflop: its bets are strong |
| `F` | Opens 3.2 bb (≥ 70% of its opens), very wide | Folds ~60% to 3-bets and ~92% to small 4-bets (176 real cases) |
| `M` | 2.5 bb opens plus open-shoves | Folds ~40% to 3-bets (re-jams ~37% in the real hands) |
| `D` | Seat 2, set at table start when we sit in seat 4 of 8 | Preflop all-ins showed AA/KK 10 times in 17 |

The reads are **self-correcting**:
- If the `J` seat starts 3-betting more than 14% of the time, it's untagged and its seeded fold-to-3-bet record is removed (its other seeds stay, as ordinary pseudo-observations).
- The `F` seed (11 folds in 12) is light enough that, after shrinkage, one called 4-bet bluff drops the measured fold-to-4-bet below the 80% trigger.

The seat-specific exploits (`X_TJAM`, `X_P85`) only fire once the `J` and `F` fingerprints both confirm that this really is that table.

---

## 3. Decision logic

### Preflop (`preflop`)
**Unopened pot**
- Opening threshold by number of players left to act (`OPEN`), widened or narrowed by how often *those specific players* fold to opens.
- Sizes: 2.2 bb (≤ 3 players behind) or 2.5 bb, +1 bb per limper, +1 bb when a loose player is behind (+0.5 bb from the small blind heads-up against the BB).
- **Any-two steal** when the expected fold equity makes it profitable.
- Against starter or always-fold bots, a small 2.2 bb open designed to get called by the starter bot's calling rule.
- Raises over limpers, especially loose ones; cheap limp-behind with pairs and suited hands.

**Facing a raise**
- Estimates the raiser's range width from its line (`_line_q`) and tightens it for each caller already in.
- Equity vs that range, with a **realisation factor** (position, hand quality) compared with pot odds.
- **3-bet for value** with hands far ahead of the raiser's range: 3× in position, 3.6× out of position, bigger vs irrational players.
- **Light 3-bets** in position vs openers who fold to 3-bets too often (randomised, ~40% of the time).
- **Any-two 3-bets from the blinds** only against the 3.0 bb opener (`J`): in the real hands, 3-bets from the BB against it got through 98% of the time.
- **Blind defence:** 3-bet value plus polarised suited bluffs vs late-position opens.
- **Small 4-bet bluffs** vs 3-bettors whose measured fold-to-4-bet is ≥ 80%, with the bluff remembered (`b4key`) so it doesn't keep bluffing postflop if called.

**All-in spots**
- Jam with ≥ 60% equity; call when equity beats pot odds + 3%.
- **Commit rule:** if *calling* would leave less than 0.8 pot behind, it's jam or fold, never flat.
- **Premiums (AA, KK, QQ, AK)** call shoves, *except* QQ/AK vs a seat whose shown shove range is ultra-tight; AA/KK always continue.
- At the Sunday table (`X_TJAM`), everything except AA/KK/QQ folds to the tight-jamming `D` seat.

### Postflop (`postflop`)
1. **Build each opponent's range (`_pool`):** start from their preflop range width, then reshape it with their postflop actions. After a bet, keep the top share of hands in proportion to how often they bet (adjusted by size), with bluffs weighted by their showdown history and size tell. After a call, thin out the weakest hands by how often they'd have folded. Flush and straight draws count as semi-strong on flop and turn. Random, always-raise and always-all-in bots get unfiltered ranges; the starter bot gets a range built from its known rules.
2. **Equity (`_equity`):** Monte Carlo against those ranges (up to 280 samples heads-up, 200 multiway), with **sequential early stopping**: it stops sampling as soon as the result is statistically clear of every decision threshold (±3.2σ). On the river heads-up it enumerates exactly against the sampled range.
3. **Checked to us:** evaluate check vs bets of 33/50/75/100% pot (plus 180% / all-in vs loose players or at low stack-to-pot ratio). EV = fold equity × pot + (when called) equity against the *calling* range − bet. Bluffs only against one or two opponents, never into stations or always-callers, never above pot size, with a bluff cost penalty. A bet must beat checking by 3% of the pot.
4. **Facing a bet:** call if equity minus a safety margin beats pot odds (margin is larger on the river and grows by 3% per player still to act). Raise for value with ≥ 62% equity, comparing a 75%-pot raise with all-in by EV.
5. **Starter bot heads-up:** bet exactly 2 bb on the flop and turn, which its rules always call.

### Guardrails learned from real hands
- **`X_RGUARD`:** if we've put chips in this street and get raised by a rational player, fold one pair or worse (in real hands, continuing lost 25 times out of 31), unless we hold a flush draw, or the raiser raises ≥ 40% of bets in general or ≥ 30% of *our* bets (it's caught on and is bluffing).
- **`X_GUARD`:** on the turn and river against rational players, one pair or worse never raises and never bets 180% or all-in; big turn/river bets from rational players are also read as rarely bluffs.
- **`X_FGUARD`:** on the flop against rational players, one pair or worse never raises more than 1.2 pot and never bets 180% or all-in.
- **Board-paired "two pair"** (one of the pairs on the board) counts as one pair when deciding whether to fold to a raise (0 wins in 7 live spots).
- **`X_P85`:** at the Sunday table, fold one pair to seat 6's pot-sized turn/river bets (only 22% / 6% weak at showdown).

### Controlled randomness
It isn't a fixed rulebook: light 3-bets, any-two 3-bets and 4-bet bluffs fire with set probabilities; **bet sizes are randomly chosen among near-best options** (`X_SIZEMIX`); and range sampling is random each time. Opponents can't map its sizes or frequencies precisely.

---

## 4. Speed and safety

- **Typical decision < 1 ms.** Preflop decisions are table lookups (~0.01 ms); postflop decisions typically take 0.1–0.7 ms.
- **Slow-decision guard:** any decision over 3.5 ms cuts the sample sizes by 30% (`self.scale`, floor 25%). The cut lasts for the rest of the round.
- **Thinking-bank budget:** it tracks total thinking time this round and plans the remaining samples per hand against a 5.5 s budget (half the 10 s bank, as a safety margin). If the pace projects over budget, it drops to 110 or 40 samples.
- **`legal()`** clamps every raise to `[min_raise_to, max_raise_to]`, converts impossible actions into the right legal one, and never "checks" into a bet by accident. It also nudges any raise that would match the starter bot's sizing formula by 1 chip, so other teams' starter-detection never misreads us.
- **`safe()`** is the fallback: check if possible, call tiny bets, otherwise fold.
- Every entry point (`act`, `on_hand_end`, `on_table_start`) is wrapped in try/except.
- Raises of ≥ 80% of the stack become all-in (no awkward, exploitable leftover stacks).

---

## 5. Feature switches (all A/B tested)

Each feature is a class-level switch, kept only if it won a paired A/B test with shared seeds:

| On | Feature |
|---|---|
| ✅ `X_MW` | Multiway value bets use per-opponent equity |
| ✅ `X_SIZEMIX` | Random choice among near-best bet sizes |
| ✅ `X_GUARD`, `X_FGUARD`, `X_RGUARD` | One-pair guardrails (see above) |
| ✅ `X_STARTER` | Exploit lines vs the starter-template bot |
| ✅ `X_STATION` | Bigger value bets, no bluffs vs calling stations |
| ✅ `X_LIGHT3`, `X_ATC3`, `X_BLIND3`, `X_4BX` | 3-bet / 4-bet aggression where opponents over-fold |
| ✅ `X_SIZETELL` | Per-seat bet-size tells from showdowns |
| ✅ `X_COMMIT` | Jam-or-fold when committed preflop |
| ✅ `X_TJAM`, `X_P85` | Sunday-table-specific reads |
| ❌ `X_TRAP`, `X_IMAGE`, `X_BBF`, `X_BRAISE` | Tested and switched **off** (no gain or negative); the code paths remain |
| ❌ `X_SEMI` | Tested and dropped; only the flag remains in this file |

Tunable constants: `OPEN` (open widths), `CALL_EQ`, `M_CALL`, `M_RIVER` (call margins), `RAISE_E` (value-raise threshold), `BLUFF_CUT`, `BET_EDGE`, `ATC_F/P`, `ATC_JONLY`, `FBX_F/P`.

---

## 6. How it was built

1. **Data first:** every real hand from Saturday's 54 counted rounds was parsed and verified, and each opponent was profiled. Practice-round data was excluded after it was found to distort the profiles: one bot was a VPIP-70 maniac in practice but VPIP-17 in counted rounds.
2. **Opponent clones:** each real bot was rebuilt as a clone matching its real stats, to form a replica of the Sunday table for testing.
3. **Paired A/B tests on shared seeds:** every feature had to beat the previous version on held-out seeds, and across several independent seed sets, before it was kept. That's why many ideas are switched off.
4. **Real-hand replays:** decisions were checked against what actually happened in the real hands (e.g. the jam-or-fold rule and the one-pair-vs-raise rule came from this).
5. **Safety gates:** fuzz testing (tens of thousands of random states, zero illegal actions), timing checks under load, and the organisers' local simulator, in no-limit, pot-limit, fixed-limit and capped-raise variants.

---

## Repository layout

```
Winning Bot.py                    the final bot (class Agent): this is what the README describes
CHANGELOG.md                      version log for iteration 3 (v1 → v31; v31 = Winning Bot.py)
Imperial AI Hackathon Starter kit/  the organisers' starter kit: engine, local_sim.py, example bots
iteration-1/                      first build (Saturday)
iteration-2/                      second build (Saturday night → Sunday morning)
iteration-3/                      third build (Sunday): every bot_v*.py version leading to the winning bot
simlab/                           training ground for analysing other teams' hands and simulating against them
agents/                           the Claude Code agent setup used to develop the bots
```

Each iteration folder is a self-contained working context with its own notes, so read its `CLAUDE.md` / `NOTES.md` / `CHANGELOG.md` first:

- **`iteration-1/`**: "OzanBot". `ozanbot.py` with snapshots in `versions/ozanbot_v0–v10`, teammates' bots in `bots/`, the evaluation arena, tuner and real-hand analysis in `tools/`, tuning state in `params/`, opponent and winners-vs-losers reports in `reports/`, and experiments in `scratch/`.
- **`iteration-2/`**: a rebuild against the Sunday Table C field. Clones of each real opponent (`clones/`), a paired-seed gauntlet and arena (`tools/`), synthetic aggressor bots and fuzz tests (`tests/`), and versions v1 → v5.1 (`versions/`, logged in `versions/CHANGELOG.md`). `PROGRESS.md`, `DECISIONS.md` and `reports/final.md` record the process.
- **`iteration-3/`**: the Sunday version line, `bot_v1.py` to `bot_v31.py`. `bot_v31.py` is identical to `Winning Bot.py`; the root `CHANGELOG.md` explains what changed in each version and why.
- **`simlab/`**: a clean copy of the starter kit (plus the starter-template bot) used as a sandbox for replaying other teams' hands and testing against them.
- **`agents/`**: `CLAUDE.md`, subagents (strategist, legality auditor, perf profiler, hand analyst), slash commands (`/plan-version`, `/gauntlet`, `/review`, `/promote`, `/ship-check`, `/analyse`), the post-edit hook and its `tools/check_bot.py` / `tools/gauntlet.py`. `SETUP.md` explains how it was installed.

Raw hand histories, simulation run logs, caches and the event's PDF (which holds team emails and the data token) are not included.

## Running it

```bash
python local_sim.py --rounds 1 --hands 1000 --seed 1   # with the official starter kit
```

The bot needs nothing but Python 3.9+ and has no dependencies. `DEBUG = True` prints a per-seat read-out to stderr every 100 hands.

## Limitations

- The Sunday table reads (`J`, `D`, `X_TJAM`, `X_P85`) assume that table's seat layout: we sit in seat 4 of 8. Elsewhere they stay dormant, because the seat and fingerprint checks never confirm, and the generic model plays.
- The `F` (3.2 bb opener) and `M` (2.5 bb opener plus shoves) tags are **not** tied to that table. Any seat at any table that matches the open-size fingerprint gets the seeded 3-bet / 4-bet reads, which can switch on 4-bet bluffs against it until its own record corrects them.
- The opponent model resets every round (a sandbox rule), so early-round reads rely on priors.
- The reads are tuned to this tournament's field of bots; against strong human players the exploitative assumptions wouldn't hold as well.

---

*Team Jump Street · Imperial AI Hack 2026.*
