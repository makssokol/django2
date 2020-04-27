from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db import connection
from django.dispatch import receiver
from django.db.models.signals import pre_save

from adminapp.forms import ArtShopUserAdminEditForm, ArtCategoryEditForm, ArtObjectEditForm
from authapp.forms import ArtShopUserRegisterForm
from authapp.models import ArtShopUser
from mainapp.models import ArtObject, ArtCategory
from django.db.models import F

# Create your views here.

@user_passes_test(lambda u: u.is_superuser)
def admin_main(request):
    response = redirect("myadmin:users")
    return response

class UsersListView(LoginRequiredMixin, ListView):
    model = ArtShopUser
    template_name = "adminapp/users.html"

class ArtShopUserCreateView(LoginRequiredMixin, CreateView):
    model = ArtShopUser
    template_name = "adminapp/user_update.html"
    success_url = reverse_lazy("myadmin:users")
    fields = "__all__"

class ArtShopUserUpdateView(LoginRequiredMixin, UpdateView):
    model = ArtShopUser
    template_name = "adminapp/user_update.html"
    success_url = reverse_lazy("myadmin:users")
    fields = "__all__"

class ArtShopUserDeleteView(LoginRequiredMixin, DeleteView):
    model = ArtCategory
    template_name = "adminapp/user_delete.html"
    success_url = reverse_lazy("myadmin:users")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda x: x.is_superuser)
def categories(request):
    object_list = ArtCategory.objects.all().order_by('-is_active', 'name')
    context = {
        'title': 'adminsite/categories',
        'object_list': object_list
    }
    return render(request, 'adminapp/artcategory_list.html', context)

class ArtCategoryCreateView(LoginRequiredMixin, CreateView):
    model = ArtCategory
    template_name = "adminapp/category_update.html"
    success_url = reverse_lazy("myadmin:categories")
    fields = "__all__"

class ArtCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = ArtCategory
    template_name = "adminapp/category_update.html"
    success_url = reverse_lazy("myadmin:categories")
    form_class = ArtCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "categories/edit"
        return context
    
    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.artobject_set.update(
                    price=F('price') * (1 - discount / 100)
                )
                # db_profile_by_type(self.__class__, 'UPDATE', connection.queries)
        return super().form_valid(form)
        

class ArtCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = ArtCategory
    success_url = reverse_lazy("myadmin:categories")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = "adminsite/product"
    category = get_object_or_404(ArtCategory, pk=pk)
    products_list = ArtObject.objects.filter(category__pk=pk).order_by("name")
    content = {
        "title": title,
        "category": category,
        "objects": products_list,
        "media_url": settings.MEDIA_URL,
    }
    return render(request, "adminapp/products.html", content)

@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = "art object / creation"
    category = get_object_or_404(ArtCategory, pk=pk)

    if request.method == "POST":
        product_form = ArtObjectEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse("myadmin:products", args=[pk]))
    else:
        product_form = ArtObjectEditForm(initial={"category": category})

    content = {
        "title": title,
        "update_form": product_form,
        "category": category,
        "media_url": settings.MEDIA_URL,
    }
    return render(request, "adminapp/product_update.html", content)

@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = "art object / edit"
    edit_product = get_object_or_404(ArtObject, pk=pk)

    if request.method == "POST":
        edit_form = ArtObjectEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse("myadmin:product_update", args=[edit_product.pk]))
    else:
        edit_form = ArtObjectEditForm(instance=edit_product)

    content = {
        "title": title,
        "update_form": edit_form,
        "category": edit_product.category,
        "media_url": settings.MEDIA_URL,
    }
    return render(request, "adminapp/product_update.html", content)


class ArtObjectDetailView(LoginRequiredMixin, DetailView):
    model = ArtObject
    template_name = "adminapp/artobject_detail.html"



class ArtObjectDeleteView(LoginRequiredMixin, DeleteView):
    model = ArtObject
    template_name = "adminapp/product_delete.html"
    success_url = reverse_lazy("myadmin:products")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x : type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]

@receiver(pre_save, sender=ArtCategory)
def product_is_active_update_artcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.artobject_set.update(is_active=True)
        else:
            instance.artobject_set.update(is_active=False)
        
        # db_profile_by_type(sender, 'UPDATE', connection.queries)
