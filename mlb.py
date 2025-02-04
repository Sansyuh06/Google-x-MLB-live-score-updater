import tkinter as tk
from tkinter import ttk

def update_score(team, points):
    scores[team] += points
    update_display()

def reset_scores():
    scores["home"] = 0
    scores["away"] = 0
    update_display()

def update_display():
    home_score_label.config(text=str(scores["home"]))
    away_score_label.config(text=str(scores["away"]))

def update_team_name(entry, label):
    label.config(text=entry.get())

# Initialize the main window
root = tk.Tk()
root.title("MLB Score Updater")
root.geometry("360x640")  # Mobile-friendly dimensions
root.configure(bg="#f0f0f0")

# Score dictionary
scores = {"home": 0, "away": 0}

# Frame setup
frame = ttk.Frame(root, padding=10)
frame.pack(expand=True, fill=tk.BOTH)

# Create a grid layout
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

# Home team section
home_frame = ttk.LabelFrame(frame, text="Home Team", padding=10)
home_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
home_entry = ttk.Entry(home_frame, font=("Arial", 14))
home_entry.insert(0, "Home Team")
home_entry.pack(pady=5)
home_entry.bind("<KeyRelease>", lambda e: update_team_name(home_entry, home_label))
home_score_label = ttk.Label(home_frame, text="0", font=("Arial", 20))
home_score_label.pack(pady=5)

# Away team section
away_frame = ttk.LabelFrame(frame, text="Away Team", padding=10)
away_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
away_entry = ttk.Entry(away_frame, font=("Arial", 14))
away_entry.insert(0, "Away Team")
away_entry.pack(pady=5)
away_entry.bind("<KeyRelease>", lambda e: update_team_name(away_entry, away_label))
away_score_label = ttk.Label(away_frame, text="0", font=("Arial", 20))
away_score_label.pack(pady=5)

# Buttons container
buttons_frame = ttk.LabelFrame(frame, text="Scoring Actions", padding=10)
buttons_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")

# Create two columns for buttons
buttons_frame.columnconfigure(0, weight=1)
buttons_frame.columnconfigure(1, weight=1)

# Buttons for scoring actions
scoring_actions = [
    ("Single", 1), ("Double", 2), ("Triple", 3), ("Home Run", 4),
    ("Run", 1), ("RBI", 1), ("Walk", 1), ("Hit by Pitch", 1),
    ("Stolen Base", 2), ("Caught Stealing", -1), ("Win", 4), ("Save", 2),
    ("Inning Pitched", 1), ("Earned Run Allowed", -1)
]

for i, (action, points) in enumerate(scoring_actions):
    ttk.Button(buttons_frame, text=f"{action} (Home)", command=lambda p=points: update_score("home", p)).grid(row=i, column=0, padx=5, pady=2, sticky="ew")
    ttk.Button(buttons_frame, text=f"{action} (Away)", command=lambda p=points: update_score("away", p)).grid(row=i, column=1, padx=5, pady=2, sticky="ew")

# Reset button
reset_button = ttk.Button(frame, text="Reset Scores", command=reset_scores)
reset_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

root.mainloop()