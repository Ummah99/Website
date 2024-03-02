from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings

def home(request):
    return render (request, 'store/pannel1.html')

#---------------------------------------------------------------------------------
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "store/pannel1.html", {"fname": fname})
        else:
            messages.error(request, "Bad News, please try again.")
            return redirect('home')
        
    return render(request, 'store/login.html')

#-------------------------------------------------------------------------------
def register(request):
      if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email Ikurs!!"
        message2 = render_to_string('store/email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        messages.success(request, "Your account has been created successfully! Please check your email to confirm your email address in order to activate your account.")

        return render(request, 'store/registration_pending.html')  # Neue Seite für ausstehende Bestätigung
      return render(request, 'store/register.html')


#------------------------------------------------------------------------------------------
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            force_str(user.pk) + force_str(timestamp) +
            force_str(user.profile.signup_confirmation)
        )

generate_token = TokenGenerator()



#----------------------------------------------------------------------------------------------------
def activate(request,uidb64,token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your account has been activated!")
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')

#----------------------------------------------------------------------------

def logout(request):
    auth_logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')


#-------------------------------------------------------------------------------

from django.shortcuts import render, redirect


def upload(request):
    return render(request, 'store/upload.html')