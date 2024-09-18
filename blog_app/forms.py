from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    # The four lines down are just for set placeholder for fields.
    # name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    # email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    # title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    # body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'message'}))

    class Meta:
        model = Message
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Subject'}),
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'body': forms.Textarea(attrs={'placeholder': 'message'}),
        }
