import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests

scores = {"home": 0, "away": 0}


def update_score(team, points):
    scores[team] += points
    update_score_display()

def reset_scores():
    scores["home"] = 0
    scores["away"] = 0
    update_score_display()

def update_score_display():
    home_score_label.config(text=str(scores["home"]))
    away_score_label.config(text=str(scores["away"]))

def update_team_name(entry, team_label, logo_label, team):
    team_name = entry.get()
    team_label.config(text=team_name)
    logo_url = get_logo_url(team_name)

    if logo_url:
        logo_image = get_logo_image(logo_url)
        if logo_image:
            logo_label.config(image=logo_image)
            logo_label.image = logo_image
        else:
            logo_label.config(text="Logo not found")
            logo_label.image = None
    else:
        logo_label.config(text="Logo not found")

def get_logo_url(team_name):
    api_url = f"https://api.sportsapi.com/logos/{team_name}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data.get("logo_url")
    except requests.RequestException:
        return None
print("hello")
def get_logo_image(logo_url):
    try:
        response = requests.get(logo_url, stream=True)
        response.raise_for_status()
        image_data = Image.open(response.raw)
        team_logo = ImageTk.PhotoImage(image_data)
        return team_logo
    except requests.RequestException:
        return None

root = tk.Tk()
root.title("MLB Score Updater")
root.geometry("360x640")
root.configure(bg="#f0f0f0")

frame = ttk.Frame(root, padding=10)
frame.pack(expand=True, fill=tk.BOTH)

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

home_frame = ttk.LabelFrame(frame, text="Home Team", padding=10)
home_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

home_entry = ttk.Entry(home_frame, font=("Arial", 14))
home_entry.insert(0, "Home Team")
home_entry.pack(pady=5)

home_score_label = ttk.Label(home_frame, text="0", font=("Arial", 20))
home_score_label.pack(pady=5)

home_logo_label = ttk.Label(home_frame)
home_logo_label.pack(pady=5)

home_label = ttk.Label(home_frame, text="Home Team", font=("Arial", 14))
home_label.pack(pady=5)

home_entry.bind("<KeyRelease>", lambda e: update_team_name(home_entry, home_label, home_logo_label, "home"))

away_frame = ttk.LabelFrame(frame, text="Away Team", padding=10)
away_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

away_entry = ttk.Entry(away_frame, font=("Arial", 14))
away_entry.insert(0, "Away Team")
away_entry.pack(pady=5)

away_score_label = ttk.Label(away_frame, text="0", font=("Arial", 20))
away_score_label.pack(pady=5)

away_logo_label = ttk.Label(away_frame)
away_logo_label.pack(pady=5)

away_label = ttk.Label(away_frame, text="Away Team", font=("Arial", 14))
away_label.pack(pady=5)

away_entry.bind("<KeyRelease>", lambda e: update_team_name(away_entry, away_label, away_logo_label, "away"))

buttons_frame = ttk.LabelFrame(frame, text="Scoring Actions", padding=10)
buttons_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")

buttons_frame.columnconfigure(0, weight=1)
buttons_frame.columnconfigure(1, weight=1)

scoring_actions = [
    ("Single", 1), ("Double", 2), ("Triple", 3), ("Home Run", 4),
    ("Run", 1), ("RBI", 1), ("Walk", 1), ("Hit by Pitch", 1),
    ("Stolen Base", 2), ("Caught Stealing", -1), ("Win", 4), ("Save", 2),
    ("Inning Pitched", 1), ("Earned Run Allowed", -1)
]

for i, (action, points) in enumerate(scoring_actions):
    ttk.Button(buttons_frame, text=f"{action} (Home)", command=lambda p=points: update_score("home", p)).grid(row=i, column=0, padx=5, pady=2, sticky="ew")
    ttk.Button(buttons_frame, text=f"{action} (Away)", command=lambda p=points: update_score("away", p)).grid(row=i, column=1, padx=5, pady=2, sticky="ew")

reset_button = ttk.Button(frame, text="Reset Scores", command=reset_scores)
reset_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

root.mainloop()
