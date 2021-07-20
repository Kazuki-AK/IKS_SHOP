from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import ( LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView )
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect, resolve_url
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from .forms import ( LoginForm, UserCreateForm, UserUpdateForm, ShopUpdateForm, TimeUpdateForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm, EmailChangeForm )

from .models import ( User, Shop )

# Create your views here.

User = get_user_model()

class Top(generic.TemplateView):

    template_name = 'top.html'

    def get_context_data(self, **kwargs):
        # 継承元のメソッド呼び出し
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:

            shop_id = self.request.user.shop_number

            if Shop.objects.filter( pk = shop_id ).exists():
                context['shop'] = Shop.objects.get( pk = shop_id ).shop_name
            else:
                context['shop'] = '未登録'
        else:
            pass
        return context


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'registration/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'registration/logout.html'


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        # 「ログイン中のユーザーのpkと、そのユーザー情報ページのpkが同じ」or「ログイン中のユーザーがスーパーユーザー」なら許可
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetail(OnlyYouMixin, generic.DetailView):
    model = User
    template_name = 'registration/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:

            shop_id = self.request.user.shop_number

            if Shop.objects.filter( pk = shop_id ).exists():
                context['shop'] = Shop.objects.get( pk = shop_id ).shop_name
            else:
                context['shop'] = '未登録'
        else:
            pass
        return context

class UserUpdate(OnlyYouMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'registration/user_form.html'

    def get_success_url(self):
        return resolve_url('UserLogin:user_detail', pk=self.kwargs['pk'])


class ShopDetail(OnlyYouMixin, generic.DetailView):
    model = Shop
    template_name = 'registration/shop_detail.html'

class ShopUpdate(OnlyYouMixin, generic.UpdateView):
    model = Shop
    form_class = ShopUpdateForm
    template_name = 'registration/shop_form.html'

    def get_success_url(self):
        return resolve_url('UserLogin:shop_detail', pk=self.kwargs['pk'])


class TimeDetail(OnlyYouMixin, generic.DetailView):
    model = Shop
    template_name = 'registration/time_detail.html'

class TimeUpdate(OnlyYouMixin, generic.UpdateView):
    model = Shop
    form_class = TimeUpdateForm
    template_name = 'registration/time_form.html'

    def get_success_url(self):
        return resolve_url('UserLogin:time_detail', pk=self.kwargs['pk'])


class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'registration/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('registration/mail_template/create/subject.txt', context)
        message = render_to_string('registration/mail_template/create/message.txt', context)

        user.email_user(subject, message)
        return redirect('UserLogin:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'registration/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'registration/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()

                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')   #登録後にそのままログインする場合の処理

                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('UserLogin:password_change_done')
    template_name = 'registration/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'registration/password_change_done.html'


class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'registration/mail_template/password_reset/subject.txt'
    email_template_name = 'registration/mail_template/password_reset/message.txt'
    template_name = 'registration/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('UserLogin:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'registration/password_reset_done.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('UserLogin:password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'

class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'registration/password_reset_complete.html'


class EmailChange(LoginRequiredMixin, generic.FormView):
    """メールアドレスの変更"""
    template_name = 'registration/email_change_form.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }

        subject = render_to_string('registration/mail_template/email_change/subject.txt', context)
        message = render_to_string('registration/mail_template/email_change/message.txt', context)
        send_mail(subject, message, None, [new_email])

        return redirect('registration:email_change_done')


class EmailChangeDone(LoginRequiredMixin, generic.TemplateView):
    """メールアドレスの変更メールを送ったよ"""
    template_name = 'registration/email_change_done.html'


class EmailChangeComplete(LoginRequiredMixin, generic.TemplateView):
    """リンクを踏んだ後に呼ばれるメアド変更ビュー"""
    template_name = 'registration/email_change_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            User.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)


class ShopPreView(TemplateView):
    template_name = 'shop/infomation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:

            shop_id = self.request.user.shop_number

            if Shop.objects.filter( pk = shop_id ).exists():
                context['shop'] = Shop.objects.get( pk = shop_id )
            else:
                pass
        else:
            pass
        return context