from django.contrib import admin
from .models import NewsArticle

# 註冊 NewsArticle 模型到 Django 管理後台
@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "source_name", "published_at") # 顯示標題、來源和發佈時間
    search_fields = ("title", "source_name") # 標題和來源可以被搜索
    list_filter = ("source_name", "published_at") # 來源和發佈時間可以被過濾