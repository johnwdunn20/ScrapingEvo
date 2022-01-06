import pandas as pd 
import numpy as np

# ToDo: rename all my variables

results = pd.read_excel('/Users/JohnDunn/Documents/Python_Docs/Web Scraper/Test1.xlsx')


# not sure I need this
z = results.groupby(['Hyperlink', 'Ski', 'Section Title'])['Description'].apply('; '.join).reset_index()


# will need to join on HyperLink to get ski in here
x = results[['Hyperlink', 'Section Title', 'Description']].pivot_table(index = 'Hyperlink', columns= 'Section Title', values = 'Description', aggfunc = lambda x: ' ;'.join(x))

f = results[['Hyperlink', 'Ski']].drop_duplicates()
j = f.join(x, on = 'Hyperlink', how = 'inner')

print(f.head())
print(x.head())

print(j.head())

# not sure we need to set the index
j.set_index('Ski')

j.to_excel('/Users/JohnDunn/Documents/Python_Docs/Web Scraper/Results.xlsx')


import math
countSkis = 121
print(math.ceil(countSkis / 40) + 1)