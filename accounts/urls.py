from django.urls import path,include
from .views import UserRegistrationView,UserLoginView,UserLogoutView,deposit,profile
from Book.views import return_book
urlpatterns = [
    path('registration/',UserRegistrationView.as_view(),name="registration"),
    path('login/',UserLoginView.as_view(),name="login"),
    path('logout/',UserLogoutView.as_view(),name="logout"),
    path('deposit/',deposit,name="deposit"),
    path('profile/',profile,name="profile"),
    path('return/<int:book_id>/', return_book, name='return_book'),   
]