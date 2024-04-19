from django import forms


class Question_and_answer(forms.Form):

    pytanie = forms.CharField(widget=forms.Textarea(attrs={"rows": "5", "cols": "50"},))




