from django.forms import ModelForm
from .models import List
from django.utils.translation import gettext_lazy as _

class ListForm(ModelForm):
    class Meta:
        model = List
        fields = ['name', 'description']
        labels = {
            'name': _('List Name'),
            'description': _('Description')
        }
