from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from polls.forms import LoginForm
from polls.views import RegisterView, LoginView, profile
from django.conf import settings
from django.conf.urls.static import static
import polls.views as views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('polls.urls')),
    path('login/', LoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html',authentication_form=LoginForm), name='login'),
    path('profile/', profile, name='profile'),
    path('registration/', RegisterView.as_view(), name='register'),
    path('user_delete/', views.profileDelete, name='delete'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
