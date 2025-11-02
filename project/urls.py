from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls.web')),
    path('treinamentos/', include('apps.trainings.urls.web')),
    path('turmas/', include('apps.classesapp.urls.web')),
    path('recursos/', include('apps.resourcesapp.urls.web')),
    path('matriculas/', include('apps.enrollments.urls.web')),
    path('aluno/', include('apps.accounts.urls.web')),
    path('api/', include('apps.accounts.urls.api')),
    path('login/',  auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),

]
