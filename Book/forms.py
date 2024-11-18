from .models import Book,Comment
from django import forms

class BookFrom(forms.ModelForm):
    class Meta:
        model=Book
        fields='__all__'

class CommentForm(forms.ModelForm):
    class Meta: 
        model = Comment
        fields = ['name', 'email', 'body']