from django.db import models
from django.urls import reverse
import uuid     # new
from django.contrib.auth import get_user_model
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2) 
    # max_digits是整数和小数点的总长度, decimal_prices指定小数位数

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,     # 在创建新的模型实例时,如果没有提供id的值,uuid.uuid4函数将被调用来生成一个新的UUID作为默认值
        editable=False,
    )
    cover = models.ImageField(upload_to="covers/", blank=True)      # new

    class Meta: 
        indexes = [
            models.Index(fields=["id"], name="id_index"),
        ]       # new
        permissions = [
            ("special_status", "Can read all books")    # 权限元组:(权限名称,权限描述),哪些用户可以阅读所有书籍
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):     # 为模型实例生成一个绝对URL
        return reverse("book_detail", args=[str(self.id)])
    
class Review(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    review = models.CharField(max_length=255)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.review
    

