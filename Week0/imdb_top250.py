''' This program retrieves the top 250 movies from the IMDB database and stores the titles,
    years, and directors in a dictionary. The program then converts the data into a xlsx file as the final output.'''

#Importing Libraries
from bs4 import BeautifulSoup
import requests
import re
import json 
import pandas as pd

# Downloading imdb top 250 movie's data
url = 'http://www.imdb.com/chart/top'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

movies = soup.select('td.titleColumn')
links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]

ratings = [b.attrs.get('data-value')
		for b in soup.select('td.posterColumn span[name=ir]')]

votes = [b.attrs.get('data-value')
		for b in soup.select('td.ratingColumn strong')]



# create a empty list for storing
# movie information
List = []

# Iterating over movies to extract
# each movie's details
for index in range(0, len(movies)):
	
	# Separating movie into: 'place',
	# 'title', 'year'
	movie_string = movies[index].get_text()
	movie = (' '.join(movie_string.split()).replace('.', ''))
	movie_title = movie[len(str(index))+1:-7]
	year = re.search('\((.*?)\)', movie_string).group(1)
	place = movie[:len(str(index))-(len(movie))]
	data = {"movie_title": movie_title,
			"year": year,
			"place": place,
			"star_cast": crew[index],
			"rating": ratings[index],}
	List.append(data)

# printing movie details with its rating.
#for movie in list:
#	print(movie['place'], '-', movie['movie_title'], '('+movie['year'] +
#		') -', 'Starring:', movie['star_cast'], movie['rating'])

final_json = json.dumps(List)

# writing data to a json file
with open("imdb_top250.json", "w") as final:
   json.dump(List, final)


#converting imdb_top100.json to a xlsx file with pandas
pd.read_json("imdb_top250.json").to_excel("imdb_top250.xlsx")
# ------------ Upper part of code is fine, it collects data from IMDB website and stores the parsed values in a json file ------------ #


#making a general list for storing all the director names

#initialization of variables
director_list = []
director_dictionary = {}
director_json = []
for i in List:   #iterating over the list of dictionaries created above and storing the director names in a list
    director_list.append((i['star_cast'].split('(dir.)')[0]))

#unique values in director dictonary with name as keys and number of times the name appears as values
def unique_values(lst, dict):  
    for i in lst:
        if i not in dict:
            dict[i] = 1
        else:
            dict[i] += 1
    return dict

director_dictionary = unique_values(director_list, director_dictionary) #calling the function to update the dictionary

# writing data in a different format i.e from a dictionary to a list of dictionaries 
# with keys as the name of the director and values as the number of times the director appears in the list
for index in range(0, len(director_dictionary)):
    director_json.append({"name": list(director_dictionary.keys())[index],
                            "number": list(director_dictionary.values())[index]})


#writing director data to a separate json file
with open("dir_top250.json", "w") as final:
   json.dump(director_json, final)

#converting director data to a xlsx file with pandas
pd.read_json("dir_top250.json").to_excel("dir_top250.xlsx")

