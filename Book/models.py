from django.db import models
from Category.models import Category
from django.contrib.auth.models import User
# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="uploads/")
    description=models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category=models.ForeignKey(Category,related_name='books',on_delete=models.CASCADE)
    borrow_book = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class Comment(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name='comments')
    name=models.CharField(max_length=30)
    email=models.EmailField()
    body=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"Comments by {self.name}"

class Borrow(models.Model):
    user = models.ForeignKey(User, related_name='borrowed_books', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='borrows', on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
