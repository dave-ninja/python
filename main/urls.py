from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^signup/$', views.signup, name='signup'),
    path('activate/<uid>/<token>/', views.activate, name='activate'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='main/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', views.pagelogout, name='user_logout'),
    path('contacts/', views.contacts, name='contacts'),
    path('add_parcel/', views.add_parcel, name='add_parcel'),
    path('track_result', views.track_result, name='track_result'),
    path('stores/', views.stores, name='stores')

    # path('login/', views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]