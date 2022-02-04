from django.urls import path

from .views import profile, BoardLoginView, BoardLogoutView, UserInfoView, UserPassChangeView, \
    RegisterUserView, RegisteredView, user_activate, \
    DeleteUserView, PassResetView, PassResetDone, PassConfirmView


urlpatterns = [
    path('login/', BoardLoginView.as_view(), name='login'),
    path('logout/', BoardLogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/delete/', DeleteUserView.as_view(), name='delete'),
    path('change/', UserInfoView.as_view(), name='info_change'),
    path('password/change', UserPassChangeView.as_view(), name='pass_change'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('register/success/', RegisteredView.as_view(), name='registered'),
    path('register/activate/<str:sign>/', user_activate, name='activate_register'),
    path('password-reset/', PassResetView.as_view(), name='pass_reset'),
    path('password-reset/done/', PassResetDone.as_view(), name='reset_done'),
    path('reset/<uidb64>/<token>/', PassConfirmView.as_view(), name='pass_confirm')


]
