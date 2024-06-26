from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.contrib.auth.models import Group,User
from django.forms.widgets import FileInput
from django.db.models import Q
from .models import *
from custom.models import *
from tempus_dominus.widgets import TimePicker

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField()

class UploadFileForm(forms.Form):
    file = forms.FileField()

class DateInput(forms.DateInput):
	input_type = 'date'

class MemberForm(forms.ModelForm):
	data_moris = forms.DateField(label='Data Moris', widget=DateInput())
	end_date = forms.DateField(label='Data Remata', widget=DateInput())
	class Meta:
		model = Member
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('nu_id', css_class='form-group col-md-3 mb-0'),
				Column('naran', css_class='form-group col-md-6 mb-0'),
				Column('sexo', css_class='form-group col-md-3 mb-0'),
			),
			Row(
				Column('naturalidade', css_class='form-group col-md-3 mb-0'),
				Column('data_moris', css_class='form-group col-md-6 mb-0'),
				Column('join_date', css_class='form-group col-md-3 mb-0'),
			),
			Row(
				Column('end_date', css_class='form-group col-md-3 mb-0'),
				Column('enderesu', css_class='form-group col-md-6 mb-0'),
				Column('municipio', css_class='form-group col-md-3 mb-0'),
			),
			Row(
				Column('status', css_class='form-group col-md-3 mb-0'),
				Column('phone', css_class='form-group col-md-6 mb-0'),
				Column('email', css_class='form-group col-md-3 mb-0'),
			),
			
			Row(
				Column('fotografia', css_class='form-group col-md-6 mb-0'),
                Column('documentos', css_class='form-group col-md-6 mb-0'),

            ),
			HTML(""" <div class="text-left mt-4"> <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Update"><span class="btn-label"><i class='fa fa-save'></i></span> Save</button>"""),
			HTML("""  <button class="btn btn-sm btn-labeled btn-secondary" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel</button></div>""")
		)

class GymClassForm(forms.ModelForm):
    start_time = forms.TimeField(widget=TimePicker(
        options={
            'useCurrent': True,
            'collapse': False,
            'icons': {
                'time': 'fa fa-clock',
                'up': 'fa fa-chevron-up',
                'down': 'fa fa-chevron-down',
                'previous': 'fa fa-chevron-left',
                'next': 'fa fa-chevron-right'
            }
        }
    ))
    end_time = forms.TimeField(widget=TimePicker(
        options={
            'useCurrent': True,
            'collapse': False,
            'icons': {
                'time': 'fa fa-clock',
                'up': 'fa fa-chevron-up',
                'down': 'fa fa-chevron-down',
                'previous': 'fa fa-chevron-left',
                'next': 'fa fa-chevron-right'
            }
        }
    ))

    class Meta:
        model = GymClass
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-3 mb-0'),
                Column('description', css_class='form-group col-md-6 mb-0'),
                Column('start_time', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('end_time', css_class='form-group col-md-3 mb-0'),
                Column('days_of_week', css_class='form-group col-md-6 mb-0'),
                Column('payment_per_month', css_class='form-group col-md-3 mb-0'),
            ),
            HTML("""
                <div class="text-left mt-4">
                    <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Update">
                        <span class="btn-label"><i class='fa fa-save'></i></span> Save
                    </button>
                    <button class="btn btn-sm btn-labeled btn-secondary" type="button" onclick="self.history.back()">
                        <span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel
                    </button>
                </div>
            """)
        )

class EnrollmentForm(forms.ModelForm):
	class Meta:
		model = Enrollment
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('member', css_class='form-group col-md-3 mb-0'),
				Column('gym_class', css_class='form-group col-md-6 mb-0'),
				Column('enrollment_date', css_class='form-group col-md-3 mb-0'),
            ),
			HTML(""" <div class="text-left mt-4"> <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Update"><span class="btn-label"><i class='fa fa-save'></i></span> Save</button>"""),
			HTML("""  <button class="btn btn-sm btn-labeled btn-secondary" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel</button></div>""")
		)

