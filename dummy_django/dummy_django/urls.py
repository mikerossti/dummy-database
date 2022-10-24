from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from our_dummy_project import views

urlpatterns = [
    path('', include('our_dummy_project.urls', namespace='our_dummy_project')), 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
