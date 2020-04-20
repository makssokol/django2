from django.conf import settings
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from authapp.forms import ArtShopUserEditForm, ArtShopUserLoginForm, ArtShopUserProfileEditForm, ArtShopUserRegisterForm
from django.core.mail import send_mail
from artshop import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction
from authapp.models import ArtShopUser



def login(request):
    title = "login"

    login_form = ArtShopUserLoginForm(data=request.POST or None)
    next_page = request.GET["next"] if "next" in request.GET.keys() else ""
    if request.method == "POST" and login_form.is_valid():
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if "next_page" in request.POST.keys():
                return HttpResponseRedirect(request.POST["next_page"])
            return HttpResponseRedirect(reverse("main"))
    
    content = {"title": title, "login_form": login_form, "next_page": next_page}
    return render(request, "authapp/login.html", content)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("main"))


def register(request):
    title = "registration"

    if request.method == "POST":
        register_form = ArtShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_email(user):
                print('Verification email sent')
                return HttpResponseRedirect(reverse("auth:login"))
            else:
                print('Email sending error')
                return HttpResponseRedirect(reverse("auth:login"))
    else:
        register_form = ArtShopUserRegisterForm()

    content = {"title": title, "register_form": register_form}
    return render(request, "authapp/register.html", content)


@login_required
@transaction.atomic
def edit(request):
    title = "edit"

    if request.method == "POST":
        edit_form = ArtShopUserEditForm(request.POST, request.FILES, 
                                        instance=request.user)
        profile_form = ArtShopUserProfileEditForm(request.POST, request.FILES, 
                                        instance=request.user.artshopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse("auth:edit"))
    else:
        edit_form = ArtShopUserEditForm(instance=request.user)
        profile_form = ArtShopUserProfileEditForm(
            instance=request.user.artshopuserprofile)
    content = {
        "title": title, 
        "edit_form": edit_form, 
        "profile_form": profile_form,
        "media_url": settings.MEDIA_URL}
    return render(request, "authapp/edit.html", content)


def send_verify_email(user):
    verify_link = reverse(
        'auth:verify', 
        kwargs={
            'email': user.email, 
            'activation_key': user.activation_key
            })
    title = f'Confirm your account authorization {user.username}'
    message = f'For account authorization {user.username} on website \
        {settings.DOMAIN_NAME} follow the link: \n {settings.DOMAIN_NAME}{verify_link}'
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ArtShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        else:
            print(f'error user activation: {user}')
        return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error user activation: {e.args}')
        return HttpResponseRedirect(reverse('main'))
