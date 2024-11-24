from django.db import models

class Notes(models.Model):
    """
    Notes(标题，作者，内容，内容类别，通用类别，概要，发布时间，修改时间)
    """
    title = models.CharField(max_length=40)
    author = models.CharField(max_length=40)
    content = models.TextField()
    content_type = models.CharField(max_length=40)
    general_type = models.CharField(max_length=40)
    outline = models.TextField(null=True, blank=True)
    publish_date = models.DateTimeField(auto_now_add=True,null=True)
    update_date = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        ordering = ['-update_date','-general_type']




