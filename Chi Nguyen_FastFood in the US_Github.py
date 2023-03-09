#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 16:04:00 2022

@author: Khanh Chi Nguyen
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import matplotlib
import os

dpi = 300

# Set working path for this project
project_dir = os.getcwd()

# Import data set:
df = pd.read_csv('/Users/kienguyen/Documents/Data/Fastfood in US/Datafiniti_Fast_Food_Restaurants.csv', sep=',')
df.info()
#%%
# Do the EDA on the data set
# Drop columns that not necessary:
df = df.iloc[:,[1,4,5,6,7,9,10,11,12,13]]
# Change column 'name' to 'brand' for better understanding
df = df.rename(columns={df.columns[7]:'brand'})
df.info()
# Have a look on unique value of each column:
for i in df.columns:
    print(i)
    print(df[i].unique())
    
# Check missing data:
df[df.isnull().values.any(axis=1)]
df.isnull().sum()

#Convert to lower case:
df['categories'] = df.categories.apply(lambda x: " ".join(x.lower() for x in x.split()))

# Standardize Categories:
# group 1: fast food, bruger, sandwich, pizza, & others -> Fast Food
# group 2: american food -> American Food
# group 3: mexican, taco -> Mexican food
# group 4: gas station, convenient, mall store -> Gas, Convenient, Mall
# group 5: ice cream shop -> IceCream
# group 6: asian, chinese, sushi -> Asian Food
df['categories_clean'] = list(map(lambda x : 'Fast Food' if any(item in x for item in ['fried chicken',"sandwich","pizza",'burger']) else x, df['categories']))
df['categories_clean'] = list(map(lambda x : 'American Food' if any(item in x for item in ['american']) else x, df['categories_clean']))
df['categories_clean'] = list(map(lambda x : 'Mexican Food' if any(item in x for item in ['mexican','taco']) else x, df['categories_clean']))
df['categories_clean'] = list(map(lambda x : 'Gas, Convenient, Mall' if any(item in x for item in ['gas','convenient','mall']) else x, df['categories_clean']))
df['categories_clean'] = list(map(lambda x : 'Ice Cream' if any(item in x for item in ['ice cream']) else x, df['categories_clean']))
df['categories_clean'] = list(map(lambda x : 'Asian Food' if any(item in x for item in ['chinese','asian','asia','sushi']) else x, df['categories_clean']))
df['categories_clean'] = list(map(lambda x : 'Fast Food' if any(item in x for item in ['fast food']) else x, df['categories_clean']))

df['categories_clean'].unique()

#%%
# PLOT 1: Categories rank
# Create data to plot
categories_count = df['categories_clean'].value_counts(ascending = False)
categories = pd.Series(list(categories_count.index))
categories_count.index = range(len(categories_count))
# plot the horizontal bar
fig, ax = plt.subplots(figsize = (16, 8))
ax.bar(categories, categories_count,color = 'green')
ax.set_title('Number of store by Categories',fontsize = 20)
ax.set_xlabel('Categories',fontsize = 15)
ax.set_ylabel('Store', fontsize = 15)
ax.set_xticklabels(categories, fontsize=15)
# function to add value labels
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i,y[i]+100,y[i], ha = 'center', fontsize= 'large', alpha = None)
        
addlabels(categories, categories_count)
plt.tight_layout()

plot1_name = 'NNumber of store by Categories.png'
fig.savefig(project_dir + "/Chart/"+ plot1_name, dpi = dpi)

# PLOT 2: Store by Province
# Create data to plot
province_count = df['province'].value_counts(ascending = False)
province = pd.Series(list(province_count.index))
province_count.index = range(len(province_count))
# plot the horizontal bar
fig, ax = plt.subplots(figsize = (16, 8))
ax.bar(province, province_count,color = 'blue')
ax.set_title('Number of store by Province',fontsize = 20)
ax.set_xlabel('Province',fontsize = 15)
ax.set_ylabel('Store', fontsize = 15)
ax.set_xticklabels(province, fontsize=12)
# function to add value labels
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i,y[i]+20,y[i], ha = 'center', fontsize= 'medium', alpha = None)
        
addlabels(province, province_count)
plt.tight_layout()

plot2_name = 'Number of store by State.png'
fig.savefig(project_dir + "/Chart/"+ plot2_name, dpi = dpi)

# PLOT 3: Brand review
# Create data to plot
brand_count = df['brand'].value_counts(ascending = False)
brand_20 = brand_count.head(20)
brand = pd.Series(list(brand_20.index))
brand_20.index = range(len(brand_20))
# plot the horizontal bar
fig, ax = plt.subplots(figsize = (16, 8))
ax.bar(brand, brand_20,color = 'red')
ax.set_title('Top 20 FastFood brand in the US',fontsize = 20)
ax.set_xlabel('Brand',fontsize = 15)
ax.set_ylabel('Store', fontsize = 15)
ax.set_xticklabels(brand,fontsize=12,rotation=30)
# function to add value labels
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i,y[i]+30,y[i], ha = 'center', fontsize= 'large', alpha = None)
        
addlabels(brand, brand_20)
plt.tight_layout()
plot3_name = 'Top 20 Fastfood brand in the US.png'
fig.savefig(project_dir + "/Chart/"+ plot3_name, dpi = dpi)

# Plot 4: Store Density 
plot_province =pd.DataFrame({'STUSPS': province,'store':province_count})
states = gpd.read_file('/Users/kienguyen/Documents/Data/cb_2018_us_state_20m/cb_2018_us_state_20m.shp')
plot_merge=plot_province.merge(states,on='STUSPS')
plot_merge = plot_merge.rename(columns= {'STUSPS': 'state','store':'number_of_store'})
fig = px.choropleth(plot_merge, locations='state',
                    locationmode="USA-states", color='number_of_store', scope="usa",title='Number of store Density plot',
                )
fig.add_scattergeo(
    locations=plot_merge['state'],
    locationmode="USA-states", 
    text=plot_merge['state'],textfont={
        "color": ["black",'white','white','white','white','white','white','white','white','white','white','white','white',
                 'white','white','white','white','white','white','white','white',
                 'white','white','white','white','white','white',
                 'white','white','white','white','white','white','white','white','white','white','white',
                 'white','white','white','white','white','white','white','white','white','white','white',]},
    mode='text',
)

fig.show()


# PLOT 5: Top 5 Brand distribution around the US
# import US map:
states = gpd.read_file('/Users/kienguyen/Documents/Data/cb_2018_us_state_20m/cb_2018_us_state_20m.shp')
states = states.to_crs("EPSG:4326")
not_mainland = ['Alaska', 'Hawaii', "Puerto Rico"]
mainland_usa = states.query('NAME not in @not_mainland')
# create data:
brand_geo_df = df.iloc[:,[5,6,7,9]]
# Create point geometries
geometry = gpd.points_from_xy(brand_geo_df.longitude, brand_geo_df.latitude)
brand_geo_df = gpd.GeoDataFrame(brand_geo_df[['brand','latitude','longitude','province']], geometry=geometry)
brand_top5_df = brand_geo_df.loc[brand_geo_df['brand'].isin(['McDonald\'s','Taco Bell','Burger King','Subway','Arby\'s'])]
brand_top5_df = brand_top5_df.loc[~brand_top5_df['province'].isin(['HI','PR','AK'])]
# Plotting
point_palette = {'McDonald\'s': 'red', 'Taco Bell': 'green', 'Burger King' : 'blue','Subway':'green','Arby\'s':'yellow'}
cmap = matplotlib.colors.ListedColormap([point_palette[b] for b in brand_top5_df.brand.unique()])

fig, ax = plt.subplots(figsize=(24,18))
mainland_usa.plot(ax=ax, alpha=0.4, color='grey')
brand_top5_df.plot(column='brand', ax=ax, legend=True,cmap=cmap)
plt.title('Top 5 Brand distribution',fontsize=20)
ax.set_axis_off()  
plt.show()
plot5_name = 'Top 5 Brand distributionin the US.png'
fig.savefig(project_dir + "/Chart/"+ plot5_name, dpi = dpi)