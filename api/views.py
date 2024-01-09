from django.contrib.auth.models import User
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.urls import reverse
from .forms import UserRegistrationForm
from .token_generator import account_activation_token
from main.settings import EMAIL_HOST_USER


class RegisterView(View):
    template_name = 'registration/register.html'
    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')

        context = {
            'form': form
        }

        return render(request, self.template_name, context)


class LoginView(View):
    template_name = 'registration/login.html'
    def get(self, request):
        context = {
            'form': AuthenticationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

        context = {
            'form': form
        }

        return render(request, self.template_name, context)


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            token = account_activation_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_url = request.build_absolute_uri(reverse('verify_email', args=[uid, token]))
            send_mail(
                'Verify your email',
                f'Please click on the link to verify your email: {verification_url}',
                EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return render(request, 'registration/verification_sent.html')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        return redirect('register')

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/email_verified.html')
