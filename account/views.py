from django.core.signing import BadSignature
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView,\
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin

from .models import BoardUser
from .forms import ChangeUserInfoForm, RegisterUserForm
from .utilities import signer


class PassConfirmView(PasswordResetConfirmView):
    template_name = 'account/confirm_reset.html'
    success_url = reverse_lazy('login')


class PassResetDone(PasswordResetDoneView):
    model = BoardUser
    template_name = 'account/reset_done.html'


class PassResetView(PasswordResetView):
    template_name = 'account/reset_pass.html'
    subject_template_name = 'email/reset_sub.txt'
    email_template_name = 'email/reset_email.txt'
    success_url = reverse_lazy('reset_done')


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = BoardUser
    template_name = 'account/delete_user.html'
    success_url = reverse_lazy('main')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'account/bad_signature.html')
    user = get_object_or_404(BoardUser, username=username)
    if user.is_activated:
        template = 'account/activated_user.html'
    else:
        template = 'account/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class RegisteredView(TemplateView):
    template_name = 'account/registered.html'


class RegisterUserView(CreateView):
    model = BoardUser
    template_name = 'account/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('registered')


class UserPassChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'account/pass_change.html'
    success_url = reverse_lazy('profile')
    success_message = 'Пароль пользователя изменен'


class UserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = BoardUser
    form_class = ChangeUserInfoForm
    template_name = 'account/user_info.html'
    success_url = reverse_lazy('profile')
    success_message = 'Данные изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


@login_required
def profile(request):
    return render(request, 'account/profile.html')


class BoardLoginView(LoginView):
    template_name = 'account/login.html'


class BoardLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'account/logout.html'
