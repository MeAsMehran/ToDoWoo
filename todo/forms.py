# WE CREATED THIS FILE FOR DIFFERENT FORMS: (we created a file and named it forms.py)
# django helps us with different forms a lot

from django.forms import ModelForm
from .models import todo


class ToDoForm(ModelForm):       # we put () to inherit
    class Meta:
        model = todo
        fields = ['title', 'memo', 'important']     # we set the fields which we need from the models.py file to be shown in our form for user to fill them

