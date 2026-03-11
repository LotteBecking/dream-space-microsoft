from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pyexcel as pe

FILE_PATH = Path('/Users/lottebecking/Downloads/20250926+gemiddelde_referentieniveaus_per_school_2223_2324_2425_Open_data.ods')
OUT_JSON = Path('/Users/lottebecking/Documents/GitHub/dream-space-microsoft/data-analysis/school_data_nl/ods_analysis_summary.json')
OUT_MD = Path('/Users/lottebecking/Documents/GitHub/dream-space-microsoft/data-analysis/school_data_nl/ods_analysis_summary.md')


def to_numeric_dutch(series: pd.Series) -> pd.Series:
    # Handles values like "1.234,56", "12,3", and percentages as plain numbers.
    cleaned = (
        series.astype(str)
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
        .str.replace('%', '', regex=False)
        .str.strip()
    )
    cleaned = cleaned.replace({'': np.nan, 'nan': np.nan, 'None': np.nan, '-': np.nan})
    return pd.to_numeric(cleaned, errors='coerce')


def weighted_mean(values: pd.Series, weights: pd.Series) -> float:
    mask = values.notna() & weights.notna() & (weights > 0)
    if not mask.any():
        return float('nan')
    return float(np.average(values[mask], weights=weights[mask]))


def load_data_sheet(path: Path) -> pd.DataFrame:
    book = pe.get_book(file_name=str(path))
    data_sheet = book['Data']
    rows = list(data_sheet.rows())
    if not rows:
        raise ValueError('Data sheet is empty')

    header = [str(x).strip() for x in rows[0]]
    records = rows[1:]
    df = pd.DataFrame(records, columns=header)
    df = df.replace('', np.nan)
    return df


def to_markdown(report: dict[str, object]) -> str:
    overall = report['overall']
    by_weight_cat = report['by_schoolwegingscategorie']
    top_improve_1f = report['top_improvers_1f']
    top_decline_1f = report['top_decliners_1f']
    top_improve_1s2f = report['top_improvers_1s2f']
    top_decline_1s2f = report['top_decliners_1s2f']

    lines: list[str] = []
    lines.append('# ODS Analysis Summary')
    lines.append('')
    lines.append(f"- File: `{report['file']}`")
    lines.append(f"- Rows (schools): `{overall['n_schools']}`")
    lines.append(f"- Columns: `{overall['n_columns']}`")
    lines.append('')
    lines.append('## National Weighted Means')
    lines.append('')
    lines.append(f"- 1F 2022-2023: `{overall['weighted_mean_1f_2223']:.2f}`")
    lines.append(f"- 1F 2023-2024: `{overall['weighted_mean_1f_2324']:.2f}`")
    lines.append(f"- 1F 2024-2025: `{overall['weighted_mean_1f_2425']:.2f}`")
    lines.append(f"- 1S/2F 2022-2023: `{overall['weighted_mean_1s2f_2223']:.2f}`")
    lines.append(f"- 1S/2F 2023-2024: `{overall['weighted_mean_1s2f_2324']:.2f}`")
    lines.append(f"- 1S/2F 2024-2025: `{overall['weighted_mean_1s2f_2425']:.2f}`")
    lines.append('')
    lines.append('## Outcome Distribution')
    lines.append('')
    lines.append(f"- Indicator 1F: `{overall['outcome_1f_counts']}`")
    lines.append(f"- Indicator 1S/2F: `{overall['outcome_1s2f_counts']}`")
    lines.append('')
    lines.append('## By Schoolwegingscategorie')
    lines.append('')
    for row in by_weight_cat:
        lines.append(
            f"- `{row['Schoolwegingscategorie']}`: n={row['n_schools']}, "
            f"gem. gewogen 1F={row['mean_gewogen_1f']:.2f}, "
            f"gem. gewogen 1S/2F={row['mean_gewogen_1s2f']:.2f}"
        )
    lines.append('')
    lines.append('## Top Movers (2022-2023 -> 2024-2025)')
    lines.append('')
    lines.append('- 1F improvers:')
    for row in top_improve_1f:
        lines.append(f"  {row['ovt']}: delta={row['delta_1f_2223_2425']:.2f}, totaal ll={int(row['Totaal aantal leerlingen 3 jaar'])}")
    lines.append('- 1F decliners:')
    for row in top_decline_1f:
        lines.append(f"  {row['ovt']}: delta={row['delta_1f_2223_2425']:.2f}, totaal ll={int(row['Totaal aantal leerlingen 3 jaar'])}")
    lines.append('- 1S/2F improvers:')
    for row in top_improve_1s2f:
        lines.append(f"  {row['ovt']}: delta={row['delta_1s2f_2223_2425']:.2f}, totaal ll={int(row['Totaal aantal leerlingen 3 jaar'])}")
    lines.append('- 1S/2F decliners:')
    for row in top_decline_1s2f:
        lines.append(f"  {row['ovt']}: delta={row['delta_1s2f_2223_2425']:.2f}, totaal ll={int(row['Totaal aantal leerlingen 3 jaar'])}")
    lines.append('')
    lines.append('## Missing Data (Top 10)')
    lines.append('')
    for key, value in report['missing_pct_top10'].items():
        lines.append(f"- {key}: {value:.2f}%")
    lines.append('')
    return '\n'.join(lines)


def main() -> None:
    if not FILE_PATH.exists():
        raise FileNotFoundError(f'File not found: {FILE_PATH}')

    df = load_data_sheet(FILE_PATH)

    numeric_columns = [
        'Gemiddelde %1F 2223',
        'Gemiddelde %1S/2F 2223',
        'Aantal leerlingen 2223',
        'Gemiddelde %1F 2324',
        'Gemiddelde %1S/2F 2324',
        'Aantal leerlingen 2324',
        'Gemiddelde %1F 2425',
        'Gemiddelde %1S/2F 2425',
        'Aantal leerlingen 2425',
        'Schoolweging',
        'Signaleringswaarde 1F',
        'Signaleringswaarde 1S/2F',
        'Gewogen driejaarsgemiddelde %1F',
        'Gewogen driejaarsgemiddelde %1S/2F',
        'Totaal aantal leerlingen 3 jaar',
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = to_numeric_dutch(df[col])

    df['delta_1f_2223_2425'] = df['Gemiddelde %1F 2425'] - df['Gemiddelde %1F 2223']
    df['delta_1s2f_2223_2425'] = df['Gemiddelde %1S/2F 2425'] - df['Gemiddelde %1S/2F 2223']

    stable = df[df['Totaal aantal leerlingen 3 jaar'] >= 30].copy()

    weighted_mean_1f_2223 = weighted_mean(df['Gemiddelde %1F 2223'], df['Aantal leerlingen 2223'])
    weighted_mean_1f_2324 = weighted_mean(df['Gemiddelde %1F 2324'], df['Aantal leerlingen 2324'])
    weighted_mean_1f_2425 = weighted_mean(df['Gemiddelde %1F 2425'], df['Aantal leerlingen 2425'])

    weighted_mean_1s2f_2223 = weighted_mean(df['Gemiddelde %1S/2F 2223'], df['Aantal leerlingen 2223'])
    weighted_mean_1s2f_2324 = weighted_mean(df['Gemiddelde %1S/2F 2324'], df['Aantal leerlingen 2324'])
    weighted_mean_1s2f_2425 = weighted_mean(df['Gemiddelde %1S/2F 2425'], df['Aantal leerlingen 2425'])

    by_schoolweging = (
        df.groupby('Schoolwegingscategorie', dropna=False)
        .agg(
            n_schools=('ovt', 'count'),
            mean_gewogen_1f=('Gewogen driejaarsgemiddelde %1F', 'mean'),
            mean_gewogen_1s2f=('Gewogen driejaarsgemiddelde %1S/2F', 'mean'),
        )
        .reset_index()
        .sort_values('mean_gewogen_1s2f', ascending=False)
    )

    top_improvers_1f = (
        stable[['ovt', 'delta_1f_2223_2425', 'Totaal aantal leerlingen 3 jaar']]
        .dropna()
        .sort_values('delta_1f_2223_2425', ascending=False)
        .head(10)
        .to_dict(orient='records')
    )
    top_decliners_1f = (
        stable[['ovt', 'delta_1f_2223_2425', 'Totaal aantal leerlingen 3 jaar']]
        .dropna()
        .sort_values('delta_1f_2223_2425', ascending=True)
        .head(10)
        .to_dict(orient='records')
    )
    top_improvers_1s2f = (
        stable[['ovt', 'delta_1s2f_2223_2425', 'Totaal aantal leerlingen 3 jaar']]
        .dropna()
        .sort_values('delta_1s2f_2223_2425', ascending=False)
        .head(10)
        .to_dict(orient='records')
    )
    top_decliners_1s2f = (
        stable[['ovt', 'delta_1s2f_2223_2425', 'Totaal aantal leerlingen 3 jaar']]
        .dropna()
        .sort_values('delta_1s2f_2223_2425', ascending=True)
        .head(10)
        .to_dict(orient='records')
    )

    missing_pct = (df.isna().mean() * 100).sort_values(ascending=False)

    report: dict[str, object] = {
        'file': str(FILE_PATH),
        'sheet': 'Data',
        'overall': {
            'n_schools': int(df.shape[0]),
            'n_columns': int(df.shape[1]),
            'weighted_mean_1f_2223': weighted_mean_1f_2223,
            'weighted_mean_1f_2324': weighted_mean_1f_2324,
            'weighted_mean_1f_2425': weighted_mean_1f_2425,
            'weighted_mean_1s2f_2223': weighted_mean_1s2f_2223,
            'weighted_mean_1s2f_2324': weighted_mean_1s2f_2324,
            'weighted_mean_1s2f_2425': weighted_mean_1s2f_2425,
            'outcome_1f_counts': df['Uitkomst indicator 1F'].value_counts(dropna=False).to_dict(),
            'outcome_1s2f_counts': df['Uitkomst indicator 1S/2F'].value_counts(dropna=False).to_dict(),
        },
        'by_schoolwegingscategorie': by_schoolweging.to_dict(orient='records'),
        'top_improvers_1f': top_improvers_1f,
        'top_decliners_1f': top_decliners_1f,
        'top_improvers_1s2f': top_improvers_1s2f,
        'top_decliners_1s2f': top_decliners_1s2f,
        'missing_pct_top10': {
            str(k): float(v) for k, v in missing_pct.head(10).to_dict().items()
        },
    }

    OUT_JSON.write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding='utf-8')
    OUT_MD.write_text(to_markdown(report), encoding='utf-8')

    print(f'Analysis written to: {OUT_JSON}')
    print(f'Markdown summary written to: {OUT_MD}')


if __name__ == '__main__':
    main()
