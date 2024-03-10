import pandas as pd

df = pd.read_csv('gapminder.tsv',sep='\t')
print(df)
print(df.groupby('year')['lifeExp'].mean())
grouped_year_df = df.groupby('year')
grouped_year_df_lifeExp= grouped_year_df['lifeExp']
print(type(grouped_year_df_lifeExp))
print(df.groupby('year')['gdpPercap'].mean())
multi_group_var = df.groupby(['year','continent'])[['lifeExp', 'gdpPercap']].mean()