from django.forms import ModelForm, widgets
from .models import Question
from django import forms

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title','tag', 'dayNo', 'difficulty', 'company', 'source', 
                  'code', 'time_cmplx', 'space_cmplx']

        widgets = {
            'difficulty': forms.RadioSelect(),
        }