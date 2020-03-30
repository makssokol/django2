from django import forms
from authapp.forms import ArtShopUserEditForm
from authapp.models import ArtShopUser
from mainapp.models import ArtCategory, ArtObject

class ArtShopUserAdminEditForm(ArtShopUserEditForm):
    class Meta:
        model = ArtShopUser
        fields = "__all__"


class ArtCategoryEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""

    class Meta:
        model = ArtCategory
        fields = "__all__"


class ArtObjectEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArtObjectEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""

    class Meta:
        model = ArtObject
        fields = "__all__"