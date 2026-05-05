"""
Social Media Trends Dataset Generator
DVA Assignment 2 — Akshat Tripathi | 04914202023
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

platforms = ["Twitter", "Instagram", "YouTube", "Facebook", "TikTok"]
categories = ["Entertainment", "Sports", "Politics", "Technology", "Fashion", "Gaming", "Food", "Travel", "Education", "Health"]

hashtags_by_category = {
    "Entertainment": ["#Bollywood", "#Netflix", "#Movies", "#MusicMonday", "#OTT", "#WebSeries"],
    "Sports": ["#IPL2024", "#Cricket", "#FIFA", "#Olympics", "#Kabaddi", "#ChessOlympiad"],
    "Politics": ["#Elections2024", "#Budget2024", "#Parliament", "#Democracy", "#Vote", "#BJP"],
    "Technology": ["#AI", "#ChatGPT", "#Coding", "#Python", "#Startup", "#TechNews"],
    "Fashion": ["#OOTD", "#IndianFashion", "#Saree", "#Streetwear", "#BeautyTips", "#Skincare"],
    "Gaming": ["#BGMI", "#FreeFireIndia", "#Gaming", "#Esports", "#PubG", "#Valorant"],
    "Food": ["#IndianFood", "#Recipe", "#Foodie", "#Cooking", "#StreetFood", "#HealthyEating"],
    "Travel": ["#IncredibleIndia", "#Goa", "#Kashmir", "#Rajasthan", "#Travel", "#Wanderlust"],
    "Education": ["#StudyTips", "#UPSC", "#JEE", "#NEET", "#OnlineLearning", "#EdTech"],
    "Health": ["#MentalHealth", "#Yoga", "#Fitness", "#Ayurveda", "#WellBeing", "#Meditation"],
}

countries = [
    "India", "India", "India", "India", "India",   # Bias toward India
    "USA", "UK", "Brazil", "Indonesia", "Pakistan",
    "Bangladesh", "Australia", "Canada", "Germany", "France",
]

rows = []
start_date = datetime(2023, 1, 1)

for _ in range(2000):
    platform   = random.choice(platforms)
    category   = random.choice(categories)
    hashtag    = random.choice(hashtags_by_category[category])
    country    = random.choice(countries)
    date       = start_date + timedelta(days=random.randint(0, 364))
    month      = date.strftime("%B")
    
    # Platform-specific ranges
    if platform == "TikTok":
        posts       = random.randint(50_000, 5_000_000)
        likes       = int(posts * random.uniform(0.15, 0.60))
        views       = int(posts * random.uniform(5, 30))
        comments    = int(likes  * random.uniform(0.01, 0.08))
        shares      = int(likes  * random.uniform(0.05, 0.20))
    elif platform == "Instagram":
        posts       = random.randint(10_000, 2_000_000)
        likes       = int(posts * random.uniform(0.10, 0.45))
        views       = int(posts * random.uniform(3, 15))
        comments    = int(likes  * random.uniform(0.02, 0.10))
        shares      = int(likes  * random.uniform(0.03, 0.12))
    elif platform == "YouTube":
        posts       = random.randint(500, 200_000)
        likes       = int(posts * random.uniform(0.05, 0.20))
        views       = int(posts * random.uniform(20, 200))
        comments    = int(likes  * random.uniform(0.02, 0.15))
        shares      = int(likes  * random.uniform(0.01, 0.08))
    elif platform == "Twitter":
        posts       = random.randint(5_000, 1_000_000)
        likes       = int(posts * random.uniform(0.05, 0.25))
        views       = int(posts * random.uniform(2, 10))
        comments    = int(likes  * random.uniform(0.05, 0.20))
        shares      = int(likes  * random.uniform(0.10, 0.40))
    else:  # Facebook
        posts       = random.randint(8_000, 800_000)
        likes       = int(posts * random.uniform(0.08, 0.30))
        views       = int(posts * random.uniform(2, 8))
        comments    = int(likes  * random.uniform(0.03, 0.12))
        shares      = int(likes  * random.uniform(0.04, 0.15))

    engagement_rate = round((likes + comments + shares) / max(views, 1) * 100, 2)
    
    rows.append({
        "platform":        platform,
        "hashtag":         hashtag,
        "category":        category,
        "country":         country,
        "month":           month,
        "date":            date.strftime("%Y-%m-%d"),
        "posts":           posts,
        "likes":           likes,
        "views":           views,
        "comments":        comments,
        "shares":          shares,
        "engagement_rate": engagement_rate,
    })

df = pd.DataFrame(rows)
df.to_csv("Social_Media_Trends_India.csv", index=False)
print(f"Dataset created: {len(df)} rows")
print(df.head())
print(df.describe())
