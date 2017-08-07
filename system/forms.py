from django import forms

class ParanuaraForm(forms.Form):
	'''
	This form class contains text input field. This form is 
	for user to submit argument data.
	'''

	args = forms.CharField(widget=forms.Textarea,label="Given argument")
