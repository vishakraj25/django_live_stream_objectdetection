from django import forms
import os
'''
class ClassForm(forms.Form):
	with open(os.path.join(os.getcwd(), "cv", "coco_names.txt"), 'r') as f:
		classes = [w.strip() for w in f.readlines()]
	classes1 = []
	for i in range(len(classes)):
		classes1.append((str(classes[i]), str(classes[i])))
	print('classes in forms', classes1, [c[0] for c in classes1])
	video_location = forms.CharField()
	classes_field = forms.MultipleChoiceField(choices = classes1,
												#widget=forms.CheckboxSelectMultiple, 
												initial=['person', 'laptop'],#[c[0] for c in classes1],
												)
'''
	
class DeleteForm(forms.Form):
	delete_field = forms.IntegerField(help_text = "Enter number days")


class ClassForm(forms.Form):
	with open(os.path.join(os.getcwd(), "cv", "coco_names.txt"), 'r') as f:
		classes = [w.strip() for w in f.readlines()]
	classes1 = []
	for i in range(len(classes)):
		classes1.append((str(classes[i]), str(classes[i])))
	#print('classes in forms', classes1)
	video_location = forms.CharField()
	classes_field = forms.MultipleChoiceField(choices = classes1,
												#initial=[c[0] for c in classes1],
												)
	def __init__(self, request, *args, **kwargs):
		#session_icons = kwargs.pop('session_icons')
		print('session_icons', request.session['classes_field'])
		super(ClassForm, self).__init__(*args, **kwargs)
		self.fields['classes_field'].initial = request.session['classes_field']
                