from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls.web')),
    path('treinamentos/', include('apps.trainings.urls.web')),
    path('turmas/', include('apps.classesapp.urls.web')),
    path('recursos/', include('apps.resourcesapp.urls.web')),
    path('matriculas/', include('apps.enrollments.urls.web')),
]
