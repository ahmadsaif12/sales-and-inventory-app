from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='user-register'),
    path('login/', views.RatelimitedLoginView.as_view(template_name='accounts/login.html'), name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='user-logout'),
    path('profile/', views.profile, name='user-profile'),
    path('profile/update/', views.profile_update, name='user-profile-update'),

    path('staff/', views.ProfileListView.as_view(), name='profile_list'),
    path('staff/create/', views.ProfileCreateView.as_view(), name='profile-create'),
    path('staff/<int:pk>/update/', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('staff/<int:pk>/delete/', views.ProfileDeleteView.as_view(), name='profile-delete'),

    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/update/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),
    path('customers/search/', views.get_customers, name='get_customers'),

    path('vendors/', views.VendorListView.as_view(), name='vendor-list'),
    path('vendors/create/', views.VendorCreateView.as_view(), name='vendor-create'),
    path('vendors/<int:pk>/update/', views.VendorUpdateView.as_view(), name='vendor-update'),
    path('vendors/<int:pk>/delete/', views.VendorDeleteView.as_view(), name='vendor-delete'),
]
