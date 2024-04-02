from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.Form):
    nick = forms.CharField(min_length=3, max_length=30, required=True)
    content = forms.CharField(min_length=10, max_length=1000, required=True, widget=forms.Textarea)
