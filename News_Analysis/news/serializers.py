from rest_framework import serializers
from .models import NewsArticle

# 定義 NewsArticle 的序列化器
class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = "__all__"