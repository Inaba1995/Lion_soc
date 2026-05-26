from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text", "image"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3, "class": "form-control", "placeholder": "What's on your mind?"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.TextInput(attrs={"class": "form-control", "placeholder": "Write a comment..."}),
        }
