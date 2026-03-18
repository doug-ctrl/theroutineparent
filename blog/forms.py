from django import forms


class CommentForm(forms.Form):
    name = forms.CharField(
        max_length=80,
        widget=forms.TextInput(attrs={
            "placeholder": "Your name",
            "class": "comment-input",
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Your email (not published)",
            "class": "comment-input",
        })
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Write your comment...",
            "class": "comment-textarea",
            "rows": 4,
        })
    )