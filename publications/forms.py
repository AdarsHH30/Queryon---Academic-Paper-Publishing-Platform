from django import forms

class RequestAccessForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    institution = forms.CharField(max_length=200)
    role = forms.ChoiceField(choices=[('faculty', 'Faculty'), ('researcher', 'Researcher'), ('student', 'Student'), ('other', 'Other')])
    purpose = forms.CharField(widget=forms.Textarea)
