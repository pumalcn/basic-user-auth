from django.urls import path, include
from django.contrib.auth import views as auth_views
from api.views import register_view, RegisterView, login_view, LoginView, logout_view, verify_email


urlpatterns = [
    path('register/', register_view, name='register'),
    path('cbv/register/', RegisterView.as_view(), name='register_cbv'),
    path('login/', login_view, name='login'),
    path('cbv/login/', LoginView.as_view(), name='login_cbv'),
    path('logout/', logout_view, name='logout'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('verify-email/<uuid:token>', verify_email, name='verify_email'),
    #path('password_reset/', include('django.contrib.auth.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
