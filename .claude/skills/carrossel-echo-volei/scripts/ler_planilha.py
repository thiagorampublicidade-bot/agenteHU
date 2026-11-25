#!/usr/bin/env python3
"""Despeja todas as abas de uma planilha de briefing, com células mescladas resolvidas.

Uso: python3 ler_planilha.py <arquivo.xlsx> [--aba NOME]

Para cada aba imprime as linhas não vazias como "L<n> | col: valor | ...",
usando a primeira linha não vazia como cabeçalho quando ela parecer um.
Valores de células mescladas são repetidos em todas as células da mescla,
para que informações que valem para várias linhas (ex.: tema do carrossel)
apareçam em cada página.
"""
import signal
import sys
from datetime import date, datetime

import openpyxl


def fmt(v):
    if v is None:
        return ""
    if isinstance(v, (datetime, date)):
        return v.strftime("%d/%m/%Y")
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v).strip()


def dump(ws):
    grid = {}
    for row in ws.iter_rows():
        for c in row:
            if c.value is not None:
                grid[(c.row, c.column)] = c.value
    for rng in ws.merged_cells.ranges:
        v = grid.get((rng.min_row, rng.min_col))
        for r in range(rng.min_row, rng.max_row + 1):
            for col in range(rng.min_col, rng.max_col + 1):
                grid[(r, col)] = v
    if not grid:
        print("  (vazia)")
        return
    rows = sorted({r for r, _ in grid})
    cols = sorted({c for _, c in grid})
    first = rows[0]
    header_vals = [fmt(grid.get((first, c))) for c in cols]
    is_header = sum(1 for h in header_vals if h) >= max(2, len(cols) // 2) and all(
        len(h) < 60 for h in header_vals
    )
    names = {
        c: (header_vals[i] if is_header and header_vals[i] else openpyxl.utils.get_column_letter(c))
        for i, c in enumerate(cols)
    }
    if is_header:
        print("  Cabeçalho: " + " | ".join(h or "—" for h in header_vals))
    for r in rows:
        if is_header and r == first:
            continue
        parts = [f"{names[c]}: {fmt(grid.get((r, c)))}" for c in cols if fmt(grid.get((r, c)))]
        if parts:
            print(f"  L{r} | " + " | ".join(parts))


def main():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    only = sys.argv[sys.argv.index("--aba") + 1] if "--aba" in sys.argv else None
    wb = openpyxl.load_workbook(path, data_only=True)
    for ws in wb.worksheets:
        if only and ws.title != only:
            continue
        print(f"\n=== Aba: {ws.title} ({ws.sheet_state}) ===")
        dump(ws)


if __name__ == "__main__":
    main()
