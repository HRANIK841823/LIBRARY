#message import
from django.contrib import messages
from django.shortcuts import render,redirect
from django.views.generic import FormView ,CreateView
from .forms import UserRegistrationForm
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
#EMAIL SENDING IMPORT
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
#Email sending Function
def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
# Create your views here.
class UserRegistrationView(FormView):
    template_name='accounts/user_registration.html'
    form_class=UserRegistrationForm
    success_url=reverse_lazy('registration')
    def form_valid(self,form):
        # print(form.cleaned_data)
        user=form.save()
        login(self.request,user) #request kortechi ,k korteche user
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name='accounts/user_login.html'
    def get_success_url(self) -> str:
        return reverse_lazy('home')
    
class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
    




from .models import UserAccount
from .forms import DepositForm   
#deposit
def deposit(request):
    # Ensure the user has an associated account
    user_account, created = UserAccount.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            # Update user's balance
            user_account.balance += amount
            user_account.save()

            # Provide feedback to the user
            messages.success(request, f"Deposit of {amount} was successful! Your new balance is {user_account.balance}.")
            send_transaction_email(request.user, amount, "Deposite Message", "accounts/deposit_email.html")
            return redirect('profile')  # Or wherever you want to redirect the user
    else:
        form = DepositForm()
        
    return render(request, 'accounts/deposit.html', {'form': form})

#profile
def profile(request):
    user_account, created = UserAccount.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'user_account': user_account})