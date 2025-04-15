# part3.py

"""
Final Project - Part 3: Data Processing
This file performs data selection, joins, and calculations across all three APIs:
- NYT Books (Fateha)
- Reddit (Sarina)
- Weather (Najmul)

Each section is labeled by group member.
Results will be saved to a text file as required for Part 3.
"""

import sqlite3

# === SETUP: Connect to database ===
DB_NAME = "final_project.db"

# ----------------------------------------------------
# 🔹 FATEHA'S SECTION: Books + Weather Analysis
# ----------------------------------------------------
# Tasks:
# - Join NYT books and weather data based on published_date
# - Calculate genre frequency by weather condition
# - Calculate average rank per weather condition
# - Prepare summary strings for output

# TODO: Write query + summary here


# ----------------------------------------------------
# 🔹 SARINA'S SECTION: Reddit + Weather Analysis
# ----------------------------------------------------
# Tasks:
# - Join Reddit and weather data by date
# - Count posts with "student", "college", "campus" keywords
# - Calculate average upvotes/comments by weather condition
# - Prepare summary strings for output

# TODO: Write query + summary here


# ----------------------------------------------------
# 🔹 NAJMUL'S SECTION: Weather Summary + Integration
# ----------------------------------------------------
# Tasks:
# - Summarize daily weather conditions from 4/6 to 4/13
# - Enable clean joins with Reddit and Books via date
# - Optionally prepare summary of total rainy/sunny/cloudy days

# TODO: Write query + summary here


# ----------------------------------------------------
# 🔸 WRITE TO TEXT FILE (ALL MEMBERS CONTRIBUTE)
# ----------------------------------------------------
# Tasks:
# - Combine summary outputs from all three sections
# - Write final combined summary to "weekly_analysis.txt"

# TODO: Combine and write results to file
