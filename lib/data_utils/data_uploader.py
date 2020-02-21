import pickle

from lib.cloud_utils import storage


with open("../../AAPL_5.pickle", "rb") as file:
    data = pickle.load(file)

dates = list(data.index)
days = sorted(set([timestamp[:8] for timestamp in dates]))

for i in range(len(days) - 1):
    print(f"{i}/{len(days) - 1}")
    storage.load_to_gcs(
        f"AAPL_5_{days[i]}.csv", (data.loc[days[i]: days[i + 1]]).to_csv()
    )

storage.load_to_gcs(f"AAPL_5_{days[-1]}.csv", (data.loc[days[-1] :]).to_csv())
