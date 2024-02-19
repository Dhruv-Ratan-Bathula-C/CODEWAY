import tkinter as tk
import json
import urllib.request
from tkinter import messagebox

class InspiringQuoteApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Inspiring Quote App")

        self.quote_label = tk.Label(master, text="", wraplength=300)
        self.quote_label.pack(pady=20)

        self.refresh_button = tk.Button(master, text="Refresh Quote", command=self.refresh_quote)
        self.refresh_button.pack(pady=5)

        self.share_button = tk.Button(master, text="Share Quote", command=self.share_quote)
        self.share_button.pack(pady=5)

        self.favorite_button = tk.Button(master, text="Favorite Quote", command=self.favorite_quote)
        self.favorite_button.pack(pady=5)

        self.load_quote_of_the_day()

    def load_quote_of_the_day(self):
        try:
            with urllib.request.urlopen("https://api.quotable.io/random") as response:
                data = json.loads(response.read())
                self.current_quote = f'"{data["content"]}" - {data["author"]}'
                self.quote_label.config(text=self.current_quote)
        except Exception as e:
            print(e)
            self.current_quote = "Failed to fetch quote. Please try again later."
            self.quote_label.config(text=self.current_quote)

    def refresh_quote(self):
        self.load_quote_of_the_day()

    def share_quote(self):
        messagebox.showinfo("Share Quote", f"Share the following quote:\n\n{self.current_quote}")

    def favorite_quote(self):
        messagebox.showinfo("Favorite Quote", "Quote added to favorites.")

def main():
    root = tk.Tk()
    app = InspiringQuoteApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
