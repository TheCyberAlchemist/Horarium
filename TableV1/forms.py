from django import forms
from .models import event_class
DAYS = [
    ('Monday','Monday'),
    ('Tuesday','Tuesday'),
    ('Wednesday','Wednesday'),
    ('Thursday','Thursday'),
    ('Friday','Friday'),
    ('Saturday','Saturday'),
    ('Sunday','Sunday'),
]
# Option on the right and value on the left
class selectdays(forms.Form):
    Days = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=DAYS,
    )

class add_event(forms.ModelForm):
    class Meta: 
        model = event_class
        exclude = ['owner']
        fields = "__all__"