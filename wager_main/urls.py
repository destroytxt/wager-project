from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.edit import CreateView
from django.urls import include, path, reverse_lazy

from bets.views import edit_profile, profile_view
from pages.views import homepage, logout_view
from users.forms import CustomUserCreationForm

urlpatterns = [
    path('', homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('bets/', include('bets.urls', namespace='bets')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/', include('django.contrib.auth.urls')),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/', profile_view, name='profile'),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=CustomUserCreationForm,
            success_url=reverse_lazy('homepage')
        ),
        name='registration'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler403 = 'pages.views.csrf_failure'
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
