"""
URL configuration for ai_influencer_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from . import views

# Custom error handlers
handler404 = 'ai_influencer_backend.views.custom_404'
handler500 = 'ai_influencer_backend.views.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include([
        path('health/', views.health_check, name='health_check'),
        path('info/', views.api_info, name='api_info'),
        # TODO: Add app-specific API URLs
        # path('auth/', include('users.urls')),
        # path('generations/', include('ai_generation.urls')),
        # path('payments/', include('payments.urls')),
    ])),
    
    # Health check for load balancers
    path('health/', views.health_check, name='health_check_root'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
