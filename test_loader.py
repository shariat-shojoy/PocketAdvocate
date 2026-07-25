from utils.loader import LawLoader

loader = LawLoader("data/bdlaws_formatted.csv")

df = loader.load()

print(df.head())
print(df.columns)
print(len(df))