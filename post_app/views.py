from django.shortcuts import render, redirect
from .models import PostApp  # 追加
from django.contrib.auth.decorators import login_required

#クラスビューに変更したので追加
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import PostAppCreateForm
from django.contrib import messages

from django.contrib.messages.views import SuccessMessageMixin

from django.db.models import Q

# Create your views here.
from .forms import PostAppCreateForm,PostSearchForm

#from accounts.views import OnlyYouMixin

#クラスビューに変更したので追加
class PostListView(generic.ListView):
    model=PostApp
    template_name = "post_app/post_list.html"

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        post_l = PostApp.objects.all()

        l = []
        for post in post_l:
            l.append(str(post.created_by))

        l = set(l)
        choice = [('1','すべて')]
        choice = choice + [(str(i),s) for i,s in enumerate(l,len(choice)+1)]

        #GET内に保存されているデータでPostSearchFormを作成することで、入力された内容を保持できる
        form = PostSearchForm(self.request.GET)
            
        form.fields['posted_name'].choices = choice
        #GETのデータから検索投稿者名と検索ワードを取得
        q_name = self.request.GET.get('posted_name')
        q_word = self.request.GET.get('serach_word')
        
        if q_word or q_name and q_name != '1':
            q = Q()
            if q_word:
                q_word_l = q_word.split()
                for w in q_word_l:
                    q &= (Q(title__icontains=w)|Q(content__icontains=w))
            if q_name and q_name != '1':
                d_choice = dict(choice)
                q_name = d_choice[q_name]
                q &= Q(created_by__username__exact = q_name)
            
            object_list = PostApp.objects.filter(q)
        else:
            object_list = PostApp.objects.all()

        context.update({'post_list': object_list, 'form':form})
        return context


 #   paginate_by = 5

#他のモデルからのデータを設定する場合など、ここでcontextをアップデートする。
#テンプレートに渡すデータを設定
#    def get_context_data(self, **kwargs):
#        context = super(PostListView, self).get_context_data(**kwargs)
#        post_l = PostApp.objects.all()
#        context.update({'post_list': post_l})
#        return context

#クラスビューに変更したので追加
class PostCreateView(LoginRequiredMixin, generic.FormView):
    model = PostApp
    template_name = "post_app/post_create.html"
    form_class = PostAppCreateForm
#    fields = ['content']
    success_url = reverse_lazy('post_app:post_list')

    def form_valid(self, form):
        #save()はformに結びつけられた新たなモデルのインスタンスを返す
        #https://djangoproject.jp/doc/ja/1.0/topics/forms/modelforms.html
        post_f = form.save(commit=False)
        post_f.created_by = self.request.user
        post_f.save()
        #多対多のデータはここで保存する
        form.save_m2m()
        return super().form_valid(form)

class PostDetailView(generic.DetailView):
    model = PostApp
    template_name = 'post_app/post_detail.html'

class PostUpdateView(generic.UpdateView):
    model = PostApp
    template_name = 'post_app/post_update.html'
    form_class = PostAppCreateForm
    success_message='投稿を更新しました。'

    def get_success_url(self):
        return reverse_lazy('post_app:post_detail', kwargs={'pk':self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '投稿を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '投稿の更新に失敗しました。')
        return super().form_invalid(form)

class PostDeleteView(generic.DeleteView):
    model = PostApp
    template_name = 'post_app/post_delete.html'

    def get_success_url(self):
        return reverse_lazy('accounts:user_profile', kwargs={'pk':self.object.created_by.pk})

    def delete(self,request,*args,**kwargs):
        messages.success(self.request, '日記を削除しました。')
        return super().delete(request,*args,**kwargs)
