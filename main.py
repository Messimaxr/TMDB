# Importing libraries and packages
import pandas as pd
import numpy as np
import os
import json
from matplotlib import pyplot as plt

# Change directory to yours before running
os.chdir('D:\python_folder\TMDB')

#Data Wrangling
# Importing data for both credits and info files
dfc = pd.read_csv('tmdb_5000_credits.csv')
dfi = pd.read_csv('tmdb_5000_movies.csv')

# Sorting data files with movie id
dfi = dfi.sort_values(by=['id'])
dfc = dfc.sort_values(by=['movie_id'])

# Merging both data frames with corresponding movie id
dfi['cast'] = dfc['cast']
dfi['crew'] = dfc['crew']
df = dfi
df = df.sort_index()

# Changing column data type to facilitate data analysis
"""
data in cast column were str, so it should be changed to dictionaries before analysis
Analysis conducted in cast_dicts column in order to get the main two actors of each movie if data is available 
"""
results = []
for i in range(4803):
    a = df['cast'][i]
    result = json.loads(a)
    results.append(result)
df.drop('cast', inplace=True, axis=1)
df['cast_dicts'] = results

''' Two new columns for main two actors'''
actor1 = []
actor2 = []
for j in range(4803):
    cast_len = df['cast_dicts'][j]
    if len(cast_len) >= 2:
        actor1.append(df['cast_dicts'][j][0]['name'])
        actor2.append(df['cast_dicts'][j][1]['name'])
    else:
        actor1.append('No data')
        actor2.append('No data')

# Adding two columns
df['Actor_1'] = actor1
df['Actor_2'] = actor2

# Extract director and producer names from crew column for each movie if data is available
directors = []
producers = []
for j in range(4803):
    crew_i = df['crew'][j]
    if len(crew_i) >= 2:
        a = crew_i.find('"Director"') + 20
        b = crew_i.find('"', crew_i.find('"Director"') + 21)
        directors.append(crew_i[a + 1:b])
        aa = crew_i.find('"Producer"') + 20
        bb = crew_i.find('"', crew_i.find('"Producer"') + 21)
        producers.append(crew_i[aa + 1:bb])

    else:
        directors.append('No data')
        producers.append('No data')

# Adding two columns
df['director'] = directors
df['producer'] = producers

# Extracting genres counts in dictionary
genres_dict = {'Action': 0, 'Adventure': 0, 'Animation': 0, 'Fantasy': 0, 'Crime': 0, 'Drama': 0, 'Science Fiction': 0,
               'Family': 0, 'Thriller': 0, 'Comedy': 0, 'Horror': 0, 'Romance': 0, 'Western': 0, 'Mystery': 0,
               'History': 0, 'War': 0, 'Documentary': 0}
''' Iterating through genre column with every key in genres_dict'''
for j in range(4803):
    genre_i = df['genres'][j]
    for key in genres_dict:
        if genre_i.find(key) != -1:
            genres_dict[key] += 1

"""
data in release date column should be changed to year only to group by years
There is one null date value that will be remain intact for future analysis with data
"""
df['date'] = pd.to_datetime(df['release_date']).dt.year
''' Adding new column for profit of each movie'''
df['profit'] = df['revenue'] - df['budget']
# EDA

# 1-Max data of each item all over the years
print('This analysis is conducted on TMDB files and limited to these data with most recent release date 03/02/2017')
print('-' * 110)

genre_max = max(genres_dict, key=genres_dict.get)
print('The most used genre over the years is: {}'.format(genre_max))

'''Movies with vote counts less than 100 will be misleading as they may be voted for one time with rating equals 10 '''
vote_count_filter = (df['vote_count'] > 100)
dff = df[vote_count_filter]
high_rate = (dff['vote_average'].max())
high_rate_name = (dff['title'][(dff['vote_average'].idxmax(axis=0))])
high_rate_director = (dff['director'][(dff['vote_average'].idxmax(axis=0))])
print(
    'The highest rated movie ever is {} with rating: {} for director: {}'.format(high_rate_name, high_rate,
                                                                                 high_rate_director))

high_revenue = (df['revenue'].max())
high_revenue_name = (df['title'][(df['revenue'].idxmax(axis=0))])
print('The highest revenue ever is {:,} for the movie: {}'.format(high_revenue, high_revenue_name))

high_budget = (df['budget'].max())
high_budget_name = (df['title'][(df['budget'].idxmax(axis=0))])
print('The highest budget ever is {:,} for the movie: {}'.format(high_budget, high_budget_name))

high_profit = ((df['revenue'] - df['budget']).max())
high_profit_name = (df['title'][((df['revenue'] - df['budget']).idxmax(axis=0))])
high_profit_producer = (df['producer'][((df['revenue'] - df['budget']).idxmax(axis=0))])
print('The highest profit ever is {:,} for the movie: {} for producer: {}'.format(high_profit, high_profit_name,
                                                                                  high_profit_producer))

high_popularity = (df['popularity'].max())
high_popularity_name = (df['title'][(df['popularity'].idxmax(axis=0))])
print('The highest popularity ever is {:,} for the movie: {}'.format(high_popularity, high_popularity_name))

Longest_movie = (df['runtime'].max())
Longest_movie_name = (df['title'][(df['runtime'].idxmax(axis=0))])
print('The longest movie ever is {:,} for the movie: {}'.format(Longest_movie, Longest_movie_name))

run_time_filter = (df['runtime'] > 5)
dff = df[run_time_filter]
shortest_movie = (dff['runtime'].min())
shortest_movie_name = (dff['title'][(dff['runtime'].idxmin(axis=0))])
print('The shortest movie ever is {:,} for the movie: {}'.format(shortest_movie, shortest_movie_name))

most_lang = (df['original_language'].mode()[0])
print('The most original language ever is {}'.format(most_lang))


# Filtering movies with budget less than 1000 dollars and plotting years vs total budget spent on movies
dff=df[df['budget']>1000]
fig, ax = plt.subplots(figsize=(15,7))
dff.groupby(['date'])['budget'].sum().plot(ax=ax)
plt.ylabel("budget")
plt.xticks(np.arange(1916, 2017, 4))
plt.grid()
plt.show()

# Filtering movies with revenue less than 1000 dollars and plotting years vs total revenue came from movies
dff=df[df['revenue']>1000]
fig, ax = plt.subplots(figsize=(15,7))
dff.groupby(['date'])['revenue'].sum().plot(ax=ax)
plt.ylabel("revenue")
plt.xticks(np.arange(1916, 2017, 4))
plt.grid()
plt.show()

# Correlation between revenue and budget
dff=df[df['revenue']>1000]
dff=dff[dff['budget']>1000]
dff.plot(kind='scatter', x='revenue', y='budget')
plt.grid()
plt.show()

#Histogram of revenue of movies
dff=df[df['revenue']>1000]
dff.plot(kind='hist', x='revenue', y='budget')
plt.grid()
plt.show()

# Creating graph of genres count over all years
names = list(genres_dict.keys())
values = list(genres_dict.values())
plt.bar(range(len(names)), values, tick_label=names)
plt.show()

# Graph of original language count of movies over the years
fig, ax = plt.subplots(figsize=(15, 7))
dff['original_language'].value_counts().plot.bar(ax=ax)
plt.ylabel("original_language")
ax.set_ylim([0, 75])
plt.yticks(np.arange(0, 75, 2))
plt.grid()
plt.show()

# Filtering movies with vote count less than 100 and plot max rated movie every year
dff = df[df['vote_count'] > 100]
fig, ax = plt.subplots(figsize=(15, 7))
dff.groupby(['date'])['vote_average'].max().plot.bar(ax=ax)
plt.ylabel("vote_average")
ax.set_ylim([6, 9])
# plt.xticks(np.arange(1916, 2017, 4))
plt.grid()
plt.show()

# Graph of highest popularity every year
fig, ax = plt.subplots(figsize=(15, 7))
dff.groupby(['date'])['popularity'].max().plot.bar(ax=ax)
plt.ylabel("popularity")
# plt.xticks(np.arange(1916, 2017, 4))
plt.grid()
plt.show()

# Top_10 analysis
# popularity
dff = df
dff = dff.sort_values(by=['popularity'])
dff = (dff.tail(10))
dff.plot(kind='bar', x='title', y='popularity')
plt.grid()
plt.show()
print('-' * 40)

# Runtime
dff = df
dff = dff.sort_values(by=['runtime'])
dff = dff[dff['runtime'].notna()]
dff = (dff.tail(10))
dff.plot(kind='bar', x='title', y='runtime')
plt.grid()
plt.show()

dff = df
dff = df[df['vote_count'] > 100]
dff = dff.sort_values(by=['vote_average'])
dff = dff[dff['vote_average'].notna()]
dff = (dff.tail(10))
dff.plot(kind='bar', x='title', y='vote_average', ylim=(7.5, 9))
plt.grid()
plt.show()

dff = df
dff = df[df['vote_count'] > 100]
dff = dff.sort_values(by=['vote_average'])
dff = dff[dff['vote_average'].notna()]
dff = (dff.tail(10))
dff.plot(kind='bar', x='director', y='vote_average', ylim=(7.5, 9))
plt.grid()
plt.show()

dff = df
dff = dff.sort_values(by=['profit'])
dff = (dff.tail(10))
dff = dff[dff['profit'].notna()]
dff.plot(kind='bar', x='title', y='profit')
plt.grid()
plt.show()


dff = df
dff = dff.sort_values(by=['profit'])
dff = (dff.tail(10))
dff = dff[dff['profit'].notna()]
dff.plot(kind='bar', x='producer', y='profit')
plt.grid()
plt.show()

#Counting the number of occurence of each actor as either in the first or second order of cast
unique_dire = set()
all_keys = list()
for i in range(4803):
    unique_dire.add(df['Actor_1'][i])
    all_keys.append(df['Actor_1'][i])
    unique_dire.add(df['Actor_2'][i])
    all_keys.append(df['Actor_2'][i])

count_list=list()
unique_dire=list(unique_dire)
for item in unique_dire:
    count_unique=all_keys.count(item)
    count_list.append(count_unique)

oscar_nom=dict()
for unique in range(len(unique_dire)):
    oscar_nom[unique_dire[unique]]=count_list[unique]

vals = sorted(oscar_nom.items(), key=lambda x: x[1])
del vals[0:-11]
vals=dict(vals)
del vals["No data"]

# Plot top 10 actors in order of appearance in movies regardless of movie rating
names = list(vals.keys())
values = list(vals.values())
plt.bar(range(len(names)), values, tick_label=names)
plt.ylabel("No of movies")
plt.xlabel("Actor")
plt.grid()
plt.show()