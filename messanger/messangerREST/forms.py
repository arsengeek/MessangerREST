from django import forms
from .models import Message, UserMessanger, Room, User

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        
class ProfilUpdate(forms.ModelForm):
    class Meta:
        model = UserMessanger
        fields = ['name', 'image']
        
class CreateGroup(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name']
        
# class AddUserForm(forms.Form):
#     user = forms.ModelChoiceField(queryset=UserMessanger.objects.all())
#     room = forms.ModelChoiceField(queryset=Room.objects.all())
    

#     def save(self):
#         room = self.cleaned_data['room']
#         user = self.cleaned_data['user']
#         room.add_member(user)