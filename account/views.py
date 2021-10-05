from django.shortcuts import redirect, reverse, render, get_object_or_404
from django.http import HttpResponse 
from .tokens import account_activation_token
from django.template.loader import *
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode   
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.views import View
from django.contrib import messages
from django.conf import settings
from io import BytesIO
from datetime import datetime


# Create your views here.
def index(request):
	context = {}
	return render(request,'customer/index.html', context)

def aboutus(request):
	form = ExampleForm()
	context = {'form': form}
	return render(request,'customer/aboutus.html', context)



def signup(request):
	form = createUserForm(request.POST or None)
	if request.method == 'POST':
		form = createUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.email = form.cleaned_data['email']
			user.is_active = False
			user.save()
			token = account_activation_token.make_token(user)
			user_id = urlsafe_base64_encode(force_bytes(user.id))
			url = 'http://' + 'vicatel.herokuapp.com' + reverse('confirm-email', kwargs={'user_id': user_id, 'token': token})
			message = get_template('customer/account_activation_email.html').render({'confirm_url': url})
			#message = render_to_string('customer/account_activation_email.html',{'user': user,'domain': Site.objects.get_current().domain,'uidb64': urlsafe_base64_encode(force_bytes(user.id)),'token': account_activation_token.make_token(user)})
			mail = EmailMessage('VICTORIA COMPUTERS AND TELECOMS LTD - Account Confirmation mail', message, to=[user.email], from_email=settings.EMAIL_HOST_USER, fail_silently=False)
			mail.content_subtype = 'html'
			mail.send()
			username = form.cleaned_data.get('username')
			form = createUserForm(request.POST or None)
			messages.success(request, 'A confirmation email has been sent to your email. Please confirm to finish registration. '+ username)
			return redirect('signin')

	context = {'form': form}
	return render(request, 'customer/signup.html', context)

class ConfirmRegistrationView(View):
    def get(self, request, user_id, token):
        user_id = force_text(urlsafe_base64_decode(user_id))

        user = User.objects.get(pk=user_id)

        context = {
            'message': 'Registration confirmation error. Please click the resend email to generate a new confirmation email.'
        }

        if user and account_activation_token.check_token(user, token):
            user.is_active=True
            user.save()
            context['message'] = 'Registration complete. Please login'

        return render(request, 'customer/registration_complete.html', context)



def signin(request):
	user = authenticate()
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('/')
		if user is None:	
			messages.info(request, 'username or password is incorrect')
		
	return render(request,'customer/signin.html')

def logoutUser(request):
	logout(request)
	return redirect('/')	
