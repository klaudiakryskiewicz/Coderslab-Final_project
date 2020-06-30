"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from gift_wishes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='main'),
    path('add-wish/', views.AddWishView.as_view(), name='add-wish'),
    path('wish-list/<int:id>/', views.WishListView.as_view(), name='wish-list'),
    path('present-list/<int:id>/', views.PresentListView.as_view(), name='present-list'),
    path('family/<int:id>/', views.FamilyMembersView.as_view(), name='family'),
    path('add-member/', views.AddMemberView.as_view(), name='add-member'),
    path('add-family/', views.AddFamilyView.as_view(), name='add-family'),
# path('wish-details/', views.WishDetailsViews.as_view(), name='wish-details'), OPCJONALNIE
    path("accounts/", include('django.contrib.auth.urls')),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/signup/family/<int:id>/', views.SignUpFamilyView.as_view(), name='signup'),
    path('invite/', views.InviteView.as_view(), name='invite'),
    path('book-wish/', views.BookWish.as_view(), name='book-wish'),
    path('buy-present/', views.BuyPresent.as_view(), name='buy-present'),
]


