from django.db import models

# 定義 NewsArticle 模型
class NewsArticle(models.Model):
    title = models.CharField(max_length=255, verbose_name="標題")
    description = models.TextField(verbose_name="描述", blank=True, null=True)
    published_at = models.DateTimeField(verbose_name="發佈時間")
    source_name = models.CharField(max_length=100, verbose_name="來源")
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "新聞文章"
        verbose_name_plural = "新聞文章"