from collections import Counter
from textblob import TextBlob
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import NewsArticle
from .serializers import NewsArticleSerializer
from dotenv import load_dotenv
from io import BytesIO
import requests
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 使用非交互式後端
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import os

# 加載 .env 檔案
load_dotenv()

# 獲取 API Key
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

# 定義 NewsAPI 的 URL
NEWS_URL = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWSAPI_KEY}"

# 定義 NewsArticle 的 ViewSet
class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer

# 顯示首頁的視圖
def home_view(request):
    return render(request, "home.html")

# 獲取新聞資料的函數
def fetch_news():
    response = requests.get(NEWS_URL)
    data = response.json()
    articles = data.get("articles", [])
    return pd.DataFrame(articles)[["title", "description", "publishedAt", "source"]]

# 顯示新聞的視圖
def news_view(request):
    df = fetch_news()
    context = {"news": df.to_dict(orient="records")}
    return render(request, "news.html", context)

# 分析新聞資料的函數
def analyze_news(df):
    df["date"] = pd.to_datetime(df["publishedAt"]).dt.date
    df_count = df["date"].value_counts().sort_index()

    plt.figure(figsize=(10,5))
    sns.lineplot(x=df_count.index, y=df_count.values)
    plt.xlabel("Date")
    plt.ylabel("Number of News Articles")
    plt.title("News Publication Trend")

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_data = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return image_data

# 顯示新聞分析結果的視圖
def news_analysis_view(request):
    df = fetch_news()
    image_data = analyze_news(df)
    return render(request, "analysis.html", {"image": image_data})

# 將新聞資料保存為 CSV 的函數
def save_to_csv(df):
    media_dir = os.path.join("media")
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)
    path = os.path.join(media_dir, "news_data.csv")
    df.to_csv(path, index=False)
    return path

# 導出新聞資料的視圖
def export_news_view(request):
    df = fetch_news()
    csv_path = save_to_csv(df)
    with open(csv_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="news_data.csv"'
        return response

# 獲取並存儲新聞資料的函數
def fetch_and_store_news():
    response = requests.get(NEWS_URL)
    data = response.json()
    articles = data.get("articles", [])

    for article in articles:
        NewsArticle.objects.update_or_create(
            title=article["title"],
            defaults={
                "description": article.get("description", ""),
                "published_at": article["publishedAt"],
                "source_name": article["source"]["name"],
            },
        )

# 關鍵字分析的函數
def keyword_analysis(df):
    text = ' '.join(df['description'].dropna())
    words = text.split()
    counter = Counter(words)
    most_common = counter.most_common(10)
    return most_common

# 顯示關鍵字分析結果的視圖
def keyword_analysis_view(request):
    df = fetch_news()
    keywords = keyword_analysis(df)
    return render(request, "keywords.html", {"keywords": keywords})

# 來源分佈分析的函數
def source_distribution(df):
    source_count = df['source'].apply(lambda x: x['name']).value_counts()
    return source_count

# 顯示來源分佈分析結果的視圖
def source_distribution_view(request):
    df = fetch_news()
    source_count = source_distribution(df)

    plt.figure(figsize=(12,6))  # 調整圖表大小
    sns.barplot(x=source_count.index, y=source_count.values)
    plt.xlabel("Source")
    plt.ylabel("Number of Articles")
    plt.title("Source Distribution")
    plt.xticks(rotation=45, ha='right')  # 旋轉 x 軸標籤
    plt.tight_layout()  # 自動調整佈局以防止標籤被截掉

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_data = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return render(request, "source_distribution.html", {"image": image_data})

# 文章情感分析的函數
def sentiment_analysis(df):
    df['sentiment'] = df['description'].apply(lambda x: TextBlob(x).sentiment.polarity if x else None)
    sentiment_count = df['sentiment'].value_counts(bins=5, sort=False)
    return sentiment_count

# 顯示文章情感分析結果的視圖
def sentiment_analysis_view(request):
    df = fetch_news()
    sentiment_count = sentiment_analysis(df)

    plt.figure(figsize=(10,5))
    sns.barplot(x=sentiment_count.index.astype(str), y=sentiment_count.values)
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Articles")
    plt.title("Sentiment Analysis")
    plt.tight_layout()  # 自動調整佈局以防止標籤被截掉

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_data = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return render(request, "sentiment_analysis.html", {"image": image_data})

# 類別分類分析的函數
def category_classification(df):
    df['category'] = df['title'].apply(lambda x: classify_category(x))
    category_count = df['category'].value_counts()
    return category_count

# 類別分類的簡單分類器函數
def classify_category(title):
    if 'politics' in title.lower():
        return 'Politics'
    elif 'sports' in title.lower():
        return 'Sports'
    elif 'technology' in title.lower():
        return 'Technology'
    elif 'entertainment' in title.lower():
        return 'Entertainment'
    else:
        return 'Other'

# 顯示類別分類分析結果的視圖
def category_classification_view(request):
    df = fetch_news()
    category_count = category_classification(df)

    plt.figure(figsize=(12,6))  # 調整圖表大小
    sns.barplot(x=category_count.index, y=category_count.values)
    plt.xlabel("Category")
    plt.ylabel("Number of Articles")
    plt.title("Category Classification")
    plt.xticks(rotation=45, ha='right')  # 旋轉 x 軸標籤
    plt.tight_layout()  # 自動調整佈局以防止標籤被截掉

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_data = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return render(request, "category_classification.html", {"image": image_data})