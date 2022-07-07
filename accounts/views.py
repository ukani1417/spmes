from email import message
from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.models import faculty, user, student

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth import login, authenticate

from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from .models import user as User
from django.core.mail import send_mail, BadHeaderError

# Create your views here.

# Login Forget views
def loginpage(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_admin:
                request.session['user_id'] = user.id
                return redirect("project_types")
            if user.is_faculty:
                request.session['user_id'] = user.id
                return redirect("faculty")
            if user.is_student:
                request.session['user_id'] = user.id
                request.session['sid'] = user.student.sid
                return redirect("student")
                
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("loginpage")

    return render(request, 'loginblock/loginpage.html')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = user.objects.filter(Q(email=data)).first()
            if associated_users:
                newuser =  associated_users
                subject = "Password Reset Requested"
                email_template_name = "loginblock/password_reset_email.txt"
                c = {
                    "email": newuser.email,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(newuser.pk)),
                    "user": newuser,
                    'token': default_token_generator.make_token(newuser),
                    'protocol': 'http',
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, 'spmesdaiict@gmail.com',
                                [newuser.email], fail_silently=False)
                except BadHeaderError:
                    messages.error(request,"Invalid header Found")
                    return redirect("password_reset/")
                return redirect("/password_reset/done/")
            else:
                messages.info(request, "You are not registred  here.")
                redirect("password_reset/")
    password_reset_form  =PasswordResetForm()
    return render(request, template_name="loginblock/password_reset.html", context={"password_reset_form": password_reset_form})


def logout_request(request):
    logout(request)
    messages.success(request, "Logout Succesfully")
    return redirect("/")



# Admin Views
