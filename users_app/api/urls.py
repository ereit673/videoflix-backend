from django.urls import path
from users_app.api import views


urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='registration'),
    path('activate/<uidb64>/<token>/',
         views.ActivateAccountView.as_view(), name='activate_account'),
    path('login/', views.CookieTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', views.CookieTokenRefreshView.as_view(),
         name='token_refresh')
]
