from pathlib import Path
import pandas as pd
import random
from datetime import date, timedelta

# -------- CONFIG --------
OUTPUT_PATH = Path("test_primos.csv")
NUM_ROWS = 60                 # number of days / entries
START_DATE = date(2024, 9, 1) # arbitrary start
PRIMO_RANGE = (60, 1600)      # realistic daily range
# ------------------------

def generate_random_data(
    num_rows: int,
    start_date: date,
    primo_range: tuple[int, int],
) -> pd.DataFrame:
    rows = []
    current_total = 0
    current_date = start_date

    for _ in range(num_rows):
        primos = random.randint(*primo_range)
        current_total += primos

        rows.append({
            "date": current_date.isoformat(),
            "primogems": primos,
            "total": current_total,
        })

        # advance date by 1–2 days (feels more real)
        current_date += timedelta(days=random.choice([1, 1, 1, 2]))

    return pd.DataFrame(rows)

def main():
    df = generate_random_data(NUM_ROWS, START_DATE, PRIMO_RANGE)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Generated {len(df)} rows → {OUTPUT_PATH.resolve()}")

if __name__ == "__main__":
    main()
