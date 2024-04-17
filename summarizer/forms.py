from django import forms

class DocumentForm(forms.Form):
    document_type = forms.ChoiceField(choices=[('pdf', 'PDF'), ('youtube', 'YouTube Video')])
    document = forms.FileField(label='Upload Document', required=False)
    youtube_url = forms.CharField(label='YouTube URL', required=False)
