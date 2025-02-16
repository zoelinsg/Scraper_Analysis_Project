from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NewsArticleViewSet, news_view, news_analysis_view, export_news_view, home_view,
    keyword_analysis_view, source_distribution_view, sentiment_analysis_view, category_classification_view
)

# 使用 DefaultRouter 註冊 API 視圖
router = DefaultRouter()
router.register(r"news", NewsArticleViewSet)

# 定義 URL 規則
urlpatterns = [
    path("", home_view, name="home"),  # 首頁
    path("news/", news_view, name="news"),  # 新聞列表
    path("analysis/", news_analysis_view, name="analysis"),  # 新聞分析
    path("export/", export_news_view, name="export"),  # 導出新聞
    path("keywords/", keyword_analysis_view, name="keywords"),  # 關鍵字分析
    path("source_distribution/", source_distribution_view, name="source_distribution"),  # 來源分佈分析
    path("sentiment_analysis/", sentiment_analysis_view, name="sentiment_analysis"),  # 文章情感分析
    path("category_classification/", category_classification_view, name="category_classification"),  # 類別分類分析
    path("api/", include(router.urls)),  # API 路由
]