from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='items'
    )
    image = models.ImageField(upload_to='items/images/', blank=True, null=True)
    title = models.CharField(max_length=200)
    caption = models.TextField(blank=True)
    link = models.URLField(max_length=500, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ['-created_at']

    def __str__(self):
        return self.title