# %%
import json

import pandas as pd

file_name = "job-board.txt"

rows = []

with open(file_name, "r") as f:
    for l in f.readlines():
        if not l.startswith("---SEP---"):
            rows.append(json.loads(l))

print(len(rows))
df = pd.DataFrame(rows)

# %%
df.median_tenure.dropna().hist(bins=100)

# %%
df[df.median_tenure > 7]


# %%

import matplotlib as mpl
import matplotlib.pyplot as plt

plt.scatter(df.total_applicant, df.median_tenure)

# %%
