import pandas as pd
df = pd.read_json("out.json")
# print(df.columns)
print(df['catlevel2Name'].unique())


