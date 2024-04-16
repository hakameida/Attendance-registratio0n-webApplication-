from django.forms import ModelForm
from .models import Session,message,Profile
from django.contrib.auth.models import User
from django import forms

class sessionForm(ModelForm):
   class Meta :
      model=Session
      fields='__all__'


class messageForm(ModelForm):
   class Meta:
      model=message
      fields=['subject','body']
   def __init__(self,*args,**kwargs):
      super(messageForm,self).__init__(*args,**kwargs)

      for name,feild in self.fields.items():
         feild.widget.attrs.update({'class':'input'})


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['super', 'firstname', 'secondname', 'image']

