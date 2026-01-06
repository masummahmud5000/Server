from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.home.as_view()),
    path('token/', views.loginView.as_view(), name='My_Token_Obtain'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
