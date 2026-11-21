
from django.contrib import admin
from django.urls import path, include

from core.views import CustomLoginView

urlpatterns = [

    # Django Admin
    path('admin/', admin.site.urls),

    # Custom Login
    path(
        'accounts/login/',
        CustomLoginView.as_view(),
        name='login'
    ),

    # Authentication URLs
    path('accounts/', include('django.contrib.auth.urls')),

    # Core App URLs
    path('', include('core.urls')),

]
