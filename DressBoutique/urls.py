"""
URL configuration for DressBoutique project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from Maria import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.SignUpView.as_view(),name='signup'),
    path('login/',views.SignInView.as_view(),name="login"),
    path('index/',views.IndexView.as_view(),name='index'),
    path('logout/',views.SignOutView.as_view(),name="signout"),
    path('dresses/<int:pk>/',views.DressDetailView.as_view(),name="dress-detail"),
    path('dresses/cart/add/',views.AddCartView.as_view(),name='add-cart'),
    path('cart/summary/',views.CartSummaryView.as_view(),name="cart-summary"),
    path('cart/<int:pk>/remove/',views.CartItemDeleteView.as_view(),name="cartitem-delete"),
    path('placeorder/',views.PlaceOrderView.as_view(),name="place-order"),
    path('order/success/',views.PaymentSuccessView.as_view(),name="order-success"),
    path('order/summary/',views.OrderSummaryView.as_view(),name='order-summary'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
