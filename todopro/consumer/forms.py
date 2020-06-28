from django.forms import ModelForm
from .models import Consumerprofile

class ProfileForm(ModelForm):
    class Meta:
        model =  Consumerprofile
        fields = '__all__'
