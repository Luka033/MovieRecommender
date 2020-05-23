import tkinter as tk
from tkinter import messagebox
import movie_recommender

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Move Recommender System')
        # Width height
        master.geometry("700x500")
        # Create widgets/grid
        self.create_widgets()
        # Init selected item var
        self.selected_item = 0
        # Populate initial list

    def create_widgets(self):
        # Part
        self.movie_text = tk.StringVar()
        self.movie_label = tk.Label(self.master, text='Movie Name', font=('bold', 14), pady=20)
        self.movie_label.grid(row=0, column=0, sticky=tk.W)
        self.movie_entry = tk.Entry(self.master, textvariable=self.movie_text)
        self.movie_entry.grid(row=0, column=1)

        # Buttons
        self.add_btn = tk.Button(self.master, text="Search", width=12, command=self.search_similar_movies)
        self.add_btn.grid(row=0, column=2, pady=20)

        # Parts list (listbox)
        self.movie_list = tk.Listbox(self.master, height=20, width=30, border=1)
        self.movie_list.grid(row=5, column=0, columnspan=3, rowspan=6, pady=20, padx=20)

        # Create scrollbar
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=5, column=2)
        # Set scrollbar to parts
        self.movie_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.movie_list.yview)

        # Bind select
        self.movie_list.bind('<<ListboxSelect>>', self.select_movie)


    def populate_list(self, movie_list):
        # Delete items before update. So when you keep pressing it doesnt keep getting (show example by calling this twice)
        self.movie_list.delete(0, tk.END)
        # Loop through records
        for row in movie_list:
            # Insert into list
            self.movie_list.insert(tk.END, row)


    # Selected movie
    def search_similar_movies(self):
        if self.movie_text.get() == '':
            messagebox.showerror("Required Fields", "Please include all fields")
            return

        movie= movie_recommender.MovieRecommender()
        similar_movie_list = movie.recommend_movie(self.movie_text.get())
        if similar_movie_list:
            self.populate_list(similar_movie_list)
        else:
            messagebox.showerror("Movie Not Found", "Movie Not Found, Please Try Another Movie")
            return

    def select_movie(self, event):
        # Get index
        index = self.movie_list.curselection()[0]
        # Get selected item
        try:
            self.selected_item = self.movie_list.get(index)
            movie = movie_recommender.MovieRecommender()
            movie_info = movie.get_movie_info(self.selected_item)

            self.display_movie_info(movie_info)

            self.movie_entry.delete(0, tk.END)
            self.movie_entry.insert(tk.END, self.selected_item)
        except IndexError:
            pass

    # Takes in a movie and displays its information
    def display_movie_info(self, movie_info):
        # Movie text description
        self.description_text = tk.Text(self.master, height=20, width=30, border=1)
        self.description_text.grid(row=5, column=4, columnspan=3, rowspan=6, pady=20, padx=20)
        self.description_text.insert(tk.END, movie_info)


root = tk.Tk()
app = Application(master=root)
app.mainloop()