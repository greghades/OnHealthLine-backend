from django.urls import path
from .views import LoginView, ResetPasswordView, SendCodeResetPassword,RegistroView,LogoutView, DeleteView,UpdateUser,ListUsers, ValidationCodeView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('register/', RegistroView.as_view()),
    path('delete/<int:pk>/', DeleteView.as_view()),
    path('update/<int:pk>/',UpdateUser.as_view()),
    path('listUsers/',ListUsers.as_view()),
    path('password/code/',SendCodeResetPassword.as_view()),
    path('password/validate_code/',ValidationCodeView.as_view()),
    path('password/reset/',ResetPasswordView.as_view())
]