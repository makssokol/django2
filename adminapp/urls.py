from django.urls import path
import adminapp.views as adminapp
from .apps import AdminappConfig

app_name = AdminappConfig.name

urlpatterns = [
    path("", adminapp.admin_main, name="admin_main"),
    path("users/create/", adminapp.ArtShopUserCreateView.as_view(), 
         name="user_create"),
    path("users/read/", adminapp.UsersListView.as_view(), name="users"),
    path("users/update/<int:pk>/", adminapp.ArtShopUserUpdateView.as_view(), 
         name="user_update"),
    path("users/delete/<int:pk>/", adminapp.ArtShopUserDeleteView.as_view(), 
         name="user_delete"),
    path("artcategory/create/", adminapp.ArtCategoryCreateView.as_view(), 
         name="category_create"),
    path("artcategory/read/", adminapp.categories, name="categories"),
    path("artcategory/update/<int:pk>/", adminapp.ArtCategoryUpdateView.as_view(), 
         name="category_update"),
    path("artcategory/delete/<int:pk>/", adminapp.ArtCategoryDeleteView.as_view(), 
         name="artcategory_delete"),
    path("products/create/category/<int:pk>/", adminapp.product_create, 
         name="product_create"),
    path("products/read/category/<int:pk>/", adminapp.products, 
         name="products"),
    path("products/read/<int:pk>", adminapp.ArtObjectDetailView.as_view(), 
         name="product_read"),
    path("products/update/<int:pk>/", adminapp.product_update, 
         name="product_update"),
    path("products/delete/<int:pk>/", adminapp.ArtObjectDeleteView.as_view(), 
         name="product_delete"),
    # path("orders/<int:pk>", adminapp.OrdersListView.as_view(), name="orders"),
]
