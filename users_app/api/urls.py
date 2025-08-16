from django.urls import path
from users_app.api import views


urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='registration'),
    path('activate/<uidb64>/<token>/',
         views.ActivateAccountView.as_view(), name='activate_account'),
    path('login/', views.CookieTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('logout/', views.CookieTokenBlacklistView.as_view(), name='token_blacklist'),
    path('token/refresh/', views.CookieTokenRefreshView.as_view(),
         name='token_refresh'),
    path('password_reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password_confirm/<uidb64>/<token>/',
         views.PasswordConfirmView.as_view(), name='password_confirm')
]
