"""
Name: Valery Leslie Tanada
frontend with GUI, reads from SQL database to display data to the user
"""

import sqlite3
import matplotlib
matplotlib.use('TkAgg')
import tkinter as tk
import webbrowser

class Display(tk.Toplevel):
    ''' the plot window '''
    def __init__(self, master, movie, option):
        super().__init__(master)
        self.LB_display = tk.Listbox(self, height=12, width=40)
        if option == 1:
            self.LB_display.insert(tk.END, "Movie: " + movie[0])
            self.LB_display.insert(tk.END, "Director: " + movie[3])
            self.LB_display.insert(tk.END, "Starring: ")
            for i in range(4, len(movie)):
                self.LB_display.insert(tk.END, movie[i])
        if option == 2:
            for title in movie:
                self.LB_display.insert(tk.END, "Movie: " + title[0])
                self.LB_display.insert(tk.END, "Director: " + title[3])
                self.LB_display.insert(tk.END, "Starring: ")
                for i in range(4, len(title)):
                    self.LB_display.insert(tk.END, title[i])
        self.LB_display.grid()
        self.mainloop()

class Dialog(tk.Toplevel):
    ''' the dialog window'''
    def __init__(self, master, str_sent, num):
        super().__init__(master)
        self._master = master
        self._option = num
        tk.Label(self, text = "Click on a " + str_sent + " to select").grid()
        scroll_bar = tk.Scrollbar(self, orient = "vertical")
        self._LB = tk.Listbox(self, height=12, width=40, yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=self._LB.yview)
        self._LB.grid(row = 1, column = 0)
        scroll_bar.grid(row = 1, column = 1, sticky = "nw")

        self._conn = sqlite3.connect('movie_database.db')
        self._cur = self._conn.cursor()
        self._list_tuple = []
        self._selection = ()

        if num == 0:
            self._cur.execute("SELECT * from MoviesDB")
            for record in self._cur.fetchall():
                self._list_tuple.append(record)
            self._list_tuple.sort(key = lambda x: x[num])
            count = 0
            for movie in self._list_tuple:
                if movie[num] != " " and movie[num] != "" and movie[num] != "TBD":
                    self._LB.insert(tk.END, movie[num])
                    print(count, movie[num])
                    count += 1
        elif num == 4:
            self._cur.execute("SELECT * from MoviesDB")
            for record in self._cur.fetchall():
                if record [num] != " " and record[num] != "" and record[num] != "TBD":
                    self._list_tuple.append(record)
            self._list_tuple.sort(key=lambda x: x[num])
            for actors in self._list_tuple:
                self._LB.insert(tk.END, actors[num])
        else:
            self._cur.execute("SELECT * from MonthsDB")
            for month in self._cur.fetchall():
                self._LB.insert(tk.END, month[1])

        self._LB.bind('<<ListboxSelect>>', self.callbackFct)
        if self._selection != ():
            self.destroy()
        self.grab_set()
        self.mainloop()
        self.quit()

    def callbackFct(self, event):
        ''' callback function for listbox to display an url'''
        select_tuple = self._LB.curselection()
        print(select_tuple)
        if self._option == 0:
            self._selection = self._list_tuple[select_tuple[0]]
            url = self._selection[1]
            if url != "N/A":
                webbrowser.open(url)
            else:
                tk.Label(self, text = "No URL Found.").grid()
        elif self._option == 4:
            self._selection = self._list_tuple[select_tuple[0]]
            self._master.setTuple(self._selection)
            self.destroy()
            self.quit()
        else:
            month = int(select_tuple[0]) + 1
            self._cur.execute("SELECT * from MoviesDB WHERE month = ?", (month,))
            self._master.setList(self._cur.fetchall())
            self.destroy()
            self.quit()

    def getSelection(self):
        ''' getting user selection '''
        return self._selection

class Main(tk.Tk):
    ''' the main window '''
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title("Movies")
        title = tk.Label(self, text="2021 Most Anticipated Movies", font=("Arial", 18, "bold"))
        title.grid(row=0, column = 1, columnspan = 2)
        tk.Label(self, text = "Search:").grid(row = 1, column = 0)
        button_cost = tk.Button(self, text="Webpage", fg = "blue", command = self.fct_1)
        button_cost.grid(row=1, column=1, sticky="e")
        button_data = tk.Button(self, text="Main Actor", fg = "blue", command = self.fct_2)
        button_data.grid(row=1, column=2)
        button_salary = tk.Button(self, text="Month", fg = "blue", command = self.fct_3)
        button_salary.grid(row=1, column=3)
        self.mainloop()
        self.quit()

    def fct_1(self):
        ''' to choose movies for webpage'''
        self.wait_window(Dialog(self, "movie", 0))
    def fct_2(self):
        ''' to choose actors and find films'''
        self.atuple = []
        Dialog(self, "actor", 4)
        Display(self, self.atuple, 1)
    def fct_3(self):
        ''' to choose a month and find films'''
        self.alist = []
        Dialog(self, "month", 2)
        Display(self, self.alist, 2)

    def setTuple(self, a_tuple):
        ''' setting tuple '''
        self.atuple = a_tuple

    def setList(self, a_list):
        ''' setting a list of tuples'''
        self.alist = a_list
Main()