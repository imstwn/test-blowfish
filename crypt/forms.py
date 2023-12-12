from django import forms
from django.forms import FileInput
from .models import BlowfishModel


class BlowfishForm(forms.ModelForm):
	key = forms.CharField(
		label='Key',
		max_length=100,
		widget=forms.PasswordInput(
			attrs={
				'class':'form-control',
				'placeholder':'Key'
				}
			)
		)
	class Meta:
		model = BlowfishModel
		fields = ['file',]
		widgets = {
			'file':FileInput(attrs={
				'class':'form-control',
				})
		}
