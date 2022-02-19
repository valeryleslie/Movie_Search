# Movie_Search
Movie Search with a GUI 

This back-end of this program traverses through a website, "https://editorial.rottentomatoes.com/article/most-anticipated-movies-of-2021/", 
and used BeautifulSoup and requests to obtain data points of movies listed in the website. Data is then created into a SQL database and .json file. 

The front-end of this program interacts with the user with three windows: a display, dialog, and main window. 

Users are able to:
- Choose from all movies available
  - Users will be directed to a webpage in Rotten Tomatoes of such movie
- Select their favorite actors and find their films
- Select a month from 2021 and be shown films released from that month
