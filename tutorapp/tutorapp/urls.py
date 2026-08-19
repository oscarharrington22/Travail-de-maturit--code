"""
URL configuration for tutorapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView

import authentication.views
import app.views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', LoginView.as_view(
            template_name='authentication/login.html',
            redirect_authenticated_user=True), name='login'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('signup_prof/', authentication.views.signup_prof, name='signup_prof'),
    path('logout/', authentication.views.logout_user, name='logout'),

    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/changepw.html',
        success_url='/change-password-done/'
        ), name='change_password'),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/change_pw_done.html'
        ), name='change_password_done'),

    path('home/', app.views.home, name='home'),
    path('mon-compte/', app.views.mon_compte, name='mon_compte'),
    path('modifier-mon-compte/', app.views.modifier_compte, name='modifier_compte'),
    path('modifier-mon-compte-prof/', app.views.modifier_compte_prof, name='modifier_compte_prof'),
    path('profile-photo-upload', authentication.views.upload_profile_photo,name='upload_profile_photo'),

    path('recherche/', app.views.recherche, name='recherche'),
    path('profil/<int:user_id>/', app.views.profil, name='profil'),
    path('demande-lecon/<int:user_id>/', app.views.demande_lecon, name = 'demande_lecon'),

    path('mes-disponibilites/', authentication.views.mes_disponibilites, name = 'mes_disponibilites'),
    path('nouvelle-disponibilite/', authentication.views.nouvelle_disponibilite, name = 'nouvelle_disponibilite'),
    path('supprimer-disponibilite/<int:id>/', authentication.views.supprimer_disponibilite, name='supprimer_disponibilite'),

    path('mes-demandes-envoyees/', app.views.mes_demandes_envoyees, name = 'mes_demandes_envoyees'),
    path('mes-demandes-recues/', app.views.mes_demandes_recues, name = 'mes_demandes_recues'),
    path('repondre-demande/<int:demande_id>/', app.views.repondre_demande, name = 'repondre_demande'),
    path('supprimer-demande/<int:demande_id>/',app.views.supprimer_demande,name='supprimer_demande'),

    ]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
