"""
URL configuration for personalms project.

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
from django.contrib import admin
from django.urls import path

from django.urls import path
from pms import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('department/<int:department_id>/tasks/', views.department_tasks, name='department_tasks'),
    path('departments/', views.departments_view, name='departments_view'),
    path('metrics/',views.user_metrics_view, name='user_metrics'),
    path('kpimetrics/',views.metrics_view, name='metrics'),
    path('admin/', admin.site.urls),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)