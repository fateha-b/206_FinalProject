# 206_FinalProject
SI 206 Final Project

# 📚 Students, Books, & Bad Weather

**Team Members:**  
Fatehatul Bushra, Najmul Ritu, Sarina Hameed

---

## 🔍 Project Overview

This project explores how weather affects students’ reading and online habits. We used three APIs:
- **Open-Meteo** for weather data
- **NYT Books API** for bestsellers by genre
- **Reddit API** for post activity in college-related subreddits

We analyzed trends such as book popularity and Reddit engagement based on weather.

---

## 🗂 Files

- `nyt_books.py` – collects and stores NYT book data  
- `reddit_api.py` – collects Reddit post data  
- `weather_2025_data.py` – collects weather data  
- `part3.py` – analyzes and outputs results to `weekly_analysis.txt`  
- `visualizations.py` – generates charts and word cloud  
- `final_project.db` – final database  
- `weekly_analysis.txt` – output summary  

---

## ▶️ How to Run

```bash
1. Install packages:
pip install requests seaborn wordcloud
2. Run the data collection strips
python nyt_books.py
python reddit_api.py
python weather_2025_data.py
3. Run analysis
python part3.py
4. Run visualizations
python visualizations.py
