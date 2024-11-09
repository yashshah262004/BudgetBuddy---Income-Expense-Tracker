from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.urls import reverse
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def signup_redirect(request):
    message.error(request, "Something went wrong, it may be that you already have account!")
    return redirect("expenses")

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use,choose another one '}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use,choose another one '}, status=409)
        return JsonResponse({'username_valid': True})


from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # Get user data
        username = request.POST['username']
        email = request.POST['email']  # Retaining email field
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already used!')
            return render(request, 'authentication/register.html', context)
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already used!')
            return render(request, 'authentication/register.html', context)

        # Validate password length
        if len(password) < 6:
            messages.error(request, 'Password too short. It should be at least 6 characters.')
            return render(request, 'authentication/register.html', context)

        # Create user account
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)  # Set the user's password
        user.is_active = True  # Set the user to active by default
        user.save()
        
        messages.success(request, 'Account successfully created! Please log in.')
        return redirect('login')



class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')

# @csrf_exempt
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' +
                                     user.username+' you are now logged in')
                    return redirect('expenses')
                messages.error(
                    request, 'Account is not active, please check your email')
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Invalid credentials, try again!')
            return render(request, 'authentication/login.html')

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')
    
