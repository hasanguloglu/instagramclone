from django import forms
from .models import Post, Comment, CustomUser

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['tags', 'caption', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Yorumunuzu buraya girin...'}),
        }
        labels = {
            'text': '',
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image']

    