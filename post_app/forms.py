from django import forms

from .models import PostApp

class PostAppCreateForm(forms.ModelForm):
    class Meta:
        model = PostApp
        fields = ('title','content','image1','image2','image3','map_addrs')
        widgets = {
            'content': forms.Textarea(
                attrs={'rows': 10, 'cols': 30, 'placeholder': 'ここに入力'}
            ),
        }

class PostSearchForm(forms.Form):
    
    serach_word = forms.fields.CharField(required=False, max_length=25, label='検索ワード')
    posted_name = forms.fields.ChoiceField(required=False,widget=forms.Select(), label='投稿者')
 