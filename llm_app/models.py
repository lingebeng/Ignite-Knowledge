from django.db import models


class RAGVector(models.Model):
    """
    RAGVector(作者,名称,内容标签,更新时间)
    """
    author = models.CharField(max_length=40,null=True,blank=True)

    name = models.CharField(max_length=100)

    suffix = models.CharField(max_length=100,null=True,blank=True)

    content_type = models.CharField(max_length=40)

    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-update_date']
