from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='home'),
    path('animals/', views.animals, name='animals'),
    path('accounts/', include('users.urls')),
    path('notes/', include('notes.urls')),
    path('courses/', include('courses.urls')),
    path('quiz/', include('quiz.urls')),
    path('energy/', include('energy_app.urls')),
    path('carbon/', include('carbon_calculator.urls')),
    path('bookings/', include('bookings.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
