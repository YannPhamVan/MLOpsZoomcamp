import pandas as pd

df = pd.read_parquet("data/yellow_tripdata_2023-03.parquet")

df['duration'] = df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']
df['duration'] = df['duration'].dt.total_seconds() / 60

# df = df[(df.duration >= 1) & (df.duration <= 60)]

print(f"Rows after filtering: {len(df)}")
