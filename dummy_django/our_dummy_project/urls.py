from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from our_dummy_project import views
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

app_name = 'our_dummy_project'


urlpatterns = [

    # Start of user pages
    path('', views.index, name="Index"),
    path('index/', views.IndexView.as_view(), name="Index"),
    path('logout/', views.microsoft_logout, name="Logout"),
    path('microsoft_authentication/', include('microsoft_authentication.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)