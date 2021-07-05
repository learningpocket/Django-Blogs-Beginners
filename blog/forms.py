from django import forms
from blog.models import Contact


class ContactForm(forms.ModelForm):
    
    class Meta:
        model = Contact
        fields = ("name","email", "message")

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'message': forms.Textarea(attrs={'class':'form-control', 'cols':30, 'rows':10}),   
        }
