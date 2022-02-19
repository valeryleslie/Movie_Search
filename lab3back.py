'''
Name: Valery Leslie Tanada
Backend file to get data
'''
import json
import sqlite3
import requests
from bs4 import BeautifulSoup
import collections
from collections import OrderedDict
import re

class Back:
    def __init__(self):
        '''
        Use requests and beautifulsoup to extracts movie info
        '''
        page = requests.get("https://editorial.rottentomatoes.com/article/most-anticipated-movies-of-2021/")
        # using html.parser, as lxml was not a found feature in my pycharm
        soup = BeautifulSoup(page.content, "html.parser")
        tags = soup.find('div', class_='articleContentBody')

        # Dictionary containing key: title, value: url, director name, month in of release, and actors.
        self._dict_info = collections.defaultdict(list)
        # Adding url onto the dictionary kets
        for title in tags.select('strong a')[6:91]:
            value = " "
            key = title.text
            if re.search('https', title['href']):
                value = title['href']
            self._dict_info[key].append(value)

        # variables needed
        index = 1
        change = 0
        num = 0
        self._max_actors = 0
        for movies in tags.find_all('p')[5:199]:
            if (index % 2 != change):
                full_desc = movies.text.encode("utf-8", "ignore").decode("utf-8")
                alist = full_desc.splitlines()
                try:
                    num += 1
                    # 38 and 96 are indexes of special cases on the website
                    if num != 38 and num != 96:
                        index_list = 0
                        # traversing the text until finding a non whitespace character
                        while alist[index_list] == "":
                            index_list += 1
                        # inserting title if does not exist in dictionary and adding 'N/A' website
                        raw_title = str(alist[index_list])
                        index_cancel = raw_title.find("(")
                        if index_cancel != -1:
                            raw_title = raw_title[:index_cancel - 1]
                        if raw_title not in self._dict_info:
                            self._dict_info[raw_title].append("N/A")
                        # Appending months
                        if num == 1:
                            self._dict_info[raw_title].append("1")
                        elif num > 1 and num < 10:
                            self._dict_info[raw_title].append("2")
                        elif num >= 10 and num < 15:
                            self._dict_info[raw_title].append("3")
                        elif num >= 15 and num < 20:
                            self._dict_info[raw_title].append("4")
                        elif num >= 20 and num < 26:
                            self._dict_info[raw_title].append("5")
                        elif num >= 26 and num < 34:
                            self._dict_info[raw_title].append("6")
                        elif num >= 34 and num < 46:
                            self._dict_info[raw_title].append("7")
                        elif num >= 46 and num < 51:
                            self._dict_info[raw_title].append("8")
                        elif num >= 51 and num < 61:
                            self._dict_info[raw_title].append("9")
                        elif num >= 61 and num < 70:
                            self._dict_info[raw_title].append("10")
                        elif num >= 70 and num < 75:
                            self._dict_info[raw_title].append("11")
                        elif num >= 75 and num < 82:
                            self._dict_info[raw_title].append("12")
                        else:
                            self._dict_info[raw_title].append("TBD")
                        # Appending director onto the dictionary list
                        raw_dir = alist[index_list + 1]
                        director = str(raw_dir)[13:]
                        self._dict_info[raw_title].append(director)
                        # Appending actors onto the dictionary list
                        raw_act = str(alist[index_list + 2])
                        actors = raw_act[10:]
                        actor_list = actors.split(",")
                        for actor in actor_list:
                            actor = actor.strip()
                            self._dict_info[raw_title].append(actor)
                    # Special Case text
                    if num == 96:
                        index += 1
                    # calculating most actors/actresses
                    if len(actor_list) > self._max_actors:
                        self._max_actors = len(actor_list)
                except IndexError:
                    if change == 0:
                        change = 1
                    else:
                        change = 0
                    pass
            index += 1

        self._dict_info["MAX ACTORS"].append(str(self._max_actors))

    def createJSON(self):
        """creating a JSON file from the data read in"""
        with open('movie.json', 'w') as out_file:
            json.dump(self._dict_info, out_file, indent = 3)

    def createSQL(self):
        ''' creating SQL database'''
        conn = sqlite3.connect('movie_database.db')
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS MoviesDB")
        cur.execute('''CREATE TABLE MoviesDB(
                        name TEXT NOT NULL PRIMARY KEY,
                        url TEXT,
                        month TEXT,
                        director TEXT,
                        actor0 TEXT,
                        actor1 TEXT,
                        actor2 TEXT,
                        actor3 TEXT,
                        actor4 TEXT,
                        actor5 TEXT,
                        actor6 TEXT,
                        actor7 TEXT,
                        actor8 TEXT,
                        actor9 TEXT,
                        actor10 TEXT)''')
        cur.execute("DROP TABLE IF EXISTS MonthsDB")
        cur.execute('''CREATE TABLE MonthsDB(
                            month TEXT PRIMARY KEY,
                            name TEXT)''')
        with open('movie.json', 'r') as fh:
            d = json.load(fh)
        for title, values in d.items():
            a_list = [" "]*15
            a_list[0] = title
            count = 1
            for info in values:
                a_list[count] = info
                count += 1
            tupled_info = tuple(a_list)
            cur.execute('''INSERT INTO MoviesDB
                        VALUES
                        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', tupled_info)
        month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        for i in range(1, 13):
            cur.execute('''INSERT INTO MonthsDB
                            VALUES
                            (?, ?)''', (i, month_list[i-1]))
        conn.commit()

# Calling all needed functions
backend = Back()
backend.createJSON()
backend.createSQL()