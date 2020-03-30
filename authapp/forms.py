from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import ArtShopUser

class ArtShopUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(ArtShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = ArtShopUser
        fields = ("username", "password")

class ArtShopUserRegisterForm(UserCreationForm):
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

    class Meta:
        model = ArtShopUser
        fields = ("username", "first_name", "password1", "password2", "email", "age", "gender", "avatar")

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
        fields = ("username", "first_name", "email", "age", "gender", "avatar")