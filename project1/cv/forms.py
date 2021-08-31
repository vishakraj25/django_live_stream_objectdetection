from django import forms
import os
	
class DeleteForm(forms.Form):
	delete_field = forms.IntegerField(help_text = "Enter number days")


class ClassForm(forms.Form):
	with open(os.path.join(os.getcwd(), "cv", "coco_names.txt"), 'r') as f:
		classes = [w.strip() for w in f.readlines()]
	classes1 = []
	for i in range(len(classes)):
		classes1.append((str(classes[i]), str(classes[i])))
	video_location = forms.CharField()
	classes_field = forms.MultipleChoiceField(choices = classes1,
		#initial=[c[0] for c in classes1],
		)
	
	def __init__(self, request, *args, **kwargs):
		try:
		    print('session', request.session['classes_field'])
		    super(ClassForm, self).__init__(*args, **kwargs)
		    self.fields['classes_field'].initial = request.session['classes_field']
		except Exception as e:
		    super(ClassForm, self).__init__(*args, **kwargs)
		    self.fields['classes_field'].initial = ['person']
