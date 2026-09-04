#!/usr/bin/env python3
import json

for year in [2021, 2022, 2023, 2024, 2025]:
    with open(f"data/{year}.json", "r", encoding="utf-8") as f:
        qs = json.load(f)
    areas = {}
    for q in qs:
        key = q["area"] + "/" + q["disciplina"]
        areas[key] = areas.get(key, 0) + 1
    print(f"=== {year}: {len(qs)} questions ===")
    for k in sorted(areas.keys()):
        print(f"  {k}: {areas[k]}")
    diffs = {}
    for q in qs:
        d = str(q["dificuldade"])
        diffs[d] = diffs.get(d, 0) + 1
    print(f"  Difficulties: {diffs}")
    # verify ID format
    print(f"  First ID: {qs[0]['id']}, Last ID: {qs[-1]['id']}")
    # verify all have 5 options
    bad = [q for q in qs if len(q["opcoes"]) != 5]
    print(f"  Questions with != 5 options: {len(bad)}")
    # verify gabarito
    bad_g = [q for q in qs if q["gabarito"] not in "ABCDE"]
    print(f"  Invalid gabarito: {len(bad_g)}")
    # verify texto length
    short = [q for q in qs if len(q["texto"]) < 50]
    print(f"  Questions with short texto (<50 chars): {len(short)}")
    print()
