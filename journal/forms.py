from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from journal.models import JournalEntry

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        widgets = {
            'title': forms.TextInput()
        }
        exclude = ('content_processed',)

    def __init__(self, action, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'cob-form'
        self.helper.form_method = 'post'
        self.helper.form_action = action

        self.helper.add_input(Submit('submit', 'Submit'))
        super(JournalEntryForm, self).__init__(*args, **kwargs)
