from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/', views.home.as_view()),
    path('token/', views.loginView.as_view(), name='My_Token_Obtain'),
    path('profile/', views.Profile.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('deposite/', views.deposite.as_view()),
    path('withdraw/', views.withdraw.as_view()),
    path('sendMoney/', views.sendMoney.as_view()),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
