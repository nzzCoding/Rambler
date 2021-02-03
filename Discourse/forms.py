from django import forms

class RamblerSubForm(forms.Form):
    name = forms.CharField(max_length=30)
    description = forms.CharField()


class RamblerPostForm(forms.Form):
    title = forms.CharField(max_length=120)
    content = forms.CharField()


class RamblerCommentForm(forms.Form):
    content = forms.CharField()
