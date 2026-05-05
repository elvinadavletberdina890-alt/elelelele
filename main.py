import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.movies = []
        self.load_movies()

        # --- Создание виджетов ---
        # Поля ввода
        tk.Label(root, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(root)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Жанр:").grid(row=1, column=0, padx=5, pady=5)
        self.genre_entry = tk.Entry(root)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Год выпуска:").grid(row=2, column=0, padx=5, pady=5)
        self.year_entry = tk.Entry(root)
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Рейтинг (0-10):").grid(row=3, column=0, padx=5, pady=5)
        self.rating_entry = tk.Entry(root)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(root, text="Добавить фильм", command=self.add_movie).grid(row=4, columnspan=2, pady=10)

        # Таблица для отображения фильмов
        self.columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(root, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=120)
        self.tree.grid(row=5, columnspan=2)

        # Фильтры
        tk.Label(root, text="Фильтр по жанру:").grid(row=6, column=0, padx=5)
        self.filter_genre = tk.Entry(root)
        self.filter_genre.grid(row=6, column=1, padx=5)

        tk.Label(root, text="Фильтр по году:").grid(row=7, column=0, padx=5)
        self.filter_year = tk.Entry(root)
        self.filter_year.grid(row=7, column=1, padx=5)

        tk.Button(root, text="Применить фильтры", command=self.apply_filters).grid(row=8, columnspan=2)

        # Заполнение таблицы при запуске
        self.update_table()

    def load_movies(self):
        if os.path.exists('movies.json'):
            with open('movies.json', 'r', encoding='utf-8') as f:
                self.movies = json.load(f)

    def save_movies(self):
        with open('movies.json', 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=2)

    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()

        # Валидация ввода
        if not title or not genre or not year_str or not rating_str:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")
            return

        try:
            year = int(year_str)
            if year > datetime.now().year or year < 1895:  # 1895 — год первого публичного кинопоказа
                raise ValueError("Некорректный год.")
            rating = float(rating_str)
            if not (0 <= rating <= 10):
                raise ValueError("Рейтинг должен быть от 0 до 10.")
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
            return

        # Добавление фильма
        movie = {"title": title, "genre": genre, "year": year, "rating": rating}
        self.movies.append(movie)
        self.save_movies()

        # Очистка полей и обновление таблицы
        self.clear_entries()
        self.update_table()

    def clear_entries(self):
        for entry in [self.title_entry, self.genre_entry, self.year_entry, self.rating_entry]:
            entry.delete(0, tk.END)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        filtered_movies = self.movies

        # Фильтрация по жанру (если есть текст в поле жанра)
        genre_filter = self.filter_genre.get().strip().lower()
        if genre_filter:
            filtered_movies = [m for m in filtered_movies if genre_filter in m["genre"].lower()]

         # Фильтрация по году (если есть число в поле года)
         year_filter = self.filter_year.get().strip()
         if year_filter.isdigit():
             filtered_movies = [m for m in filtered_movies if m["year"] == int(year_filter)]

         for movie in filtered_movies:
             self.tree.insert("", "end", values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def apply_filters(self):
         self.update_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()
