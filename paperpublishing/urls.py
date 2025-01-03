"""
URL configuration for paperpublishing project.

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
from publications import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('/',views.index,name="index"),
    path('add/',views.add_paper,name="add_paper"),
    path('',views.papers,name='papers'),
    path('papers/',views.papers,name='papers'),
    path('paper-detail/<int:id>/', views.paper_detail, name='paper-detail'),  # URL for the paper details page
    path('login/',views.login,name="login"),
    path('request_access/',views.request_access,name="request_access"),
    # path('get_all_papers/',views.get_papers,name="get_papers"),
    
]

# to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)