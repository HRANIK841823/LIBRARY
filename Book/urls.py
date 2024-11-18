from django.urls import path,include
from .views import DetailBookView,borrow_book
urlpatterns = [
      path('details/<int:id>',DetailBookView.as_view(),name='book_details'),
      path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
   
]