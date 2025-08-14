from django.urls import path
from users_app.api import views


urlpatterns = [
    path('login/', views.CookieTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', views.CookieTokenRefreshView.as_view(),
         name='token_refresh'),
    path('register/', views.RegistrationView.as_view(), name='registration')
]
