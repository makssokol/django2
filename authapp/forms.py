import hashlib
import random
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from authapp.models import ArtShopUser, ArtShopUserProfile

class ArtShopUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(ArtShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = ArtShopUser
        fields = ("username", "password")

class ArtShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ArtShopUser
        fields = ("username", "first_name", "password1", "password2", "email", "age", "gender", "avatar")
    
    def __init__(self, *args, **kwargs):
        super(ArtShopUserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""

    def clean_age(self):
        data = self.cleaned_data["age"]
        if data < 21:
            raise forms.ValidationError("Too young for such purchases")
        return data

    def save(self, commit=True):
        user = super().save()
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user
    

class ArtShopUserEditForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(ArtShopUserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""

    def clean_age(self):
        data = self.cleaned_data["age"]
        if data < 21:
            raise forms.ValidationError("Too young for such purchases")
        return data

    class Meta:
        model = ArtShopUser
        fields = ("username", "first_name", "email", "age", "avatar")
        
        
    
class ArtShopUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = ArtShopUserProfile
        exclude = ('user', )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
  

    