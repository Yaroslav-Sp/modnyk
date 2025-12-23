"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts.views import (InfoAfterRegistration, UserActivationView,
                            UserLogin, UserLogout, UserRegistration)

urlpatterns = (
    [
        path("", include("shop.urls")),
        path("login/", UserLogin.as_view(), name="login"),
        path("logout/", UserLogout.as_view(), name="logout"),
        path("registration/", UserRegistration.as_view(), name="registration"),
        path("registration_info/", InfoAfterRegistration.as_view(), name="registration_info"),
        path("activate/<str:uuid64>/<str:token>/", UserActivationView.as_view(), name="activate_user"),
        path("oauth/", include("social_django.urls", namespace="social")),
        path("api-auth/", include("rest_framework.urls")),
        path("api/", include("api.urls")),
        path("admin/", admin.site.urls),
        path("products/", include("products.urls")),
        path("cart/", include("cart.urls")),
        path("customer/", include("accounts.urls")),
        path("orders/", include("orders.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + debug_toolbar_urls()
)
