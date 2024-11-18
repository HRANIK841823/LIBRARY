from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView
from .import forms
from .models import Book
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from . import forms
from accounts.models import UserAccount

class DetailBookView(DetailView):
    model=Book
    pk_url_kwarg='id'
    template_name='books/book_details.html'
    context_object_name = 'book'
    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        book= self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object # post model er object ekhane store korlam
        comments = book.comments.all()
        comment_form = forms.CommentForm()
        #  check borrow or not
        user = self.request.user
        if user.is_authenticated:
            context['has_borrowed'] = Borrow.objects.filter(user=user, book=book).exists()
        else:
            context['has_borrowed'] = False
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context
    
from django.shortcuts import  get_object_or_404, redirect
from django.contrib import messages
from .models import Book, Borrow

def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user_account = request.user.account

    if user_account.balance >= book.price:
        new_balance = user_account.balance - book.price
        user_account.balance = new_balance 
        user_account.balance_after_transiction = new_balance
        # Create a Borrow record
        user_account.save()
        Borrow.objects.create(user=request.user, book=book)

        messages.success(request, f"You have successfully borrowed {book.title}!")
        return redirect('profile')  
    else:
        messages.error(request, "Insufficient balance to borrow this book.")
        return redirect('book_details', book_id)  

def return_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user_account = request.user.account
    borrow_record = Borrow.objects.filter(user=request.user, book=book).first()
    
    if borrow_record:
        borrow_record.delete()  
        user_account.balance += book.price
        user_account.save()
        book.borrow_book = False
        book.save()

        messages.success(request, f"You have successfully returned {book.title}. Your balance has been updated!")
    else:
        messages.error(request, "You have not borrowed this book, so it cannot be returned.")

    return redirect('profile') 