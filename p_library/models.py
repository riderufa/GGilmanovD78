from django.db import models
from django.shortcuts import reverse
from PIL import Image
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    full_name = models.TextField()
    birth_year = models.SmallIntegerField()
    country = models.CharField(max_length=2)

    def __str__(self):
        return self.full_name

class Publishing(models.Model):
    publishing_name = models.TextField()

    def __str__(self):
        return self.publishing_name

class Friend(models.Model):
    full_name = models.TextField()

    def get_url(self):
        return reverse('p_library:friend_detail_url', kwargs={'f_n': self.full_name})

    def __str__(self):
        return self.full_name

class Book(models.Model):
    ISBN = models.CharField(max_length=13)
    title = models.TextField()
    description = models.TextField()
    year_release = models.SmallIntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publishing = models.ForeignKey(Publishing, on_delete=models.CASCADE, null=True, blank=True)
    friends = models.ManyToManyField(Friend, blank=True, related_name='books')
    # leasing_friends = models.ManyToManyField(
    #     Friend,
    #     through='Leasing',
    #     through_fields=('book', 'friend'),
    # )
    copy_count = models.BigIntegerField(default=1)
    leasing_count = models.BigIntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=19, decimal_places=2)
    avatar = models.ImageField(upload_to='book_avatars/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.title

    def author_full_name(obj):
        return obj.author.full_name

    
    def save(self):
        super().save()
        
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 100 or img.width > 100:
                output_size = (100, 100)
                img.thumbnail(output_size)
                img.save(self.avatar.path)

class UserProfile(models.Model):
    age = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # def __str__(self):
    #     return self.user

