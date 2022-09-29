from django.forms import ModelForm
from todolist.models import Task

class CreateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']