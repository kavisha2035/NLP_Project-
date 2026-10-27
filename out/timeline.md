# Consensus timeline (align=tfidf, nli=heuristic)

## E0: On August 2, 1964, three North...  -> CONFLICT [claim]
- [A] 1964-08-02              On August 2, 1964, three North Vietnamese torpedo boats attacked the destroyer USS Maddox while it patrolled in international waters.
- [B] 1964-08-02              On August 2, 1964, the American destroyer Maddox entered North Vietnamese waters and was engaged by two patrol boats.
- [C] 1964-08-02              On August 2, 1964, the Maddox exchanged fire with three torpedo boats after they approached the ship.

## E2: On August 4, 1964, North Vietnamese...  -> CONFLICT [claim]
- [A] 1964-08-04              On August 4, 1964, North Vietnamese boats attacked the Maddox and the destroyer USS Turner Joy a second time.
- [B] 1964-08-04              Hanoi insisted that no second attack took place on August 4, 1964.
- [C] 1964-08-04              On August 4, 1964, crews reported a second attack, but later analysis found no evidence that it occurred.

## E3: On August 5, 1964, American aircraft...  -> CONFLICT [temporal]
- [A] 1964-08-05              On August 5, 1964, American aircraft bombed North Vietnamese naval bases in retaliation.
- [B] 1964-08-05              On August 5, 1964, American planes bombed naval bases and an oil depot in the north.
- [C] 1964-08-06              Two days later, American aircraft struck North Vietnamese naval bases.

## E5: Congress passed the Gulf of Tonkin...  -> ok
- [A] 1964-08-07              Congress passed the Gulf of Tonkin Resolution on August 7, 1964.
- [B] 1964-08-07              On August 7, 1964, the American Congress adopted the Gulf of Tonkin Resolution.
- [C] 1964-08-07              On August 7, 1964, Congress passed the Gulf of Tonkin Resolution with two dissenting votes.

## E1: The Maddox returned fire, and aircraft...  -> ok
- [A] ?                       The Maddox returned fire, and aircraft from the carrier USS Ticonderoga joined the fight.
- [B] ?                       Aircraft from the carrier Ticonderoga then attacked the patrol boats.
- [C] ?                       Aircraft from the Ticonderoga also attacked the boats.

## E4: American officials said two North Vietnamese...  -> CONFLICT [claim]
- [A] ?                       American officials said two North Vietnamese torpedo boats were sunk in the raids.
- [B] ?                       Hanoi said eight of its boats were damaged or sunk in the raids.

## E6: Johnson said the United States sought...  -> ok
- [A] ?                       Johnson said the United States sought no wider war.

## E13: Hanoi protested the raids as an...  -> ok
- [B] ?                       Hanoi protested the raids as an act of war.

## E19: Historians later argued that the resolution...  -> ok
- [C] ?                       Historians later argued that the resolution gave Johnson broad power to expand the war.

# Conflict pairs
- A0 vs B0 (claim(NLI))
    On August 2, 1964, three North Vietnamese torpedo boats attacked the destroyer USS Maddox while it patrolled in international waters.
    On August 2, 1964, the American destroyer Maddox entered North Vietnamese waters and was engaged by two patrol boats.
- A2 vs B2 (claim(NLI))
    On August 4, 1964, North Vietnamese boats attacked the Maddox and the destroyer USS Turner Joy a second time.
    Hanoi insisted that no second attack took place on August 4, 1964.
- A2 vs C2 (claim(NLI))
    On August 4, 1964, North Vietnamese boats attacked the Maddox and the destroyer USS Turner Joy a second time.
    On August 4, 1964, crews reported a second attack, but later analysis found no evidence that it occurred.
- A3 vs C3 (temporal)
    On August 5, 1964, American aircraft bombed North Vietnamese naval bases in retaliation.
    Two days later, American aircraft struck North Vietnamese naval bases.
- A4 vs B4 (claim(NLI))
    American officials said two North Vietnamese torpedo boats were sunk in the raids.
    Hanoi said eight of its boats were damaged or sunk in the raids.
- B0 vs C0 (claim(NLI))
    On August 2, 1964, the American destroyer Maddox entered North Vietnamese waters and was engaged by two patrol boats.
    On August 2, 1964, the Maddox exchanged fire with three torpedo boats after they approached the ship.
- B3 vs C3 (temporal)
    On August 5, 1964, American planes bombed naval bases and an oil depot in the north.
    Two days later, American aircraft struck North Vietnamese naval bases.

# Negative cycles in the merged STN (why the sources are inconsistent)
- cycle 1 (total weight -1, sources ['A', 'C']):
    [A] E3: On August 5, 1964, American aircraft... <= 1964-08-05
    [C] t(E2: On August 4, 1964, North Vietnamese...) - t(E3: On August 5, 1964, American aircraft...) <= -2d
    [A] E2: On August 4, 1964, North Vietnamese... >= 1964-08-04
- cycle 2 (total weight -1, sources ['A', 'B', 'C']):
    [B] E3: On August 5, 1964, American aircraft... <= 1964-08-05
    [C] t(E2: On August 4, 1964, North Vietnamese...) - t(E3: On August 5, 1964, American aircraft...) <= -2d
    [A] E2: On August 4, 1964, North Vietnamese... >= 1964-08-04