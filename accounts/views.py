

import django.http
import accounts.models
import accounts.forms
from django.shortcuts import render,redirect,resolve_url,get_object_or_404
import uuid
from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.db import IntegrityError
from django.contrib.auth import get_user_model
#from .models import User
#from post_app.models import PostApp  # 追加

#クラスビューに変更したので追加
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import UserProfileUpdateForm
from django.contrib import messages

#ログインしている自分だけ
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        # 今ログインしてるユーザーのpkと、そのユーザー情報ページのpkが同じか、又はスーパーユーザーなら許可
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser

#プロファイルを表示するクラスビュー
class UserProfileView(LoginRequiredMixin, generic.DetailView):
    #ユーザーモデル
    model = get_user_model()
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    template_name = "accounts/user_profile.html"
#    context_object_name = 'user_profile' 

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['followee'] = self.object.followers.filter(followees=self.request.user)
#        context['follower'] = self.object.followers.filter(followers=self.request.user)

#        return context

@login_required
def users_follow(request, pk):
    """フォロー機能"""
    login_user = request.user
    user = get_user_model().objects.get(pk=pk)
    followers = login_user.followers.all()
    #既にフォローしていれば解除、していなければフォロー
    if user in followers:
        login_user.followers.remove(user)
        user.followees.remove(login_user)
        messages.success(request, 'フォローを解除しました')
    else:
        login_user.followers.add(user)
        user.followees.add(login_user)
        messages.success(request, 'フォローしました')

    user.save()
    return redirect('accounts:user_profile', pk=pk)


class FollowListView(LoginRequiredMixin, generic.ListView):
    model=get_user_model()
    template_name = "accounts/follow_list.html"

    def get_context_data(self, **kwargs):
        context = super(FollowListView, self).get_context_data(**kwargs)
        pk=self.kwargs['pk']
        flag = self.kwargs['flag']

        user = get_user_model().objects.get(pk=pk)
        if flag:
            ret_follows = user.followers.all()
        else:
            ret_follows = user.followees.all()

        context.update({'follow':ret_follows, 'flag':flag})

        return context

#    def get_queryset(self):
#        pk=self.kwargs['pk']
#        flag = self.kwargs['flag']
#        user = get_user_model().objects.get(pk=pk)
#        if flag:
#            ret_follows = user.followers.all()
#        else:
#            ret_follows = user.followees.all()
#        return ret_follows

class UserProfileUpdateView(OnlyYouMixin, generic.UpdateView):
    #ユーザーモデル
    model = get_user_model()
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    template_name = "accounts/user_profile_update.html"
    form_class = UserProfileUpdateForm

    def get_success_url(self):
        #return resolve_url('accounts:user_profile', username=self.kwargs['username'])
        return resolve_url('accounts:user_profile', pk=self.kwargs['pk'])
    '''
    def form_valid(self, form):
        messages.success(self.request, 'ユーザー情報を更新しました。')
        return super().form_valid()

    def form_invalid(self, form):
        messages.error(self.request, 'ユーザー情報の更新に失敗しました。')
        return super().form_invalid()
    '''
    
def user_profile(request, username):
    context = {
        'User':get_user_model().objects.get(username=username),
    }
    return render(request,'accounts/user_profile.html',context)

def has_digit(text):
    if re.search("\d", text):
        return True
    return False

def has_alphabet(text):
    if re.search("[a-zA-Z]", text):
        return True
    return False

def login_user(request):
    if request.method == 'POST':
        login_form = accounts.forms.LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = get_user_model().objects.get(username=username)
            if user is not None:
                django_login(request, user)
                ret = redirect('post_app:post_create')
                #return ret
        except get_user_model().DoesNotExist:
            #else:
                login_form.add_error(None, "ユーザー名またはパスワードが異なります。")
                ret = render(request, 'registration/login.html', {'login_form': login_form})
        return ret
    else:
        login_form = accounts.forms.LoginForm()
        ret = render(request, 'registration/login.html', {'login_form': login_form})
    return ret
    #アカウントとパスワードが合致したら、その人専用の投稿画面に遷移するs
    #アカウントとパスワードが合致しなかったら、エラーメッセージ付きのログイン画面に遷移する
    
def logout_user(request):
    django_logout(request)
    return render(request, 'registration/logged_out.html', {})

def registation_user(request):
    if request.method == 'POST':
        registration_form = accounts.forms.RegistrationForm(request.POST)
        password = request.POST['password']
        if len(password) < 8:
            registration_form.add_error('password', "文字数が8文字未満です。")
        if not has_digit(password):
            registration_form.add_error('password',"数字が含まれていません")
        if not has_alphabet(password):
            registration_form.add_error('password',"アルファベットが含まれていません")
        if registration_form.has_error('password'):
            return render(request, 'registration/user_create.html', {'registration_form': registration_form})

        try:
            user = get_user_model().objects.create_user(username=request.POST['username'], password=password, email=request.POST['email'])
        except IntegrityError as e:
            registration_form.add_error('username',"すでに登録されているユーザー名またはメールアドレスです")
            return render(request, 'registration/user_create.html', {'registration_form': registration_form})
        return redirect('accounts:user_registration_complete')
        #return render(request, 'registration/user_create_done.html', {'registration_form': registration_form})
    else:
        registration_form = accounts.forms.RegistrationForm()
    return render(request, 'registration/user_create.html',{'registration_form': registration_form})

def registration_complete(request):
    return render(request, 'registration/user_create_done.html')