from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from apps.accounts.urls import web as accounts_web

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',  auth_views.LoginView.as_view(template_name='auth/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('treinamentos/', include('apps.trainings.urls.web')),
    path('turmas/', include('apps.classesapp.urls.web')),  # Admin turmas
    path('recursos/', include('apps.resourcesapp.urls.web')),
    path('matriculas/', include('apps.enrollments.urls.web')),
    path('aluno/', include(accounts_web.aluno_urlpatterns)),  # Aluno turmas e recursos (prefixo /aluno/)
    path('', include('apps.accounts.urls.web')),  # Dashboard e pos-login (sem prefixo)
    path('api/', include('apps.accounts.urls.api')),
]
