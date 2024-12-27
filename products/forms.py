from django import forms
from .models import Review

class OrderForm(forms.Form):
    name = forms.CharField(max_length=100, label="Ваше имя")
    email = forms.EmailField(label="Ваш email")
    address = forms.CharField(widget=forms.Textarea, label="Адрес доставки")


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
