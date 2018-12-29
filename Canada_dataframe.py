#!/usr/bin/env python
# coding: utf-8

# ### 1. Transform data in the table on Wikipedia page into the given pandas dataframe

# ##### To build a dataframe of the postal code of each neighborhood along with the borough name and neighborhood name

# In[44]:


get_ipython().system('pip install beautifulsoup4')
get_ipython().system('pip install lxml')
get_ipython().system('pip install html5lib')
get_ipython().system('pip install requests')

print("Installed successfully!")


# In[45]:


from bs4 import BeautifulSoup
import requests
import csv
import json
import xml
import pandas as pd


# In[46]:


# To extract the html codes from wikipedia page
res = requests.get(" https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M")
df_Canada = BeautifulSoup(res.content,'lxml')

# To create a dataframe to store data from html code
col_names = ['Postalcode','Borough','Neighborhood']
toronto = pd.DataFrame(columns = col_names)

# Loop through html code to find postcode, borough, neighborhood

content = df_Canada.find('div', class_='mw-parser-output')
table = content.table.tbody
postcode = 0
borough = 0
neighborhood = 0

for tr in table.find_all('tr'):
    i = 0  
    for td in tr.find_all('td'):
        if i == 0:
            postcode = td.text
            i = i + 1
        elif i == 1:
            borough = td.text
            i = i + 1
        elif i == 2: 
            neighborhood = td.text.strip('\n').replace(']','')      
    toronto = toronto.append({'Postalcode': postcode,'Borough': borough,'Neighborhood': neighborhood},ignore_index=True)

toronto.head()


# In[50]:


# To ignore cells with boroughs that are not assigned 
toronto = toronto[toronto.Borough!='Not assigned']
toronto = toronto[toronto.Borough!= 0]
toronto.reset_index(drop = True, inplace = True)
i = 0

# To assign neighbourhood = borough if a cell has a borough but no assigned neighbourhood
for i in range(0,toronto.shape[0]):
    if toronto.iloc[i][2] == 'Not assigned':
        toronto.iloc[i][2] = toronto.iloc[i][1]
        i = i+1

# To group similar postalcodes with more than one neighborhood and separated them with a comma
df = toronto.groupby(['Postalcode','Borough'])['Neighborhood'].apply(', '.join).reset_index()
df.head()


# In[51]:


# To drop cells with boroughs that are not assigned 
df = df.dropna()
empty = 'Not assigned'
df = df[(df.Postalcode != empty) & (df.Borough != empty) & (df.Neighborhood != empty)]

# To group similar postalcodes with more than one neighborhood and separated them with a comma
def neighborhood_list(grouped):    
    return ', '.join(sorted(grouped['Neighborhood'].tolist()))
                    
grp = df.groupby(['Postalcode', 'Borough'])
df2 = grp.apply(neighborhood_list).reset_index(name='Neighborhood')

df2.head()


# In[52]:


# Shape of dataframe
print(df2.shape)

