# Movie_Search
Movie Search and Display Manager with a GUI!

This back-end of this program traverses through a website, "https://editorial.rottentomatoes.com/article/most-anticipated-movies-of-2021/", 
and used BeautifulSoup and requests to obtain data points of movies listed in the website. Data is then created into a SQL database and .json file. The processing of this website from its HTML code is cumbersome, hence the many if statements in the backend processing of this website into data structure. However, they are a way to navigate through inconsistency with the website's HTML counterpart despite the neat display. 

The front-end of this program interacts with the user with three windows: a display, dialog, and main window.
It's initial page is meant for users to choose through three choices:
![alt text](initial_display.png)

From the main window, users are able to:
- Choose from all movies available through the 'Webpage' search:
  ![alt text](webpage_display.png)
  - Users will be directed to a webpage in Rotten Tomatoes of such movie
  ![alt text](click_webpage.png)
- Select their favorite actors and find their films, alphabetically 
  ![alt text](mainactor_display.png)
  - Users will be directed to a list of the actors' works of 2021 (e.g. Anya Taylor Joy)
  ![alt text](click_mainactor.png)
- Select a month from 2021 and be shown films released from that month
  ![alt_text](month_display.png)
  - Users will be directed to a list of movies released that month (e.g. August!)
  ![alt_text](click_month.png)

When users close the displays, they would be brought back to the main window. 
