from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Dash(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dash_posts')
    body = models.TextField()
    image = models.ImageField(upload_to='dash_images', blank=True, null=True)

    # === Yangi qo‘shilgan maydonlar ===
    contact = models.CharField(
        max_length=255,
        help_text="Telefon raqaming yoki Telegram URL (masalan: +99890..., yoki https://t.me/username)"
    )
    ad_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Reklama narxi so'mda"
    )


    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-publish',)


    def get_absolute_url(self):
        return reverse('jurnal_app:dash_detail', args=[self.publish.year,
                                             self.publish.month,
                                             self.publish.day,
                                             self.slug])
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    dash = models.ForeignKey(Dash, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.dash}'


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Maqola(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.CharField(max_length=150)
    content = models.TextField()
    image = models.ImageField(upload_to='article_images', blank=True, null=True)
    file = models.FileField(upload_to='article_files', blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    contact = models.CharField(max_length=255, blank=True, null=True) # Masalan, muallif telegram/telefon
    ad_price = models.DecimalField(max_digits=10, decimal_places=2, default=0) # Reklama taklif puli

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('jurnal_app:maqola_detail', args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug
        ])

class MaqolaComment(models.Model):
    maqola = models.ForeignKey(Maqola, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.maqola}'