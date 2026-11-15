"""Scratch pokerbot: opponent-model-first no-limit hold'em bot. Standard library only."""
import gc
import random
import time

DEBUG = False
_TBL = "AA 801 809 839 847 852 859 858 855 854 852;KK 622 702 709 727 744 750 769 801 816 825;QQ 449 611 631 660 678 698 714 743 782 800;JJ 274 530 563 606 638 661 681 705 748 775;TT 192 452 509 552 586 618 647 673 713 751;99 189 369 457 510 544 577 609 642 676 720;88 192 291 419 474 513 551 581 612 643 692;AKs 394 454 534 592 626 659 670 674 671 670;AQs 349 403 446 531 573 620 636 654 658 662;77 192 245 373 447 492 523 559 586 617 662;AJs 314 375 384 477 537 591 615 630 650 654;AKo 358 424 510 575 608 638 650 656 656 653;ATs 299 359 347 426 498 562 597 613 636 647;AQo 319 375 424 514 558 602 622 638 646 643;AJo 276 344 351 453 520 575 599 612 632 636;66 191 237 358 417 464 500 534 562 592 634;KQs 317 377 370 413 462 500 537 583 620 634;ATo 261 324 312 396 473 539 574 593 616 628;A9s 292 333 328 386 451 524 563 590 611 627;KJs 273 366 363 386 427 477 517 568 608 623;A8s 297 318 321 374 435 494 543 570 602 619;KTs 262 351 360 364 395 444 498 551 593 617;KQo 275 340 336 380 434 470 509 563 599 615;A7s 299 308 311 367 424 474 521 558 590 609;A9o 250 295 287 349 421 493 535 563 593 608;KJo 234 329 330 350 396 442 490 546 586 606;55 192 240 356 404 441 471 518 541 561 604;QJs 245 357 362 374 393 432 464 510 574 602;K9s 255 320 340 353 359 410 462 523 569 602;A6s 294 306 308 357 413 452 505 544 579 600;A5s 304 314 319 367 416 453 499 539 573 598;KTo 223 315 323 327 357 417 466 526 573 598;A8o 254 273 277 337 397 462 516 546 577 598;QTs 234 338 357 364 379 404 448 497 560 595;A7o 256 271 268 328 389 443 492 533 564 591;A4s 303 319 321 367 417 448 492 534 568 590;K8s 248 293 324 337 350 389 440 499 551 583;A3s 298 313 313 363 409 445 485 523 559 583;QJo 200 321 325 341 357 397 432 485 552 581;K9o 215 281 303 316 319 376 436 494 551 578;A5o 269 284 285 330 379 422 468 515 551 577;A6o 252 264 264 317 376 419 474 515 554 577;Q9s 231 308 336 356 364 381 417 470 539 576;JTs 207 334 356 367 376 401 427 462 534 575;K7s 254 290 316 338 351 382 432 485 544 574;QTo 194 303 320 332 344 376 417 472 541 573;A2s 296 307 306 358 401 438 480 518 551 572;44 190 239 355 399 427 463 496 521 540 570;A4o 268 280 278 327 376 415 461 503 541 566;K6s 252 293 319 333 349 380 419 475 530 564;A3o 264 274 278 329 376 411 460 498 535 562;Q8s 220 283 319 339 360 371 395 452 524 561;K8o 208 258 287 298 313 353 409 472 527 560;K5s 252 291 318 328 341 372 408 462 517 558;J9s 205 303 335 357 364 382 402 435 510 557;Q9o 189 272 300 321 326 348 383 443 515 553;JTo 167 302 324 334 352 371 398 438 509 553;K7o 215 253 282 303 312 347 397 460 518 551;A2o 259 271 268 321 371 410 450 495 522 550;K4s 249 286 318 326 339 375 402 452 510 549;K6o 214 254 281 296 307 346 385 443 505 543;Q7s 214 266 303 326 346 359 384 427 501 542;K3s 247 288 311 327 335 374 400 451 508 540;T9s 204 300 343 358 370 388 407 430 487 540;J8s 199 281 323 341 359 373 390 418 491 539;Q8o 180 242 284 305 323 333 363 420 496 537;33 183 234 344 394 423 455 475 493 512 536;Q6s 216 270 304 323 343 356 378 419 493 535;K2s 245 285 313 324 338 370 397 444 500 535;K5o 213 253 280 294 300 337 370 435 495 532;J9o 161 271 305 324 334 350 372 409 485 531;Q5s 215 269 303 323 339 352 377 411 484 528;J7s 187 258 301 328 345 358 374 397 474 526;K4o 210 253 281 290 302 340 372 425 487 524;T8s 198 271 328 347 363 378 394 409 470 523;Q4s 212 268 300 322 335 350 371 403 471 518;Q7o 172 227 261 291 310 320 342 393 473 517;J8o 157 241 284 308 322 340 357 386 461 515;T9o 161 260 308 321 334 354 367 398 460 515;K3o 206 248 276 288 299 332 365 415 478 513;Q6o 172 230 265 284 306 317 343 384 461 511;Q3s 208 264 295 316 332 349 366 397 462 509;T7s 190 258 309 330 349 365 381 393 452 508;98s 209 264 331 353 370 381 396 411 450 507;K2o 202 242 266 281 289 331 358 411 469 506;J6s 176 256 294 316 333 347 366 386 451 505;22 181 230 340 387 416 447 464 476 492 504;J5s 178 257 298 317 328 344 363 381 447 502;Q5o 176 233 267 286 301 316 339 376 454 501;Q2s 204 258 290 314 330 343 361 387 458 501;T8o 158 238 292 308 331 347 360 380 439 497;J7o 146 226 267 292 307 321 337 365 442 497;Q4o 167 227 262 281 300 312 333 369 443 492;97s 202 248 316 340 354 369 386 398 428 490;J4s 175 256 294 314 327 345 354 377 437 490;T6s 179 249 298 317 338 350 368 382 428 489;J3s 172 253 290 311 326 344 355 372 432 484;98o 168 224 291 319 336 346 361 373 417 482;Q3o 165 223 256 280 294 310 332 359 437 481;87s 215 241 315 344 366 374 391 402 426 479;T7o 149 218 270 294 315 329 346 360 418 479;J6o 135 219 258 276 294 309 326 352 423 478;J2s 168 251 287 306 320 339 350 364 422 474;Q2o 160 221 250 274 292 307 326 353 430 473;96s 194 241 302 327 346 357 377 384 412 473;T5s 168 240 288 304 322 333 356 366 411 473;J5o 136 221 259 281 291 308 326 344 414 472;T4s 167 240 293 304 323 339 355 370 408 464;97o 163 213 275 308 325 335 349 364 400 463;J4o 136 219 256 278 294 307 321 340 406 462;86s 206 233 307 332 352 362 378 389 404 462;T6o 141 215 262 282 302 316 334 347 402 460;95s 182 236 292 319 328 343 359 372 397 457;T3s 163 235 288 305 319 338 347 363 401 456;76s 222 238 306 341 362 371 384 399 410 454;J3o 132 219 253 273 289 302 315 337 398 453;87o 178 204 277 308 329 343 361 371 392 451;T2s 159 233 280 292 312 331 340 351 388 448;85s 198 228 297 323 341 349 368 378 393 446;96o 155 205 268 292 307 323 338 349 384 445;J2o 122 208 245 266 282 300 315 330 391 443;T5o 125 203 253 270 283 300 319 330 378 443;94s 162 217 276 304 315 327 339 352 377 439;75s 209 229 298 331 348 360 378 384 397 436;T4o 124 201 251 266 285 303 313 331 371 435;86o 167 198 266 294 316 330 343 353 375 433;65s 222 240 303 333 351 365 382 392 399 432;93s 165 221 279 304 317 331 342 351 376 431;84s 181 212 282 311 326 341 350 362 378 427;95o 140 194 256 280 292 304 326 334 362 427;T3o 120 199 245 262 280 299 309 322 363 425;92s 160 212 276 303 313 328 339 346 373 425;76o 182 199 271 301 325 337 355 363 377 421;74s 191 215 281 314 334 346 357 371 381 418;T2o 116 195 241 261 279 296 304 317 360 417;54s 223 245 308 332 347 362 376 386 393 416;64s 209 231 297 323 343 356 372 382 388 414;85o 156 187 257 287 302 316 332 341 358 413;83s 165 200 270 297 316 328 339 345 361 408;94o 124 182 241 267 278 296 305 319 340 405;82s 161 194 268 295 314 331 337 346 359 404;75o 170 192 257 290 308 319 337 348 357 404;73s 175 200 267 302 322 333 343 352 362 401;65o 185 201 268 297 316 327 347 357 366 400;93o 123 178 238 270 277 298 304 317 341 400;84o 138 172 243 273 289 306 316 325 340 397;53s 207 233 296 320 334 351 361 367 377 396;63s 192 215 279 307 327 338 352 359 366 396;92o 118 172 235 266 276 291 298 310 334 390;43s 199 224 289 313 328 345 351 363 369 386;74o 154 176 246 283 299 313 322 334 341 386;54o 184 209 270 297 314 328 342 351 357 382;64o 169 190 259 288 303 322 332 340 349 381;72s 159 184 252 285 303 317 327 334 346 380;62s 172 200 263 292 314 326 338 339 353 378;52s 190 214 277 304 320 337 345 349 360 377;83o 123 158 230 257 278 292 301 312 321 376;82o 118 153 223 252 274 287 296 304 319 369;42s 185 211 276 304 318 337 340 351 359 368;73o 133 160 226 261 280 292 305 312 324 366;53o 166 193 256 281 300 314 324 331 340 363;32s 183 209 273 299 313 332 337 343 353 360;63o 149 175 242 269 289 303 313 323 330 359;43o 162 188 255 282 296 311 318 334 335 352;72o 121 149 216 252 271 286 292 301 308 345;52o 149 178 244 270 286 299 311 316 325 343;62o 131 159 225 255 276 292 300 307 313 340;42o 143 170 237 263 280 295 303 310 316 331;32o 143 173 240 265 283 299 302 308 315 323"


# ----------------------------------------------------------------- cards
RANKS = "23456789TJQKA"
SUITS = "cdhs"
CARD = {r + s: (i << 2) | j for i, r in enumerate(RANKS) for j, s in enumerate(SUITS)}
P5 = [5 ** (c >> 2) for c in range(52)]
S8 = [8 ** (c & 3) for c in range(52)]
RBIT = [1 << (c >> 2) for c in range(52)]

STRAIGHT = [-1] * 8192
for _m in range(8192):
    _w = (_m << 1) | ((_m >> 12) & 1)
    for _top in range(12, 2, -1):
        if (_w >> (_top - 3)) & 31 == 31:
            STRAIGHT[_m] = _top
            break
FLV = [0] * 8192
for _m in range(8192):
    if bin(_m).count("1") >= 5:
        if STRAIGHT[_m] >= 0:
            FLV[_m] = (8 << 20) | (STRAIGHT[_m] << 16)
        else:
            _v = 5
            _k = 0
            for _r in range(12, -1, -1):
                if (_m >> _r) & 1:
                    _v = (_v << 4) | _r
                    _k += 1
                    if _k == 5:
                        break
            FLV[_m] = _v
FSUIT = [-1] * 4096
for _i in range(4096):
    for _s in range(4):
        if ((_i >> (3 * _s)) & 7) >= 5:
            FSUIT[_i] = _s
NF = {}


def _nf(cards):
    """Hand value ignoring flushes (5 to 7 cards)."""
    cnt = [0] * 13
    mask = 0
    for c in cards:
        r = c >> 2
        cnt[r] += 1
        mask |= 1 << r
    q = -1
    t = []
    p = []
    s = []
    for r in range(12, -1, -1):
        n = cnt[r]
        if n == 4:
            q = r
        elif n == 3:
            t.append(r)
        elif n == 2:
            p.append(r)
        elif n == 1:
            s.append(r)
    if q >= 0:
        k = 0
        for r in range(12, -1, -1):
            if cnt[r] and r != q:
                k = r
                break
        return (7 << 20) | (q << 16) | (k << 12)
    if t and (len(t) > 1 or p):
        pr = t[1] if len(t) > 1 else -1
        if p and p[0] > pr:
            pr = p[0]
        return (6 << 20) | (t[0] << 16) | (pr << 12)
    sh = STRAIGHT[mask]
    if sh >= 0:
        return (4 << 20) | (sh << 16)
    if t:
        return (3 << 20) | (t[0] << 16) | (s[0] << 12) | (s[1] << 8)
    if len(p) >= 2:
        k = s[0] if s else 0
        if len(p) > 2 and p[2] > k:
            k = p[2]
        return (2 << 20) | (p[0] << 16) | (p[1] << 12) | (k << 8)
    if p:
        return (1 << 20) | (p[0] << 16) | (s[0] << 12) | (s[1] << 8) | (s[2] << 4)
    return (s[0] << 16) | (s[1] << 12) | (s[2] << 8) | (s[3] << 4) | s[4]


def ev7(cards):
    k = 0
    s = 0
    for c in cards:
        k += P5[c]
        s += S8[c]
    v = NF.get(k)
    if v is None:
        v = NF[k] = _nf(cards)
    fs = FSUIT[s]
    if fs >= 0:
        m = 0
        for c in cards:
            if c & 3 == fs:
                m |= RBIT[c]
        f = FLV[m]
        if f > v:
            return f
    return v


# ------------------------------------------------------- preflop tables
QG = (0.02, 0.04, 0.07, 0.11, 0.16, 0.24, 0.35, 0.5, 0.75, 1.0)
ORDER = []
EQT = {}
PCT = {}
COMBOS = []
CLS = {}


def _cname(a, b):
    ra, rb = a >> 2, b >> 2
    if ra < rb:
        ra, rb = rb, ra
    if ra == rb:
        return RANKS[ra] + RANKS[rb]
    return RANKS[ra] + RANKS[rb] + ("s" if (a & 3) == (b & 3) else "o")


def _build():
    by = {}
    for a in range(52):
        for b in range(a + 1, 52):
            c = _cname(a, b)
            by.setdefault(c, []).append((a, b))
            CLS[(a, b)] = c
            CLS[(b, a)] = c
    for item in _TBL.split(";"):
        parts = item.split()
        ORDER.append(parts[0])
        EQT[parts[0]] = [int(x) / 1000.0 for x in parts[1:]]
    cum = 0
    for c in ORDER:
        n = len(by[c])
        PCT[c] = (cum + n / 2.0) / 1326.0
        cum += n
        COMBOS.extend(by[c])


_build()
NOPAIR_NOAK = [(a, b) for (a, b) in COMBOS if (a >> 2) != (b >> 2) and (a >> 2) < 11 and (b >> 2) < 11]
PAIR_AK = [(a, b) for (a, b) in COMBOS if (a >> 2) == (b >> 2) or (a >> 2) >= 11 or (b >> 2) >= 11]
gc.collect()
gc.freeze()


def eq_vs(cls, q):
    t = EQT[cls]
    if q <= QG[0]:
        return t[0]
    for i in range(1, 10):
        if q <= QG[i]:
            w = (q - QG[i - 1]) / (QG[i] - QG[i - 1])
            return t[i - 1] * (1 - w) + t[i] * w
    return t[9]


SI = {"preflop": 0, "flop": 1, "turn": 2, "river": 3}
FOLD, CALL, RAISE, CHECK = 0, 1, 2, 3


def parse(history, n, bb):
    """-> events (seat, street, act, to_call, pot_before, size_frac, raises_before, amount, starter_formula)."""
    bets = [0] * n
    pot = 0
    cur = 0
    st = "preflop"
    raises = 0
    last = bb
    out = []
    for h in history:
        s = h["seat"]
        a = h["action"]
        amt = h.get("amount") or 0
        if h["street"] != st:
            st = h["street"]
            bets = [0] * n
            cur = 0
            raises = 0
            last = bb
        if a == "small_blind" or a == "big_blind":
            bets[s] += amt
            pot += amt
            if bets[s] > cur:
                cur = bets[s]
            continue
        tc = cur - bets[s]
        si = SI[st]
        if a == "raise":
            x = (amt - cur) / float(max(1, pot + tc))
            out.append((s, si, RAISE, tc, pot, x, raises, amt, amt == cur + max(last, bb) + pot // 2))
            if amt - cur > last:
                last = amt - cur
            pot += amt - bets[s]
            bets[s] = amt
            cur = amt
            raises += 1
        elif a == "call":
            out.append((s, si, CALL, tc, pot, tc / float(max(1, pot)), raises, amt, False))
            bets[s] += amt
            pot += amt
        elif a == "fold":
            out.append((s, si, FOLD, tc, pot, tc / float(max(1, pot)), raises, 0, False))
        else:
            out.append((s, si, CHECK, 0, pot, 0.0, raises, 0, False))
    return out


# -------------------------------------------------------------- OppBook
# fold priors [commitment state][size bucket <0.4, 0.4-0.9, >0.9 pot] (real tournament data)
FPRI = ((0.40, 0.55, 0.74), (0.22, 0.42, 0.58), (0.25, 0.47, 0.58))   # refit: ~25k real decisions, size = call / pot before the bet
NOISE = ("always_raise", "always_allin", "random")


def bucket(x):
    return 0 if x < 0.4 else (1 if x < 0.9 else 2)


class Seat(object):
    def __init__(self):
        self.vp = 0
        self.pfr = 0
        self.tb = 0
        self.tbo = 0
        self.sh = 0
        self.fo = [0, 0]      # facing one open: folds, chances
        self.f3 = [0, 0]      # raised, then re-raised: folds, chances
        self.f4 = [0, 0]      # 3-bet, then faced a non-all-in 4-bet: folds, chances
        self.bbf = [0, 0]     # in the big blind facing one raise: folds, chances
        self.bk = [0, 0]      # postflop checked to: bets, chances
        self.rz = [0, 0]      # postflop facing a bet: raises, chances
        self.ff = [[[0, 0], [0, 0], [0, 0]] for _ in range(3)]   # folds, chances by state x size
        self.dev = [0.0, 0]   # sum(fold - prior), n
        self.devs = [[0.0, 0], [0.0, 0], [0.0, 0], [0.0, 0]]   # the same per street
        self.bsdz = [[0, 0], [0, 0]]   # showdowns after betting small / big (>= 0.7 pot): weak, n
        self.fcr = [0, 0, 0]  # facing any bet: fold, call, raise
        self.acts = [0, 0]    # raises, all voluntary actions
        self.ai = 0           # hands all-in
        self.stm = [0, 0]     # raises matching the starter formula, raises
        self.sd = {"C": [0, 0.0], "R": [0, 0.0], "3": [0, 0.0], "S": [0, 0.0]}
        self.bsd = [0, 0]     # showdowns after betting postflop: weak hands, n
        self.csd = [0, 0]     # showdowns after only calling postflop: weak hands, n
        self.osz = {}         # open sizes (tenths of a bb) -> count
        self.bsz = [0.0, 0]   # postflop bet size: sum of pot fractions, n
        self.kind = None
        self.species = None
        self.won = 0.0        # chips we won from this seat in heads-up pots
        self.hu = 0
        self.ourf = [[0, 0], [0, 0], [0, 0]]   # folds, chances vs OUR bets by size bucket
        self.ourr = [0, 0]   # answers to our postflop bets: raises, n
        self.tag = None       # scouting: recognised opponent ("J", "F", "M") once its open-size fingerprint is seen


class OppBook(object):
    def __init__(self, n):
        self.n = n
        self.hands = 0
        self.seat = [Seat() for _ in range(max(n, 10))]
        self.pfr_seat = None     # this hand's preflop aggressor (set by the agent each postflop decision)

    # --- frequencies (shrunk toward priors)
    def vpip(self, i):
        return (self.seat[i].vp + 2.5) / (self.hands + 10.0)

    def rat(self, i):
        """How strength-driven this seat's continuing ranges are (1 = rational, 0 = any two)."""
        k = self.seat[i].kind
        if k in NOISE or k == "always_call":
            return 0.1
        return max(0.1, min(0.95, 1.3 - 1.6 * self.vpip(i)))

    def _sd(self, i, line, q):
        n, s = self.seat[i].sd[line]
        if n >= 2:
            q2 = min(1.0, 2.2 * s / n)
            w = n / (n + 5.0)
            if q2 > q or n >= 5:
                q = (1 - w) * q + w * q2
        return min(1.0, q)

    def open_q(self, i):
        o = self.seat[i]
        return self._sd(i, "R", min(1.0, 2.2 * max(0.04, (o.pfr + 1.6) / (self.hands + 12.0))))

    def tb_q(self, i):
        o = self.seat[i]
        return self._sd(i, "3", min(1.0, 1.7 * max(0.015, (o.tb + 0.8) / (o.tbo + 14.0))))

    def shove_q(self, i):
        o = self.seat[i]
        return self._sd(i, "S", min(1.0, 3.0 * max(0.012, (o.sh + 0.4) / (self.hands + 20.0))))

    def call_q(self, i):
        return min(1.0, self.vpip(i) * 1.6)

    def fold_open(self, i):
        o = self.seat[i]
        return (o.fo[0] + 0.8 * 8) / (o.fo[1] + 8.0)

    def fold_bb(self, i):
        o = self.seat[i]
        return (o.bbf[0] + 0.7 * 6) / (o.bbf[1] + 6.0)

    def fold_3bet(self, i):
        o = self.seat[i]
        return (o.f3[0] + 0.55 * 6) / (o.f3[1] + 6.0)

    def fold_4bet(self, i):
        o = self.seat[i]
        return (o.f4[0] + 0.5 * 4) / (o.f4[1] + 4.0)

    def bet_freq(self, i):
        o = self.seat[i]
        return (o.bk[0] + 0.36 * 8) / (o.bk[1] + 8.0)

    def raise_freq(self, i):
        o = self.seat[i]
        return (o.rz[0] + 0.08 * 12) / (o.rz[1] + 12.0)

    PFR_F = (0.57, 0.80, 0.81)   # fold-rate ratio preflop raiser / other players by bet size (real counted hands)
    SZ_PRIOR = None       # (small, big) prior weak share by bet size, or None

    def bluffy(self, i, big=None):
        """Share of weak hands this seat showed after betting (0.3 prior); big = for its big / small bets."""
        o = self.seat[i]
        b = (o.bsd[0] + 0.3 * 4) / (o.bsd[1] + 4.0)
        if big is not None:
            z = o.bsdz[1 if big else 0]
            if self.SZ_PRIOR:
                b = 0.5 * b + 0.5 * self.SZ_PRIOR[1 if big else 0]   # real showdowns: small bets weak, big bets strong
            b = (z[0] + b * 3) / (z[1] + 3.0)     # size tell: the seat's own record at this bet size
        return b

    SCOUT = 1

    def identify(self, i):
        """Sunday table scouting: recognise known bots by their fixed open size and pre-load what their real hands
        showed (pseudo-observations, so the seat's own play in this round still overrides them)."""
        o = self.seat[i]
        norm = {}
        shoves = 0
        for k, v in o.osz.items():
            if k >= 500:
                shoves += v
            else:
                norm[k] = v
        tot = sum(norm.values())
        if o.tag == "J" and o.tbo >= 15 and o.tb > 0.14 * o.tbo:
            o.tag = "x"                       # 3-bets too much to be the bot we scouted: drop the seeded reads
            o.f3[0] -= 17; o.f3[1] -= 20
            return
        if o.tag or tot < 3:
            return
        k = max(norm, key=norm.get)
        share = norm[k] / float(tot)
        if k == 30 and share >= 0.9 and tot >= 4 and self.n == 8 and getattr(self, "me", -1) == 4 and i == 7:
            o.tag = "J"                       # opens exactly 3.0 bb: folds 85% to 3-bets, shoves only QQ+,
            o.f3[0] += 17; o.f3[1] += 20      # passive station postflop (its bets are strong)
            o.sd["S"][0] += 5; o.sd["S"][1] += 0.05
            o.bk[0] += 3; o.bk[1] += 12
            o.bsd[0] += 1; o.bsd[1] += 8
            o.dev[0] -= 1.8; o.dev[1] += 12
        elif k == 32 and share >= 0.7:
            o.tag = "F"                       # opens 3.2 bb, very wide (no shove seed: its 3-bet jams are QQ+/AK,
                                              # only its re-jams are wide, and the seat's own shown hands say which)
            o.f3[0] += 12; o.f3[1] += 20
            o.f4[0] += 11; o.f4[1] += 12      # folds 92% to small 4-bets (176 real cases, every round); one failure switches it off
        elif k == 25 and shoves >= 2 and norm[k] >= 2:
            o.tag = "M"                       # 2.5 bb opens plus open-shoves; re-jams 37% vs 3-bets (no shove seed)
            o.f3[0] += 8; o.f3[1] += 20

    def species(self, i):
        """Fingerprint from open size and bet size (for the debug report and size-tell priors)."""
        o = self.seat[i]
        if o.kind:
            return o.kind
        tot = sum(o.osz.values())
        op = max(o.osz, key=o.osz.get) / 10.0 if tot >= 3 else None
        mb = o.bsz[0] / o.bsz[1] if o.bsz[1] >= 4 else None
        if mb is not None and mb >= 0.72:
            return "bigbet"
        if mb is not None and mb <= 0.40:
            return "smallball"
        if self.hands >= 30 and self.vpip(i) < 0.13:
            return "nit"
        if self.station(i):
            return "station"
        if op is None or mb is None:
            return None
        return "open%.1f_bet%.2f" % (op, mb)

    def sticky(self, i):
        """Share of weak hands this seat showed after calling down (0.35 prior)."""
        o = self.seat[i]
        return (o.csd[0] + 0.35 * 4) / (o.csd[1] + 4.0)

    def pfold(self, i, x, state, street, weak, bet_chips, bb):
        """P(seat i folds to a bet of x pots). state: 0 fresh, 1 called earlier, 2 bet/raised earlier."""
        o = self.seat[i]
        k = o.kind
        if k == "always_call" or k == "always_raise" or k == "always_allin":
            return 0.02
        if k == "always_fold":
            return 0.95
        if k == "starter":
            return 0.97 if (bet_chips > 2 * bb and state < 2) else 0.0
        if k == "random":
            return 0.33
        b = bucket(x)
        base = FPRI[state][b]
        dn = o.dev[1]
        if dn:
            d = o.dev[0] / (dn + 8.0)
            ds = o.devs[street]
            d = (ds[0] + 4.0 * d) / (ds[1] + 4.0)       # this street's own record, shrunk to the seat's overall one
            base = max(0.02, min(0.95, base + d))
        c = o.ff[state][b]
        f = (c[0] + base * 5) / (c[1] + 5.0)
        of = o.ourf[b]
        if of[1] >= 3 and not (o.hu >= 40 and o.won < -40 * bb):      # how it has answered OUR bets of this size
            w = of[1] / (of[1] + 6.0)
            f = (1 - w) * f + w * (of[0] / float(of[1]))
        if state == 0 and weak and street >= 2:
            f += (1 - f) * 0.25       # checked a street: gives up more
        elif state == 0 and self.PFR_F and i == self.pfr_seat and not weak:
            f *= self.PFR_F[b]        # the preflop raiser folds less to a lead (real: 0.23 / 0.44 / 0.60)
        if x > 1.6:
            f += (0.9 - f) * 0.25 * self.rat(i)
        return max(0.0, min(0.95, f))

    def classify(self, i):
        o = self.seat[i]
        n = self.hands
        if n < 6:
            return None
        nf = o.fcr[0] + o.fcr[1] + o.fcr[2]
        if o.stm[1] >= 3 and o.stm[0] >= 0.85 * o.stm[1]:
            return "starter"
        if o.vp == 0 and o.acts[0] == 0 and nf >= 3 and o.fcr[0] >= 0.9 * nf:
            return "always_fold"
        if o.ai >= 0.7 * n:
            return "always_allin"
        if o.acts[1] >= 8 and o.acts[0] >= 0.85 * o.acts[1]:
            return "always_raise"
        if nf >= 8 and o.fcr[1] >= 0.9 * nf and o.acts[0] <= 0.05 * o.acts[1]:
            return "always_call"
        if nf >= 20 and o.vp >= 0.45 * n:
            lo, hi = 0.18 * nf, 0.50 * nf
            if lo <= o.fcr[0] <= hi and lo <= o.fcr[1] <= hi and lo <= o.fcr[2] <= hi:
                return "random"
        return None

    def station(self, i):
        o = self.seat[i]
        if o.kind == "always_call":
            return True
        nf = o.fcr[0] + o.fcr[1] + o.fcr[2]
        post = sum(c[1] for st in o.ff for c in st)
        pf = sum(c[0] for st in o.ff for c in st)
        return post >= 10 and pf <= 0.22 * post and o.rz[0] <= 0.12 * max(1, o.rz[1]) and nf >= 10

    # --- learning
    def learn(self, summary, me, bb, S0):
        self.me = me
        n = self.n
        hist = summary.get("history") or []
        evs = parse(hist, n, bb)
        seat = self.seat
        vp = set()
        pfr = set()
        line = {}
        raised = set()
        faced_open = set()
        tbo = set()
        cstate = {}
        post_bet = set()
        post_call = set()
        limp = False
        maxbet = {}
        bbs = -1
        for h in hist:
            if h["action"] == "big_blind":
                bbs = h["seat"]
                break
        our_bet = None      # (street, bucket) of our latest bet awaiting answers
        tb3 = -1            # seat that 3-bet this hand
        curb = 0            # latest preflop raise-to
        answered = set()
        for (s, st, a, tc, pot, x, raises, amt, stf) in evs:
            o = seat[s]
            if a != CHECK or tc > 0:
                o.acts[1] += 1
            if a == RAISE:
                o.acts[0] += 1
                o.stm[1] += 1
                if stf:
                    o.stm[0] += 1
            if tc > 0 and a != CHECK:
                o.fcr[a] += 1
            if st == 0:
                if a == CALL and tc > 0 or a == RAISE:
                    vp.add(s)
                if a == CALL and raises == 0:
                    limp = True
                if a == RAISE:
                    pfr.add(s)
                    lv = "S" if amt >= S0 // 2 else ("3" if raises >= 1 else "R")
                    if lv == "S":
                        o.sh += 1
                    if raises >= 1:
                        o.tb += 1
                    elif not limp:
                        key = int(round(amt * 10.0 / bb))
                        o.osz[key] = o.osz.get(key, 0) + 1
                    if "CR3S".index(lv) > "CR3S".index(line.get(s, "C")):
                        line[s] = lv
                if raises >= 1 and tc > 0:
                    if s in raised:
                        o.f3[1] += 1
                        if a == FOLD:
                            o.f3[0] += 1
                        if s == tb3 and raises == 3 and curb < 0.4 * S0:
                            o.f4[1] += 1
                            if a == FOLD:
                                o.f4[0] += 1
                    elif raises == 1 and s not in faced_open:
                        faced_open.add(s)
                        o.fo[1] += 1
                        if a == FOLD:
                            o.fo[0] += 1
                        if s == bbs:
                            o.bbf[1] += 1
                            if a == FOLD:
                                o.bbf[0] += 1
                    if s not in tbo:
                        tbo.add(s)
                        o.tbo += 1
                if a == RAISE:
                    raised.add(s)
                    curb = amt
                    if raises == 1:
                        tb3 = s
            else:
                if tc > 0:
                    if a != CHECK:
                        b = bucket(tc / float(max(1, pot - tc)))     # same scale pfold() is queried with
                        k = cstate.get(s, 0)
                        c = o.ff[k][b]
                        c[1] += 1
                        o.rz[1] += 1
                        if a == FOLD:
                            c[0] += 1
                        elif a == RAISE:
                            o.rz[0] += 1
                        o.dev[0] += (1.0 if a == FOLD else 0.0) - FPRI[k][b]
                        o.dev[1] += 1
                        o.devs[st][0] += (1.0 if a == FOLD else 0.0) - FPRI[k][b]
                        o.devs[st][1] += 1
                        if our_bet is not None and our_bet[0] == st and s != me and s not in answered:
                            answered.add(s)
                            of = o.ourf[our_bet[1]]
                            of[1] += 1
                            o.ourr[1] += 1
                            if a == RAISE:
                                o.ourr[0] += 1
                            if a == FOLD:
                                of[0] += 1
                else:
                    o.bk[1] += 1
                    if a == RAISE:
                        o.bk[0] += 1
                if a == RAISE:
                    cstate[s] = 2
                    post_bet.add(s)
                    if x > maxbet.get(s, 0.0):
                        maxbet[s] = x
                    o.bsz[0] += min(3.0, x)
                    o.bsz[1] += 1
                    if s == me:
                        our_bet = (st, bucket(x))
                        answered = set()
                    else:
                        our_bet = None
                elif a == CALL and tc > 0:
                    if cstate.get(s, 0) < 2:
                        cstate[s] = 1
                    post_call.add(s)
        # all-in hands
        put = [0] * n
        sb_ = [0] * n
        cst = "preflop"
        for h in hist:
            s = h["seat"]
            a = h["action"]
            if h["street"] != cst:
                cst = h["street"]
                sb_ = [0] * n
            amt = h.get("amount") or 0
            if a == "raise":
                put[s] += amt - sb_[s]
                sb_[s] = amt
            elif a in ("call", "small_blind", "big_blind"):
                put[s] += amt
                sb_[s] += amt
        for s in range(n):
            if put[s] >= S0:
                seat[s].ai += 1
        for s in vp:
            seat[s].vp += 1
        for s in pfr:
            seat[s].pfr += 1
        shown = summary.get("shown") or {}
        board = [CARD[c] for c in (summary.get("board") or []) if c in CARD]
        for s, cards in shown.items():
            s = int(s)
            if s == me or len(cards) != 2:
                continue
            a, b = CARD[cards[0]], CARD[cards[1]]
            d = seat[s].sd[line.get(s, "C")]
            d[0] += 1
            d[1] += PCT[CLS[(a, b)]]
            if len(board) == 5 and (s in post_bet or s in post_call):
                v = ev7(board + [a, b])
                top = max(c >> 2 for c in board)
                pr = (v >> 16) & 15
                weak = v < (1 << 20) or ((v >> 20) == 1 and (pr < top or (pr != a >> 2 and pr != b >> 2)))
                t = seat[s].bsd if s in post_bet else seat[s].csd
                t[1] += 1
                if weak:
                    t[0] += 1
                if s in post_bet:
                    z = seat[s].bsdz[1 if maxbet.get(s, 0.0) >= 0.7 else 0]
                    z[1] += 1
                    if weak:
                        z[0] += 1
        # chips won from a seat heads-up
        stacks = summary.get("stacks") or []
        if len(stacks) >= n:
            d_me = stacks[me] - S0
            inv = [s for s in range(n) if s != me and abs(stacks[s] - S0) > bb]
            if d_me and len(inv) == 1:
                seat[inv[0]].won += d_me
                seat[inv[0]].hu += 1
        self.hands += 1
        for s in range(n):
            if s != me:
                seat[s].kind = self.classify(s)
                if self.SCOUT:
                    self.identify(s)


# ---------------------------------------------------------------- Agent
class Agent:
    # switches (each one can be turned off if its A/B fails)
    X_MW = 1           # multiway value bets use per-opponent equity
    X_SIZEMIX = 1      # sample among near-best bet sizes
    X_GUARD = 1        # vs rational players on turn/river: no raises/overbets with one pair or worse
    X_STARTER = 1      # starter-bot exploit lines
    X_STATION = 1      # bigger value bets vs calling stations, no bluffs
    X_TRAP = 0         # check strong hands to an aggressive player behind
    X_IMAGE = 0        # image shift: more bluffs after hand 120 vs seats that fold
    X_LIGHT3 = 1       # light 3-bets vs openers who fold to 3-bets
    X_SIZETELL = 1     # per-seat size tells from showdowns (big vs small bets)
    X_BBF = 0          # OFF (A/B: fewer steals, no gain). Steal EV uses the big blind's own fold-to-raise record
    X_COMMIT = 1       # big preflop reraise leaving < 0.8 pot behind: jam or fold, never flat (real-hand replay)
    X_FGUARD = 1       # flop vs rational players: no overbet / all-in bets or raises with one pair or worse
    X_ATC3 = 1         # 3-bet any two vs an opener whose fold-to-3-bet stays >= ATC_F (self-correcting: uses the seat's record)
    ATC_F = 0.75
    ATC_P = 0.85
    ATC_JONLY = 1      # ... only from the blinds and only vs the 3.0 bb opener: real hands, everyone folds 98% (BB) / 81% (SB);
                       # vs the other openers and from the button it was break-even or worse in the worst case
    b4key = None       # hole cards of a hand in which we made the any-hand 4-bet (it was called: play it carefully)
    X_P85 = 1          # Sunday bucket table only: fold one pair or less to seat 6's pot-sized turn/river bets
    X_TJAM = 1         # fold everything but AA/KK to the tight-jamming seat of the Sunday bucket table
    X_4BX = 1          # 4-bet small (any hand) over a 3-bettor whose measured fold-to-4-bet is >= FBX_F; self-correcting
    FBX_F = 0.80
    FBX_P = 0.9
    X_RGUARD = 1       # our bet got raised: fold one pair or worse (real hands, both days: continuing lost 25 times in 31)
    X_BLIND3 = 1       # blinds vs late opens: 3-bet value + suited bluffs (top teams win in the blinds); SB: 3-bet or fold more
    X_SEMI = 0         # flop: raise strong draws heads-up instead of calling
    X_BRAISE = 0       # bluff-raise small bets from seats seen folding to raises after betting
    OPEN = (0.50, 0.50, 0.45, 0.34, 0.25, 0.18, 0.14, 0.12, 0.11, 0.11)   # open width by players behind
    CALL_EQ = 0.41
    M_CALL = 0.04
    M_RIVER = 0.045
    RAISE_E = 0.62
    BLUFF_CUT = 0.05
    BET_EDGE = 0.03

    def __init__(self):
        self.rng = random.Random()
        self.n = 8
        self.me = 0
        self.nhands = 1000
        self.S0 = 2000
        self.bb = 20
        self.book = OppBook(8)
        self.spent = 0.0
        self.scale = 1.0
        gc.collect()
        gc.freeze()
        gc.disable()

    def on_table_start(self, info):
        try:
            self.me = int(info.get("seat", 0) or 0)
            self.n = int(info.get("num_players", 8) or 8)
            self.nhands = int(info.get("hands", 1000) or 1000)
            self.S0 = int(info.get("starting_stack", 2000) or 2000)
            self.bb = int(info.get("big_blind", 20) or 20)
        except Exception:
            pass
        self.book = OppBook(self.n)
        try:
            if self.X_TJAM and self.n == 8 and self.me == 4:
                self.book.seat[2].tag = "D"      # Sunday bucket table: this seat's preflop all-ins showed AA/KK 10 times in 17
        except Exception:
            pass

    def on_hand_end(self, summary):
        self.b4key = None
        try:
            self.book.learn(summary, self.me, self.bb, self.S0)
            if DEBUG and self.book.hands % 100 == 0:
                self._debug()
        except Exception:
            if DEBUG:
                raise

    def _debug(self):
        bk = self.book
        out = ["-- hand %d (seat %d)" % (bk.hands, self.me)]
        for i in range(self.n):
            if i == self.me:
                continue
            o = bk.seat[i]
            out.append("  seat %d kind=%s vpip=%.2f open_q=%.2f f3b=%.2f betf=%.2f fold=%s ourf=%s won=%+.0f/%d" % (
                i, bk.species(i), bk.vpip(i), bk.open_q(i), bk.fold_3bet(i), bk.bet_freq(i),
                [round(bk.pfold(i, x, 0, 1, False, 100, 20), 2) for x in (0.33, 0.6, 1.0)], o.ourf, o.won, o.hu))
        import sys
        sys.stderr.write("\n".join(out) + "\n")

    # ------------------------------------------------------------- act
    def act(self, state):
        t0 = time.perf_counter()
        try:
            if state["street"] == "preflop":
                r = self.preflop(state)
            else:
                r = self.postflop(state)
        except Exception:
            if DEBUG:
                raise
            r = None
        try:
            r = self.legal(state, r)
        except Exception:
            r = self.safe(state)
        dt = time.perf_counter() - t0
        self.spent += dt
        if dt > 0.0035:
            self.scale = max(0.25, self.scale * 0.7)
        return r

    @staticmethod
    def safe(state):
        try:
            legal = state.get("legal_actions") or []
            if "check" in legal:
                return {"action": "check"}
            if "call" in legal and (state.get("to_call") or 0) <= 0.2 * (state.get("pot") or 0):
                return {"action": "call"}
        except Exception:
            pass
        return {"action": "fold"}

    def legal(self, state, r):
        legal = state["legal_actions"]
        if not isinstance(r, dict):
            return self.safe(state)
        a = r.get("action")
        tc = state.get("to_call") or 0
        if a == "raise":
            lo, hi = state.get("min_raise_to"), state.get("max_raise_to")
            if "raise" not in legal or lo is None or hi is None:
                a = "call" if tc > 0 else "check"
            else:
                lo, hi = int(lo), int(hi)
                try:
                    amt = int(r.get("amount"))
                except Exception:
                    amt = lo
                amt = max(lo, min(hi, amt))
                if amt == lo + (state.get("pot") or 0) // 2 and amt < hi:
                    amt += 1          # never look like the starter bot
                return {"action": "raise", "amount": amt}
        if a == "call":
            if tc > 0 and "call" in legal:
                return {"action": "call"}
            a = "check"
        if a == "check":
            return {"action": "check"} if "check" in legal else self.safe(state)
        if a == "fold":
            return {"action": "check"} if "check" in legal else {"action": "fold"}
        return self.safe(state)

    def _r(self, st, amt):
        if "raise" not in st["legal_actions"]:
            return {"action": "call"} if st["to_call"] > 0 else {"action": "check"}
        hi = st["max_raise_to"]
        amt = int(amt)
        if amt >= 0.8 * hi:
            amt = hi
        return {"action": "raise", "amount": amt}

    # --------------------------------------------------------- preflop
    def _line_q(self, s, evs):
        """Width of seat s's preflop range from what it did this hand."""
        bk = self.book
        k = bk.seat[s].kind
        if k in NOISE:
            return 1.0
        q = 1.0
        half = self.S0 // 2
        for (t, stn, a, tc, pot, x, raises, amt, stf) in evs:
            if t != s or stn != 0:
                continue
            if a == RAISE:
                if raises == 0:
                    qq = bk.open_q(s)
                elif raises == 1:
                    qq = bk.tb_q(s)
                else:
                    qq = bk.tb_q(s) * 0.5
                if amt >= half:
                    qs = bk.shove_q(s)
                    qq = min(qq, qs) if raises >= 1 else qs
                if qq < q:
                    q = qq
            elif a == CALL and tc > 0:
                v = bk.call_q(s)
                if k == "always_call":
                    qq = 1.0
                elif raises == 0:
                    qq = v
                elif raises == 1 and tc < 0.15 * self.S0:
                    qq = min(v, max(0.40, 0.7 * v))
                elif tc < 0.3 * self.S0:
                    qq = min(v, max(0.16, 0.4 * v))
                else:
                    qq = min(v, max(0.08, 2 * bk.shove_q(s), 0.25 * v))
                if qq < q:
                    q = qq
        return max(0.012, q)

    def preflop(self, st):
        bk = self.book
        me = st["seat"]
        n = len(st["stacks"])
        bb = st["big_blind"]
        legal = st["legal_actions"]
        a0, b0 = CARD[st["hole_cards"][0]], CARD[st["hole_cards"][1]]
        cls = CLS[(a0, b0)]
        p = PCT[cls]
        tc = st["to_call"]
        pot = st["pot"]
        bets = st["bets"]
        folded = st["folded"]
        stacks = st["stacks"]
        evs = parse(st["history"], n, bb)
        raises = st.get("raises_this_street", 0)
        acted = set(e[0] for e in evs)
        behind = [i for i in range(n) if i != me and not folded[i] and i not in acted]
        live = [i for i in range(n) if i != me and not folded[i]]
        cur = max(bets)
        btn = st["button"]
        pos = (me - btn - 1) % n          # 0 = small blind ... n-1 = button
        rnd = self.rng.random
        S0 = self.S0
        premium = cls in ("AA", "KK", "QQ", "AKs", "AKo")
        suited = len(cls) == 3 and cls[2] == "s"

        if raises == 0:
            limpers = [e[0] for e in evs if e[2] == CALL]
            fishy = any(bk.vpip(i) > 0.5 for i in limpers)
            if tc == 0:        # big blind option
                if p < 0.10 or (fishy and p < 0.28):
                    return self._r(st, 4 * bb + bb * len(limpers))
                return {"action": "check"}
            nb = len(behind)
            kinds = [bk.seat[i].kind for i in behind]
            if nb and not limpers and all(k in ("always_fold", "starter") for k in kinds):
                # a starter bot without a pair/ace/king calls up to 2 bb more and then pays 2 bb on the flop and
                # turn before folding the river, so keep the open small enough for it to call
                return self._r(st, 2.2 * bb)
            thr = self.OPEN[min(nb, 9)]
            fb = 1.0
            bbs = (btn + 2) % n if n > 2 else (btn + 1) % n
            for i in behind:
                fb *= bk.fold_bb(i) if (i == bbs and self.X_BBF) else bk.fold_open(i)
            if nb:
                thr *= max(0.7, min(1.6, (fb / (0.8 ** nb)) ** 1.5))
            if limpers:
                thr *= 0.85
                if fishy:
                    thr = max(thr, 0.30)
            thr = min(thr, 0.65)
            size = (2.2 if nb <= 3 else 2.5) * bb + bb * len(limpers)
            if bets[me] > 0 and nb <= 1:
                size += bb // 2
            if fishy or any(bk.vpip(i) > 0.5 for i in behind):
                size += bb
            if p < thr:
                return self._r(st, size)
            if not limpers and 1 <= nb <= 3:
                if fb * pot - (1 - fb) * 0.6 * size > 8.0:      # any-two steal
                    return self._r(st, 2.2 * bb)
            if limpers and tc <= bb and p < 0.45 and (cls[0] == cls[1] or suited):
                return {"action": "call"}
            if bets[me] > 0 and tc <= bb // 2 and limpers and p < 0.6:
                return {"action": "call"}
            return {"action": "fold"}

        # facing a raise
        agg = None
        for e in evs:
            if e[2] == RAISE:
                agg = e[0]
        if agg is None or agg == me:
            return {"action": "check"} if tc == 0 else ({"action": "call"} if premium else {"action": "fold"})
        q = self._line_q(agg, evs)
        others = [i for i in live if i != agg and bets[i] >= 0.99 * cur]
        for i in others:
            q = min(q, max(self._line_q(i, evs), 0.6 * q))
        eq = eq_vs(cls, q) - 0.04 * len(others)
        odds = tc / float(pot + tc)
        ip = pos > (agg - btn - 1) % n
        rf = 0.72 + 0.20 * (1 - p) - (0.0 if ip else 0.05)
        ka = bk.seat[agg].kind
        if ka in NOISE:
            rf += 0.10
        mystack = stacks[me]
        allin_spot = tc >= 0.35 * (mystack + bets[me]) or stacks[agg] == 0 or cur >= 0.4 * S0

        if allin_spot:
            if (self.X_TJAM and bk.seat[agg].tag == "D" and bk.seat[(me + 3) % n].tag == "J" and bk.seat[1].tag == "F"
                    and cur >= 0.4 * S0
                    and cls not in ("AA", "KK", "QQ")):
                return {"action": "fold"}      # only once the 3.0 bb opener three seats on confirms this is that table
            if eq >= 0.60 and "raise" in legal and stacks[agg] > 0:
                return {"action": "raise", "amount": st["max_raise_to"]}
            if eq >= odds + 0.03 or premium:
                left = mystack - tc
                if (self.X_COMMIT and "raise" in legal and stacks[agg] > 0 and left > 0
                        and left < 0.8 * (pot + tc)):
                    eff = min(mystack, tc + stacks[agg])
                    req = eff / float(pot + eff + (eff - tc))
                    if eq >= req + 0.02 or cls in ("AA", "KK"):
                        return {"action": "raise", "amount": st["max_raise_to"]}
                    return {"action": "fold"}
            if eq >= odds + 0.03:
                return {"action": "call"}
            if premium:
                d = bk.seat[agg].sd["S"]
                if not (d[0] >= 2 and d[1] / d[0] < 0.02) or cls in ("AA", "KK"):
                    return {"action": "call"}
            return {"action": "fold"}

        if raises == 1:
            dead = pot - cur
            if p < max(0.03, 0.2 * q) or eq >= 0.62 or premium:
                mult = 3.0 if ip else 3.6
                if bk.rat(agg) < 0.5:
                    mult += 1.0
                return self._r(st, cur * mult + 0.5 * dead)
            if (self.X_LIGHT3 and bk.fold_3bet(agg) > 0.68 and not others and ip and p < 0.40
                    and (suited or p < 0.2) and rnd() < 0.4):
                return self._r(st, cur * 3.0)
            if (self.X_ATC3 and not others and len(behind) <= 5 and cur <= 4.5 * bb and ka is None
                    and bk.fold_3bet(agg) >= self.ATC_F and rnd() < self.ATC_P
                    and pos <= 1 and (bk.seat[agg].tag == "J" or not self.ATC_JONLY)):
                return self._r(st, cur * (3.0 if ip else 3.5) + 0.5 * dead)
            if self.X_BLIND3 and pos <= 1 and not others and tc <= 0.12 * S0:
                apos = (agg - btn - 1) % n
                if apos >= n - 2 or (apos == 0 and pos == 1):        # opener is CO / BTN / SB: wide
                    hr, lr = RANKS.index(cls[0]), RANKS.index(cls[1])
                    polar = suited and (hr == 12 or (hr - lr == 1 and lr >= 2) or (hr >= 10 and lr >= 9))
                    f3 = bk.fold_3bet(agg)
                    pr = 0.85 if f3 >= 0.55 else (0.55 if f3 >= 0.45 else 0.3)
                    if p < max(0.05, 0.3 * q) or (polar and q >= 0.2 and rnd() < pr):
                        return self._r(st, cur * (3.6 if pos == 1 else 3.9) + 0.5 * dead)
                if pos == 0 and eq * rf < odds + 0.06:
                    return {"action": "fold"}
            closing = not behind
            if tc <= 0.12 * S0 and eq * rf >= odds + 0.02 and (closing or eq >= self.CALL_EQ + 0.015 * len(behind)):
                return {"action": "call"}
            return {"action": "fold"}

        if eq >= 0.57 or cls in ("AA", "KK"):
            to = 2.3 * cur
            if to >= 0.35 * S0:
                return self._r(st, st["max_raise_to"] or to)
            return self._r(st, to)
        if (self.X_4BX and raises == 2 and not others and "raise" in legal and cur <= 16 * bb and len(behind) <= 3
                and bk.seat[agg].kind is None):
            f4 = bk.fold_4bet(agg)
            if f4 >= self.FBX_F and rnd() < self.FBX_P:
                opn = None
                for e in evs:
                    if e[1] == 0 and e[2] == RAISE:
                        opn = e[0]
                        break
                fo = 1.0
                nb = len(behind)
                if opn is not None and opn != me and opn != agg and not st["folded"][opn]:
                    fo = 1.0 - 0.4 * (1.0 - bk.fold_3bet(opn))      # the opener, now facing a 3-bet and a 4-bet
                    if opn in behind:
                        nb -= 1
                F = f4 * fo * (0.97 ** nb)
                to = min(2.3 * cur, 0.3 * S0)
                if F * pot - (1 - F) * (to - bets[me]) > 2 * bb:
                    self.b4key = (st["hole_cards"][0], st["hole_cards"][1])
                    return self._r(st, to)
        if premium or (tc <= 0.16 * S0 and eq * rf >= odds + 0.03):
            return {"action": "call"}
        return {"action": "fold"}

    # -------------------------------------------------------- postflop
    def _pool(self, s, evs, dead, board, street, K):
        bk = self.book
        o = bk.seat[s]
        k = o.kind
        rnd = self.rng.random
        if k == "starter" and self.X_STARTER:
            raised = any(e[0] == s and e[2] == RAISE for e in evs)
            src = PAIR_AK if raised else NOPAIR_NOAK
            step = max(1, len(src) // K)
            j = int(rnd() * step)
            out = [c for c in src[j::step] if c[0] not in dead and c[1] not in dead]
            return out or [src[0]]
        q = self._line_q(s, evs)
        M = max(8, int(q * 1326))
        cands = []
        step = max(1.0, M / float(K))
        x = rnd() * step
        while x < M:
            a, b = COMBOS[int(x)]
            if a not in dead and b not in dead:
                cands.append((a, b))
            x += step
        if len(cands) < 3:
            cands = [(a, b) for (a, b) in COMBOS[:60] if a not in dead and b not in dead][:20]
        if k in NOISE:
            return cands
        rat = bk.rat(s)
        keep = 1.0          # top share kept at full weight after betting
        cut = 0.0           # bottom share thinned after calling
        big_late = False
        bigbet = False
        acted = False
        for (t, stn, a, tc, pot, x, raises, amt, stf) in evs:
            if t != s or stn == 0:
                continue
            if a == RAISE:
                acted = True
                af = bk.raise_freq(s) * (2.0 if raises <= 1 else 1.0) if tc > 0 else bk.bet_freq(s)
                if x < 0.4:
                    af *= 1.25
                elif x > 2.0:
                    af *= 0.5
                elif x > 0.9:
                    af *= 0.7
                if stn >= 2 and x >= 0.75:
                    big_late = True
                if x >= 0.7:
                    bigbet = True
                af = max(0.04, min(1.0, af))
                keep = min(keep, af) * (0.85 if keep < 1.0 else 1.0)
            elif a == CALL and tc > 0:
                acted = True
                f = bk.pfold(s, tc / float(max(1, pot - tc)), 0, stn, False, tc, self.bb)
                cut = 1 - (1 - cut) * (1 - f)
        if not acted or k == "always_call":
            return cands
        vals = []
        if street < 3:
            bsu = [0, 0, 0, 0]
            bm = 0
            for c in board:
                bsu[c & 3] += 1
                bm |= RBIT[c]
            for a, b in cands:
                v = ev7(board + [a, b])
                if v < (2 << 20):
                    fd = (bsu[a & 3] + 1 + (a & 3 == b & 3) >= 4) or (bsu[b & 3] + 1 >= 4)
                    m = bm | RBIT[a] | RBIT[b]
                    m2 = (m << 1) | ((m >> 12) & 1)
                    sdr = False
                    for lo in range(0, 10):
                        if (m2 >> lo) & 15 == 15 and m != bm:
                            sdr = True
                            break
                    if fd and sdr:
                        v = max(v, 2 << 20)
                    elif fd:
                        v = max(v, (1 << 20) | (8 << 16))
                    elif sdr:
                        v = max(v, (1 << 20) | (5 << 16))
                vals.append((v, a, b))
        else:
            for a, b in cands:
                vals.append((ev7(board + [a, b]), a, b))
        vals.sort(reverse=True)
        m = len(vals)
        base = (0.0, 0.26, 0.20, 0.13)[street]
        base *= 0.5 + 1.7 * bk.bluffy(s, bigbet if self.X_SIZETELL else None)   # showdown bluff evidence
        if big_late and rat > 0.6 and self.X_GUARD:
            base *= 0.45                              # rational big turn/river bets are rarely bluffs
        wb = min(1.0, base / (1 - base) * keep / max(0.02, 1 - keep))
        wb = wb + (1 - rat) * (1 - wb) * 0.9
        wc = 0.4 + (1 - rat) * 0.6
        wc = min(1.0, wc * (0.6 + 1.2 * bk.sticky(s)))
        topn = keep * m
        cutn = (1 - cut) * m
        out = []
        for idx in range(m):
            w = 1.0
            if idx >= topn:
                w *= wb
            if idx >= cutn:
                w *= wc
            if w >= 1.0 or rnd() < w:
                out.append((vals[idx][1], vals[idx][2]))
        if len(out) < 3:
            out = [(a, b) for v, a, b in vals[:3]]
        return out

    def _equity(self, hero, board, pools, N, thr, minn=48):
        rnd = self.rng.random
        need = 5 - len(board)
        h0, h1 = hero
        if need == 0 and len(pools) == 1:
            hv = ev7(board + [h0, h1])
            w = 0.0
            pl = pools[0]
            for a, b in pl:
                ov = ev7(board + [a, b])
                if hv > ov:
                    w += 1.0
                elif hv == ov:
                    w += 0.5
            return w / len(pl)
        dead = set(board)
        dead.add(h0)
        dead.add(h1)
        deck = [c for c in range(52) if c not in dead]
        nd = len(deck)
        bk5 = 0
        bs8 = 0
        bm = [0, 0, 0, 0]
        for c in board:
            bk5 += P5[c]
            bs8 += S8[c]
            bm[c & 3] |= RBIT[c]
        hk = P5[h0] + P5[h1]
        hs = S8[h0] + S8[h1]
        get = NF.get
        win = 0.0
        sq = 0.0
        tot = 0
        for it in range(N):
            if thr and (it & 15) == 0 and tot >= minn:
                e = win / tot
                var = (sq / tot - e * e) / tot
                fl = 0.05 / tot
                if var < fl:
                    var = fl
                d = 3.2 * var ** 0.5
                for t in thr:
                    if -d <= e - t <= d:
                        break
                else:
                    break
            used = set()
            opp = []
            ok = True
            for pl in pools:
                a, b = pl[int(rnd() * len(pl))]
                if a in used or b in used:
                    for _ in range(5):
                        a, b = pl[int(rnd() * len(pl))]
                        if a not in used and b not in used:
                            break
                    else:
                        ok = False
                        break
                used.add(a)
                used.add(b)
                opp.append((a, b))
            if not ok:
                continue
            ek = bk5
            es = bs8
            fm = bm
            extra = ()
            if need:
                fm = bm[:]
                extra = []
                k = need
                while k:
                    c = deck[int(rnd() * nd)]
                    if c in used:
                        continue
                    used.add(c)
                    extra.append(c)
                    ek += P5[c]
                    es += S8[c]
                    fm[c & 3] |= RBIT[c]
                    k -= 1
            key = ek + hk
            hv = get(key)
            if hv is None:
                hv = NF[key] = _nf(board + list(extra) + [h0, h1])
            fs = FSUIT[es + hs]
            if fs >= 0:
                m = fm[fs]
                if h0 & 3 == fs:
                    m |= RBIT[h0]
                if h1 & 3 == fs:
                    m |= RBIT[h1]
                f = FLV[m]
                if f > hv:
                    hv = f
            res = 1.0
            ties = 1
            for a, b in opp:
                key = ek + P5[a] + P5[b]
                ov = get(key)
                if ov is None:
                    ov = NF[key] = _nf(board + list(extra) + [a, b])
                fs = FSUIT[es + S8[a] + S8[b]]
                if fs >= 0:
                    m = fm[fs]
                    if a & 3 == fs:
                        m |= RBIT[a]
                    if b & 3 == fs:
                        m |= RBIT[b]
                    f = FLV[m]
                    if f > ov:
                        ov = f
                if ov > hv:
                    res = 0.0
                    break
                if ov == hv:
                    ties += 1
            tot += 1
            if res:
                res = 1.0 / ties
                win += res
                sq += res * res
        if tot < 12:
            if len(pools) == 1:
                return win / tot if tot else 0.5
            return min(self._equity(hero, board, [pl], max(40, N // len(pools)), ()) for pl in pools) * 0.9
        return win / tot

    @staticmethod
    def _fdraw(hero, board, street):
        if street >= 3:
            return False
        cnt = [0, 0, 0, 0]
        for c in board:
            cnt[c & 3] += 1
        for c in hero:
            cnt[c & 3] += 1
        return cnt[hero[0] & 3] == 4 or cnt[hero[1] & 3] == 4

    def postflop(self, st):
        bk = self.book
        me = st["seat"]
        n = len(st["stacks"])
        bb = st["big_blind"]
        legal = st["legal_actions"]
        street = SI[st["street"]]
        hero = (CARD[st["hole_cards"][0]], CARD[st["hole_cards"][1]])
        board = [CARD[c] for c in st["board"]]
        tc = st["to_call"]
        pot = max(1, st["pot"])
        bets = st["bets"]
        folded = st["folded"]
        stacks = st["stacks"]
        mystack = stacks[me]
        evs = parse(st["history"], n, bb)
        bk.pfr_seat = None
        for e in evs:
            if e[1] == 0 and e[2] == RAISE:
                bk.pfr_seat = e[0]
        opps = [i for i in range(n) if i != me and not folded[i]]
        if not opps:
            return {"action": "check"} if tc == 0 else {"action": "call"}
        nopp = len(opps)
        rnd = self.rng.random
        kinds = [bk.seat[i].kind for i in opps]
        can_raise = "raise" in legal
        cur = max(bets)
        lo = st.get("min_raise_to") or 0
        hi = st.get("max_raise_to") or 0

        # --- starter bot heads-up: it calls any bet up to 2 bb and folds to more unless it holds a pair/A/K
        if self.X_STARTER and nopp == 1 and kinds[0] == "starter" and tc == 0 and can_raise:
            if not any(e[0] == opps[0] and e[2] == RAISE for e in evs):
                if street < 3 and lo <= 2 * bb <= hi:
                    return {"action": "raise", "amount": 2 * bb}
                return self._r(st, max(lo, 2 * bb + 6))

        # --- sample budget
        left = max(1, self.nhands - bk.hands)
        budget = (5.5 - self.spent) / left
        if self.spent + left * self.spent / max(50.0, bk.hands) < 4.0:
            budget = 0.01               # at our measured pace the whole table fits: keep full samples
        N = 280 if nopp == 1 else 200
        K = 100
        if budget < 0.004:
            N, K = 110, 50
        if budget < 0.002:
            N, K = 40, 24
        if self.scale < 1.0:
            N = max(30, int(N * self.scale))
            K = max(24, int(K * self.scale))
        dead = set(board)
        dead.update(hero)
        pools = [self._pool(s, evs, dead, board, street, K) for s in opps]
        active = [i for i in opps if stacks[i] > 0]
        margin = self.M_RIVER if street == 3 else self.M_CALL
        if tc > 0:
            for i in active:
                if bets[i] < cur:
                    margin += 0.03
            odds = tc / float(pot + tc)
            thr = (odds + margin, self.RAISE_E)
        else:
            thr = (0.5, self.RAISE_E)
        E = self._equity(hero, board, pools, N, thr, 48 if tc > 0 else 96)
        rat = sum(bk.rat(i) for i in opps) / nopp
        hv = ev7(board + list(hero))
        onepair = hv < (2 << 20)
        late = street >= 2
        guard = self.X_GUARD and late and onepair and rat > 0.6
        fguard = self.X_FGUARD and street == 1 and onepair and rat > 0.6

        # commitment state of each opponent, who checked this street, preflop raiser
        cst = {}
        checked = set()
        pfr_seat = None
        for e in evs:
            if e[1] == 0:
                if e[2] == RAISE:
                    pfr_seat = e[0]
                continue
            if e[2] == RAISE:
                cst[e[0]] = 2
            elif e[2] == CALL and e[3] > 0 and cst.get(e[0], 0) < 2:
                cst[e[0]] = 1
            elif e[2] == CHECK:
                checked.add(e[0])
        station = self.X_STATION and any(bk.station(i) for i in active)

        def called_eq(e, f1):
            e1 = max(0.0, (e - f1) / (1 - f1)) if f1 < 0.999 else 0.0
            return rat * e1 + (1 - rat) * e

        b4 = self.b4key is not None and self.b4key == (st["hole_cards"][0], st["hole_cards"][1])
        if tc == 0:
            if not can_raise or not active:
                return {"action": "check"}
            if b4 and E < 0.6:
                return {"action": "check"}      # the 4-bet bluff was called by a strong range: no more bluffs
            ev_check = E * pot
            Eh = E ** (1.0 / nopp) if (self.X_MW and nopp > 1 and E >= 0.5) else E
            if (self.X_TRAP and nopp == 1 and street < 3 and E >= 0.8 and bk.bet_freq(opps[0]) > 0.55
                    and (opps[0] - st["button"] - 1) % n > (me - st["button"] - 1) % n and rnd() < 0.6):
                return {"action": "check"}
            sizes = [0.33, 0.5, 0.75, 1.0]
            if (rat < 0.6 or mystack <= 2.5 * pot) and not guard and not fguard:
                sizes += [1.8, 100.0]
            bluff_ok = nopp <= 2 and not station and not any(k in ("always_call", "always_raise", "always_allin")
                                                             for k in kinds)
            image = 0.0
            if self.X_IMAGE and bk.hands > 120 and nopp == 1 and late:
                image = 0.04
            opts = []
            seen = set()
            for x in sizes:
                b = int(min(mystack, max(lo - bets[me], x * pot)))
                b = max(1, min(b, hi - bets[me]))
                if b in seen:
                    continue
                seen.add(b)
                xr = b / float(pot)
                if E < 0.5 and (xr > 1.05 or not bluff_ok):
                    continue
                F = 1.0
                fs = 0.0
                for i in active:
                    f = bk.pfold(i, xr, cst.get(i, 0), street, i in checked, b, bb)
                    F *= f
                    fs += f
                if len(active) < nopp:
                    F = 0.0
                ec = called_eq(Eh, fs / len(active))
                val = F * pot + (1 - F) * (ec * (pot + 2 * b) - b)
                if E < 0.5:
                    val -= (self.BLUFF_CUT - image) * pot + 0.04 * b
                opts.append((val, b))
            if opts:
                best = max(opts)
                if best[0] > ev_check + self.BET_EDGE * pot:
                    b = best[1]
                    if self.X_SIZEMIX:
                        near = [o for o in opts if o[0] >= best[0] - 0.03 * pot and o[0] > ev_check]
                        if len(near) > 1:
                            b = near[int(rnd() * len(near))][1]
                    if station and E >= 0.6 and b < 1.25 * pot:
                        b = min(int(b * 1.3), int(1.25 * pot), mystack)
                    return self._r(st, bets[me] + b)
            return {"action": "check"}

        # --- facing a bet
        if b4 and E < 0.75:
            margin += 0.15
        weakmade = onepair
        if not onepair and hv < (3 << 20):
            rc = [0] * 13
            for c in board:
                rc[c >> 2] += 1
            if max(rc) >= 2:                 # 'two pair' with one of the pairs on the board (0 wins in 7 live spots)
                h0, h1 = hero[0] >> 2, hero[1] >> 2
                weakmade = (1 if h0 == h1 else (rc[h0] > 0) + (rc[h1] > 0)) <= 1
        if (self.X_RGUARD and weakmade and bets[me] > 0 and tc > 0.18 * (pot + tc) and rat > 0.6
                and not self._fdraw(hero, board, street)):
            rs = None
            for e in evs:
                if e[2] == RAISE and e[1] == street:
                    rs = e[0]
            c = bk.seat[rs].rz if rs is not None and rs != me else (0, 0)
            c2 = bk.seat[rs].ourr if rs is not None and rs != me else (0, 0)
            # a seat that raises 40% of all bets, or 30% of OUR bets (it has spotted the folds), is not showing strength
            if not (c[1] >= 20 and c[0] >= 0.40 * c[1]) and not (c2[1] >= 12 and c2[0] >= 0.30 * c2[1]):
                return {"action": "fold"}
        if (self.X_P85 and street >= 2 and nopp == 1 and n == 8 and me == 4 and opps[0] == 6 and bk.seat[7].tag == "J"
                and bk.seat[1].tag == "F" and weakmade and bets[me] == 0 and tc >= 0.9 * (pot - tc)
                and not self._fdraw(hero, board, street)):
            return {"action": "fold"}      # bucket table seat 6: its pot-sized turn/river bets are real (weak 22% / 6% at showdown)
        best = "fold"
        best_ev = 0.0
        if (E - margin) * (pot + tc) - tc > 0:
            best = "call"
            best_ev = E * (pot + tc) - tc
        bettor = None
        for e in evs:
            if e[2] == RAISE and e[1] == street:
                bettor = e[0]
        braise = False
        if self.X_BRAISE and can_raise and nopp == 1 and bettor == opps[0] and E < self.RAISE_E and kinds[0] is None:
            c = bk.seat[bettor].ff[2]
            fn = c[0][1] + c[1][1] + c[2][1]
            if fn >= 4 and (c[0][0] + c[1][0] + c[2][0]) >= 0.55 * fn and tc <= 0.5 * pot:
                braise = True
        if can_raise and (E >= self.RAISE_E or braise) and active and not (guard and not braise):
            for to in ((cur + 0.75 * (pot + tc),) if braise else (cur + 0.75 * (pot + tc), hi)):
                to = int(max(lo, min(hi, to)))
                add = to - bets[me]
                xr = (to - cur) / float(pot + tc)
                if fguard and xr > 1.2 and to > lo:
                    continue
                F = 1.0
                fs = 0.0
                for i in active:
                    f = bk.pfold(i, xr, 2 if i == bettor else cst.get(i, 0), street, False, to - cur, bb)
                    F *= f
                    fs += f
                if len(active) < nopp:
                    F = 0.0
                ec = called_eq(E, fs / len(active))
                val = F * pot + (1 - F) * (ec * (pot + 2 * add - tc) - add)
                if braise:
                    val -= self.BLUFF_CUT * pot + 0.04 * add
                if val > best_ev + 0.04 * pot:
                    best_ev = val
                    best = to
        if best == "fold":
            return {"action": "fold"}
        if best == "call":
            return {"action": "call"}
        return self._r(st, best)
