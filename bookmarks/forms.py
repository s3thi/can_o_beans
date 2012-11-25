from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from bookmarks.models import Bookmark


class BookmarkForm(forms.ModelForm):
	class Meta:
		model = Bookmark
		widgets = {
			'title': forms.TextInput()
		}
		exclude = ('hostname',)

	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_class = 'cob-form'
		self.helper.form_method = 'post'
		self.helper.form_action = 'bookmark_create'
		
		self.helper.add_input(Submit('submit', 'Submit'))
		super(BookmarkForm, self).__init__(*args, **kwargs)
