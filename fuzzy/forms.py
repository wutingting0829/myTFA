from django import forms


class FuzzyExtractorForm(forms.Form):
    old_password = forms.CharField(
        label='field 1', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3 col-sm-12', 'placeholder': 'Old Password', 'id': 'form-oldpass'}))


class FuzzyExtractorReproduceForm(forms.Form):
    helper = forms.CharField(
        label='field 2', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3 col-sm-12', 'placeholder': 'Old Password', 'id': 'form-oldpass1111'}))
