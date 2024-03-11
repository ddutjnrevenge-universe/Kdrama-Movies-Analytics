#!/usr/bin/env python
# coding: utf-8

# # Import required libraries

# In[4]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import os


# # Importing Dataset

# In[5]:


os.getcwd()


# In[83]:


df = pd.read_csv('korean_drama.csv')


# In[84]:


df.head()


# In[85]:


df_actors = pd.read_csv('wiki_actors.csv')
df_actors.head()


# ## Data Preprocessing

# In[86]:


df.columns


# In[87]:


df.columns = ['ID','Film','Year','Director','Screenwriter','Country','Type','Episodes','Duration','Start','End','AirDate','Network','ContentRating','Synopsis','Ranking','PopularityRanking']


# In[88]:


df.columns


# In[89]:


df.head()


# In[90]:


df_actors.columns = ['Actor_ID','Actor_name', 'Film', 'Character', 'Role']
df_actors.head()


# In[91]:


# Checking each column for missing values
df.isna().sum()


# In[92]:


# Replacing missing values
df.fillna(0)


# In[93]:


df.info()


# In[94]:


df.describe()


# In[95]:


df.AirDate = df.AirDate.astype('category')
df.Year = df.Year.astype('category')
df.ContentRating = df.ContentRating.astype('category')
df.Film = df.Film.astype('category')


# In[96]:


df.info()


# In[97]:


df.ContentRating.cat.categories


# In[98]:


df.describe()


# In[99]:


df.shape


# In[100]:


# Check if there are duplicated rows
df.duplicated().sum()


# In[101]:


# Check the numner of unique values
df.select_dtypes(include='object').nunique()


# In[102]:


# Drop ID, Country and Type columns because they are unnecessary
df.drop(['ID','Country','Type'], axis=1, inplace=True)


# In[103]:


#Turn measure of duration from seconds to minutes
df.Duration = df.Duration/60


# In[104]:


df.head()


# In[105]:


#remove unneccesary column
df_actors.drop('Actor_ID', axis=1, inplace=True)


# In[106]:


df_actors = df_actors[df_actors['Role']=='Main Role']
df_actors.head()


# In[107]:


# First, group df_actors by 'Film' and aggregate the main role actors into a list
df_actors_grouped = df_actors[df_actors['Role'] == 'Main Role'].groupby('Film')['Actor_name'].apply(list).reset_index()

# Merge the aggregated actors list with the film data
df_merged = pd.merge(df, df_actors_grouped, how='left', on='Film')

# Now, df_merged will contain one row per film with a list of main role actors in the 'Actor' column.
df_merged


# In[108]:


# grouped_df = df_merged.groupby('Film').agg({'Ranking': 'mean', 'Actor_name': list}).reset_index()
# grouped_df = grouped_df.rename(columns={'Actor Name': 'Main Role Actors'})
# grouped_df


# # Data Analysis

# ## Evolution Over the Years (2015-2023)

# ### Number of KDramas in a year

# In[109]:


amount= df["Year"].value_counts()
sns.set_style('whitegrid')
sns.lineplot(data=amount, color='green', linewidth=2.5)
plt.xlabel("Years", fontweight = 'bold')
plt.ylabel("Films", fontweight = 'bold')
plt.title("Number of Kdramas (2015-2023)", fontweight = 'bold', fontsize=15)
plt.savefig('D:\Syllabus\PROGRAMMING/numberofdrama.png', dpi=500,bbox_inches='tight')
plt.show()


# ### Average duration of an episode and average number of episodes in a film

# In[110]:


df.sort_values("Duration", ascending=False)

# Group the data by the release year
yearly_avg_duration = df.groupby("Year")["Duration"].mean().reset_index()
yearly_avg_episodes = df.groupby("Year")["Episodes"].mean().reset_index()

# Set the style
sns.set_style('whitegrid')

# Create a figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot average duration of 1 episode over the years
sns.lineplot(data=yearly_avg_duration, x="Year", y="Duration", ax=axes[0], color='green', linewidth=2.5)
axes[0].set_title("Average Duration of 1 Episode Over the Years", fontweight = 'bold', fontsize=15)

# Plot average number of episodes in a film over the years
sns.lineplot(data=yearly_avg_episodes, x="Year", y="Episodes", ax=axes[1], color='green', linewidth=2.5)
axes[1].set_title("Average Number of Episodes in a Film Over the Years", fontweight = 'bold', fontsize=15)

# Customize the plot further if needed
axes[0].set_ylabel("Average Duration (minutes)", fontweight = 'bold')
axes[1].set_ylabel("Average Number of Episodes", fontweight = 'bold')
plt.tight_layout()
plt.savefig('D:\Syllabus\PROGRAMMING/avg-duration-episode.png', dpi=500,bbox_inches='tight')
plt.show()


# ### Number of films by Content Rating

# In[322]:


import matplotlib.patches as mpatches

# Count the number of films in each Content Rating category
rating_counts = df['ContentRating'].value_counts()

# Create a color mapping for each Content Rating category
color_mapping = {
    '13+ - Teens 13 or older': 'tab:blue',
    '15+ - Teens 15 or older': 'tab:orange',
    '18+ Restricted (violence & profanity)': 'tab:green',
    'G - All Ages': 'tab:red',
    'Not Yet Rated': 'tab:purple',
    'R - Restricted Screening (nudity & violence)': 'tab:brown'
}

# Create a pie chart using Matplotlib
fig, axes = plt.subplots(1, 2, figsize=(18,8))

# Plot the pie chart
wedges, texts, autotexts = axes[0].pie(
    rating_counts, colors=[color_mapping[label] for label in rating_counts.index],
    autopct='%1.1f%%', startangle=140,
    textprops={'fontsize': 15, 'fontweight': 'bold'},
    pctdistance=0.8,  # Move the percentage text inside the slices
    explode=(0.07, 0.07, 0.07, 0.07, 0.07, 0.07)  # Explode a slice for emphasis
)

# Create a custom legend for the Content Rating categories and their colors
legend_labels = [mpatches.Patch(color=color_mapping[label], label=label) for label in rating_counts.index]

# Add the legend to the first plot
axes[0].legend(handles=legend_labels, title="Content Rating", loc="center left", bbox_to_anchor=(1, 0.5), fontsize=13)
axes[0].set_title('Distribution of Films by Content Rating', fontsize=20, fontweight='bold')
axes[0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Set the Seaborn style
sns.set(style='whitegrid', palette='tab10')

# Create a histogram using Matplotlib
list1 = [df[df.ContentRating == gen].Year for gen in df.ContentRating.cat.categories]
mylabels = df.ContentRating.cat.categories
h = axes[1].hist(list1, bins=9, stacked=True, rwidth=1, label=mylabels, color=[color_mapping[label] for label in mylabels])

# Add the legend to the second plot
# axes[1].legend(title='Content Rating', loc='upper right', bbox_to_anchor=(1.4, 1))
axes[1].set_title('Histogram of Movies by Content Rating and Year', fontsize=20, fontweight='bold')
axes[1].set_xlabel('Year', fontweight='bold')
axes[1].set_ylabel('Number of Films', fontweight='bold')

# Save the combined figure
plt.tight_layout()
plt.savefig('D:\Syllabus\PROGRAMMING/Combined charts of Movies by Content Rating.png', dpi=500, bbox_inches='tight')

# Show the combined chart
plt.show()


# ### Streaming Platforms Evolution

# In[112]:


# Group the data by the release year and network to count the number of films aired on each network each year
yearly_network_counts = df.groupby(['Year', 'Network'])['Film'].count().reset_index()
# Sort the data by year and count in descending order
network_counts = yearly_network_counts.sort_values(['Year', 'Film'], ascending=[True, False])

# Get the top 10 networks for each year
top_networks_by_year = network_counts.groupby('Year').head(10)
# Set the style
sns.set_style('whitegrid')

# Create a line plot to visualize the changing of networks airing films over the years
plt.figure(figsize=(12,10))
sns.lineplot(data=top_networks_by_year, x='Year', y='Film', hue='Network', linewidth=3, markers=True, markersize=8,style='Network', palette='tab20')
# for network, data in top_networks_by_year.groupby('Network'):
#     for i, year in enumerate(data['Year']):
#         # Add data labels (legends) beside each line
#         plt.text(year, data['Film'].iloc[i], network, fontsize=5, ha='right', va='center', fontweight='bold')
plt.title('Changing of Networks Airing Films Over the Years',fontweight = 'bold', fontsize=20)
plt.xlabel('Year',fontweight = 'bold')
plt.ylabel('Number of Films Aired',fontweight = 'bold')
plt.legend(title='Network', loc='best', ncol=2, bbox_to_anchor=(1, 1))

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('D:\Syllabus\PROGRAMMING/networkchanging.png', dpi=500,bbox_inches='tight')
plt.show()


# ## Ranking and Popularity Ranking

# ### Correlation between ranking and popularity ranking

# In[325]:


sns.jointplot(data=df, x='Ranking', y='PopularityRanking', color='green')
plt.xlabel('Ranking',fontweight = 'bold', fontsize=30)
plt.ylabel('Popularity Ranking',fontweight = 'bold',fontsize=30)
plt.savefig('D:\Syllabus\PROGRAMMING/jointplot-rank-pop.png', dpi=500,bbox_inches='tight')
plt.show()


# In[326]:


k1 = sns.kdeplot(df.Ranking,df.PopularityRanking, 
                 shade=True, shade_lowest=False,cmap='Greens')
k1b = sns.kdeplot(df.Ranking,df.PopularityRanking, cmap='Greens') #make it look smoother
plt.title('Correlation between ranking and popularity ranking',fontweight = 'bold', fontsize=20)

plt.savefig('D:\Syllabus\PROGRAMMING/kdeplot-rank-pop.png', dpi=500,bbox_inches='tight')
plt.show()


# ### Boxplots of Ranking and Popularity Ranking by Content Rating categories

# In[296]:


fig, axes = plt.subplots(1, 2, figsize=(12,4))

sns.boxplot(data=df, x='ContentRating', y='Ranking', palette='tab10',ax=axes[0])
axes[0].set_title("Content Rating and Ranking", fontweight = 'bold', fontsize=15)
sns.boxplot(data=df, x='ContentRating', y='PopularityRanking', palette='tab10',ax=axes[1])
axes[1].set_title("Content Rating and Popularity Ranking", fontweight = 'bold', fontsize=15)
labels = ['13+ - Teens 13 or older', '15+ - Teens 15 or older',
       '18+ Restricted (violence & profanity)', 'G - All Ages',
       'Not Yet Rated', 'R - Restricted Screening (nudity & violence)']
axes[0].set_xticklabels(labels, rotation = 90, fontsize=8)
axes[1].set_xticklabels(labels, rotation = 90, fontsize=8)
plt.savefig('D:\Syllabus\PROGRAMMING/boxplot-contentrating-rankpop.png', dpi=500,bbox_inches='tight')
plt.show()


# ### Top KDramas with highest ranking and popularity ranking

# In[117]:


# Top 10 Drama according to rank
top10rank_film = pd.DataFrame(df.groupby('Film')[['Film','Ranking']].mean().sort_values('Ranking', ascending=True).round(2).head(10)).merge(df[['Film', 'Year']], on='Film', how='left')
top10rank_film


# In[119]:


# Top 10 Drama according to rank
top10pop_film = pd.DataFrame(df.groupby('Film')[['Film','PopularityRanking']].mean().sort_values('PopularityRanking', ascending=True).round(2).head(10)).merge(df[['Film', 'Year']], on='Film', how='left')
top10pop_film


# In[120]:


# Create a figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Select the DataFrame for top10_rank_film
ranking_df = top10rank_film[::-1]

# Define a color map for the bars
color_map_ranking = plt.get_cmap('tab10', len(ranking_df))

# Assign colors to the bars based on rank for ranking
colors_ranking = [color_map_ranking(rank / len(ranking_df)) for rank in range(len(ranking_df))]

# Create a horizontal bar plot for top 10 films by ranking
axes[0].barh(ranking_df['Film'], ranking_df['Ranking'], color=colors_ranking)

axes[0].set_title('Top 10 Films by Ranking', fontweight='bold', fontsize=15)
axes[0].set_xlabel('Average Ranking')
axes[0].tick_params(axis='y', labelrotation=0)

# Select the DataFrame for top10_pop_film
pop_df = top10pop_film[::-1]

# Define a color map for the bars
color_map_popularity = plt.get_cmap('tab10', len(pop_df))

# Assign colors to the bars based on rank for popularity ranking
colors_popularity = [color_map_popularity(rank / len(pop_df)) for rank in range(len(pop_df))]

# Create a horizontal bar plot for top 10 films by popularity ranking
axes[1].barh(pop_df['Film'], pop_df['PopularityRanking'], color=colors_popularity)

axes[1].set_title('Top 10 Films by Popularity Ranking', fontweight='bold', fontsize=15)
axes[1].set_xlabel('Average Popularity Ranking')
axes[1].tick_params(axis='y', labelrotation=0)

# Adjust layout and display the subplots
plt.tight_layout()
plt.savefig('D:\Syllabus\PROGRAMMING/top10-rank-pop-films.png', dpi=500,bbox_inches='tight')
plt.show()


# In[121]:


# Define a threshold for high ranking (you can adjust this threshold as needed)
high_ranking_threshold = 50.0

# Filter the DataFrame to select films with rankings above the threshold
high_ranking_films = df[df['Ranking'] < high_ranking_threshold]

# Group the high-ranking films by year and count the number of films in each year
yearly_high_ranking_counts = high_ranking_films['Year'].value_counts().reset_index()
yearly_high_ranking_counts.columns = ['Year', 'High_Ranking_Films_Count']

# Find the years with the highest number of high-ranking films
highest_rank = yearly_high_ranking_counts['High_Ranking_Films_Count'].max()
years_with_highest_rank = yearly_high_ranking_counts[yearly_high_ranking_counts['High_Ranking_Films_Count'] == highest_rank]

# Print the years with the highest number of high-ranking films
print("Years with the highest number of high-ranking films:")
print(years_with_highest_rank)


# In[122]:


# Define a threshold for high ranking (you can adjust this threshold as needed)
high_pop_threshold = 50.0

# Filter the DataFrame to select films with rankings above the threshold
high_pop_films = df[df['PopularityRanking'] < high_pop_threshold]

# Group the high-ranking films by year and count the number of films in each year
yearly_high_pop_counts = high_pop_films['Year'].value_counts().reset_index()
yearly_high_pop_counts.columns = ['Year', 'High_Popularity_Films_Count']

# Find the years with the highest number of high-ranking films
highest_pop = yearly_high_pop_counts['High_Popularity_Films_Count'].max()
years_with_highest_pop = yearly_high_pop_counts[yearly_high_pop_counts['High_Popularity_Films_Count'] == highest_pop]

# Print the years with the highest number of high-ranking films
print("Years with the highest number of high-popularity-ranking films:")
print(years_with_highest_pop)


# In[124]:


from tabulate import tabulate
print("Top 10 Dramas with Highest Ranking:")
print(tabulate(top10rank_film, headers="keys", tablefmt="grid"))
print("\nTop 10 Dramas with Highest Popularity Ranking:")
print(tabulate(top10pop_film, headers="keys", tablefmt="grid"))
print("\nYears with the highest number of high-ranking films:")
print(tabulate(years_with_highest_rank, headers="keys", tablefmt="grid"))
print("\nYears with the highest number of high-popularity-ranking films:")
print(tabulate(years_with_highest_pop, headers="keys", tablefmt="grid"))


# ### Top 10 in each feature in relation to Ranking and Popularity Ranking

# #### Main Cast (Actor/Actress)

# In[125]:


# Explode the list of actors into separate rows
exploded_df = df_merged.explode('Actor_name')

# Calculate the average rank for each actor
actor_avg_rank = round(exploded_df.groupby('Actor_name')['Ranking'].mean(),1).reset_index()
actor_avg_rank = actor_avg_rank.rename(columns={'Ranking': 'avg_rank'})

# Sort the results by avg_rank
actor_avg_rank = actor_avg_rank.sort_values(by='avg_rank')

# Display the top rows
top10rank_cast = actor_avg_rank.head(10)
top10rank_cast


# In[126]:


# Explode the list of actors into separate rows
exploded_df = df_merged.explode('Actor_name')

# Calculate the average rank for each actor
actor_avg_pop = round(exploded_df.groupby('Actor_name')['PopularityRanking'].mean(),1).reset_index()
actor_avg_pop = actor_avg_pop.rename(columns={'PopularityRanking': 'avg_pop'})

# Sort the results by avg_rank
actor_avg_pop = actor_avg_pop.sort_values(by='avg_pop')

# Display the top rows
top10pop_cast = actor_avg_pop.head(10)
top10pop_cast


# In[127]:


# Create a figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Select the DataFrame for top10rank_cast
ranking_df = top10rank_cast[::-1]

# Define a color map for the bars
color_map_ranking = plt.get_cmap('tab10', len(ranking_df))

# Assign colors to the bars based on rank for ranking
colors_ranking = [color_map_ranking(rank / len(ranking_df)) for rank in range(len(ranking_df))]

# Create a horizontal bar plot for top 10 actors/actresses by ranking
axes[0].barh(ranking_df['Actor_name'], ranking_df['avg_rank'], color=colors_ranking)

axes[0].set_title('Top 10 Actor/Actress by Ranking', fontweight='bold', fontsize=15)
axes[0].set_xlabel('Average Ranking')
axes[0].tick_params(axis='y', labelrotation=0)

# Select the DataFrame for top10pop_cast
pop_df = top10pop_cast[::-1]

# Define a color map for the bars
color_map_popularity = plt.get_cmap('tab10', len(pop_df))

# Assign colors to the bars based on rank for popularity
colors_popularity = [color_map_popularity(rank / len(pop_df)) for rank in range(len(pop_df))]

# Create a horizontal bar plot for top 10 popular actors/actresses by popularity
axes[1].barh(pop_df['Actor_name'], pop_df['avg_pop'], color=colors_popularity)

axes[1].set_title('Top 10 Popular Actor/Actress by Popularity', fontweight='bold', fontsize=15)
axes[1].set_xlabel('Average Popularity Ranking')
axes[1].tick_params(axis='y', labelrotation=0)

# Adjust layout and display the subplots
plt.tight_layout()
plt.savefig('D:\Syllabus\PROGRAMMING/top10-cast.png', dpi=500,bbox_inches='tight')
plt.show()


# In[128]:


def top_avg_ranking(group_column):
    # Group by the specified column and calculate the average ranking
    avg_rank = df.groupby(group_column)['Ranking'].mean().reset_index()
    avg_rank = avg_rank.rename(columns={'Ranking': 'avg_rank'})
    # Sort the results by average ranking
    return avg_rank.sort_values(by='avg_rank').head(10)
def top_avg_popularity(group_column):
    # Group by the specified column and calculate the average ranking
    avg_pop = df.groupby(group_column)['PopularityRanking'].mean().reset_index()
    avg_pop = avg_pop.rename(columns={'PopularityRanking': 'avg_pop'})
    # Sort the results by average ranking
    return avg_pop.sort_values(by='avg_pop').head(10)

top10rank_screenwriter = top_avg_ranking('Screenwriter')
top10rank_director = top_avg_ranking('Director')
top10rank_airdate = top_avg_ranking('AirDate')
top10rank_network = top_avg_ranking('Network')

top10pop_screenwriter = top_avg_popularity('Screenwriter')
top10pop_director = top_avg_popularity('Director')
top10pop_airdate = top_avg_popularity('AirDate')
top10pop_network = top_avg_popularity('Network')


# In[129]:


from tabulate import tabulate
print("Screenwriter Top 10 Ranking:")
print(tabulate(top10rank_screenwriter, headers="keys", tablefmt="grid"))
print("\nDirector Top 10 Ranking:")
print(tabulate(top10rank_director, headers="keys", tablefmt="grid"))
print("\nAirDate Top 10 Ranking:")
print(tabulate(top10rank_airdate, headers="keys", tablefmt="grid"))
print("\nNetwork Top 10 Ranking:")
print(tabulate(top10rank_network, headers="keys", tablefmt="grid"))
print("\nActors/Actress Top 10 Ranking:")
print(tabulate(top10rank_cast, headers="keys", tablefmt="grid"))


# In[130]:


from tabulate import tabulate
print("Screenwriter Top 10 Popularity Ranking:")
print(tabulate(top10pop_screenwriter, headers="keys", tablefmt="grid"))
print("\nDirector Top 10 Popularity Ranking:")
print(tabulate(top10pop_director, headers="keys", tablefmt="grid"))
print("\nAirDate Top 10 Popularity Ranking:")
print(tabulate(top10pop_airdate, headers="keys", tablefmt="grid"))
print("\nNetwork Top 10 Popularity Ranking:")
print(tabulate(top10pop_network, headers="keys", tablefmt="grid"))
print("\nActors/Actress Top 10 Popularity Ranking:")
print(tabulate(top10pop_cast, headers="keys", tablefmt="grid"))


# #### Screenwriters and Directors

# In[131]:


import matplotlib.pyplot as plt

# Create a figure with 4x2 subplots
fig, axes = plt.subplots(2, 2, figsize=(20, 12))

# List of the DataFrames and their titles for the top rankings
top_rankings = [top10rank_screenwriter, top10rank_director]
ranking_titles = ['Top 10 Screenwriters By Ranking', 'Top 10 Directors By Ranking']
# Define a color map for the bars
color_map_ranking = plt.get_cmap('tab10', len(top_rankings[0]))

for i, ax in enumerate(axes[:, 0]):
    ranking_df = top_rankings[i][::-1]
    
    # Assign colors to the bars based on rank
    colors = [color_map_ranking(rank / len(ranking_df)) for rank in range(len(ranking_df))]
    
    ax.barh(ranking_df['Screenwriter' if i == 0 else 'Director'],
            ranking_df['avg_rank'],
            color=colors)
    ax.set_title(ranking_titles[i], fontweight='bold', fontsize=15)
    ax.set_xlabel('Average Ranking')

# List of the DataFrames and their titles for the top popularity rankings
top_popularity = [top10pop_screenwriter, top10pop_director]
popularity_titles = ['Top 10 Screenwriters by Popularity', 'Top 10 Directors by Popularity']

# Define a color map for the bars
color_map_popularity = plt.get_cmap('tab10', len(top_popularity[0]))

for i, ax in enumerate(axes[:, 1]):
    pop_df = top_popularity[i][::-1]
    
    # Assign colors to the bars based on rank
    colors = [color_map_popularity(rank / len(pop_df)) for rank in range(len(pop_df))]
    
    ax.barh(pop_df['Screenwriter' if i == 0 else 'Director'],
            pop_df['avg_pop'],
            color=colors)
    ax.set_title(popularity_titles[i], fontweight='bold', fontsize=15)
    ax.set_xlabel('Average Popularity Ranking')

# Adjust layout and display the subplots
plt.tight_layout()
plt.savefig('D:\Syllabus\PROGRAMMING/top10-screen-direct.png', dpi=500,bbox_inches='tight')

plt.show()


# #### Air Dates and Networks

# In[132]:


import matplotlib.pyplot as plt

# Create a figure with 4x2 subplots
fig, axes = plt.subplots(2, 2, figsize=(20,12))

# List of the DataFrames and their titles for the top rankings
top_rankings = [top10rank_airdate, top10rank_network]
ranking_titles = ['Top 10 AirDates By Ranking', 'Top 10 Networks By Ranking']

# Define a color map for the bars
color_map_ranking = plt.get_cmap('tab10', len(top_rankings[0]))

for i, ax in enumerate(axes[:, 0]):
    ranking_df = top_rankings[i][::-1]
    
    # Assign colors to the bars based on rank
    colors = [color_map_ranking(rank / len(ranking_df)) for rank in range(len(ranking_df))]
    
    ax.barh(ranking_df['AirDate' if i == 0 else 'Network'],
            ranking_df['avg_rank'],
            color=colors)
    ax.set_title(ranking_titles[i], fontweight='bold', fontsize=15)
    ax.set_xlabel('Average Ranking')

# List of the DataFrames and their titles for the top popularity rankings
top_popularity = [top10pop_airdate, top10pop_network]
popularity_titles = ['Top 10 AirDates by Popularity', 'Top 10 Networks by Popularity']

# Define a color map for the bars
color_map_popularity = plt.get_cmap('tab10', len(top_popularity[0]))

for i, ax in enumerate(axes[:, 1]):
    pop_df = top_popularity[i][::-1]
    
    # Assign colors to the bars based on rank
    colors = [color_map_popularity(rank / len(pop_df)) for rank in range(len(pop_df))]
    
    ax.barh(pop_df['AirDate' if i == 0 else 'Network'],
            pop_df['avg_pop'],
            color=colors)
    ax.set_title(popularity_titles[i], fontweight='bold', fontsize=15)
    ax.set_xlabel('Average Popularity Ranking')

# Adjust layout and display the subplots
plt.tight_layout()
plt.savefig('D:\Syllabus\PROGRAMMING/top10-airdate-networks.png', dpi=500,bbox_inches='tight')

plt.show()

