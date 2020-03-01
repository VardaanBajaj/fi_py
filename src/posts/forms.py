from django import forms

from .models import Post

class PostModelForm(forms.ModelForm):
    # new_title=forms.CharField()
    content=forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': "Share your insights!", "class": "form-control"}))
    class Meta:
        model=Post
        fields = [
            # "user",
            "content",
        ]

    # def clean_content(self, *args, **kwargs): #form validation for content
    #     content=self.cleaned_content.get('content')
    #     if content == "":
    #          raise forms.ValidationError("Cannot be empty")
    #     return content
