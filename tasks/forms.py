from django import forms
from django.forms import widgets

from tasks.models import Quiz, Question

class StyledFormMixin:
    # default_classes="border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"
    default_classes = (
        "w-full px-4 py-2 rounded-lg shadow-sm border border-gray-300 rounded-lg "
        "focus:outline-none focus:ring-2 focus:ring-rose-500 "
        "focus:border-rose-500"
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
        
    def apply_styled_widgets(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget,(widgets.TextInput,widgets.EmailInput,widgets.PasswordInput,)):
                field.widget.attrs.update({
                    "class": self.default_classes,
                    "placeholder": f"Enter {field.label}",
                })
            elif isinstance(field.widget,forms.CharField):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter{field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter{field.label.lower()}"
                })
            elif isinstance(field.widget,widgets.TimeInput):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter{field.label.lower()}"
                })
            
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class':"border-2 border-gray-300 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"
                    
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':"space-y-2"
                    
                })
            else: 
                field.widget.attrs.update({
                    'class':self.default_classes
                    
                })







class QuizForm(StyledFormMixin,forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "w-full p-2 border rounded"
            }
        )
    )

    class Meta:
        model = Quiz
        fields = [
            "title",
            "description",
            "start_time",
            "duration",
            "total_marks",
            "is_active"
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
            "description": forms.Textarea(attrs={"class": "w-full p-2 border rounded"}),
            "duration": forms.NumberInput(attrs={"class": "w-full p-2 border rounded"}),
            "total_marks": forms.NumberInput(attrs={"class": "w-full p-2 border rounded"}),
        }

# class QuizForm(StyledFormMixin,forms.ModelForm):
#     class Meta:
#         model = Quiz
#         fields = ['title', 'description', 'duration', 'total_marks', 'is_active']


class QuestionForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'text',
            'option_a',
            'option_b',
            'option_c',
            'option_d',
            'correct_answer',
            'marks'
        ]
