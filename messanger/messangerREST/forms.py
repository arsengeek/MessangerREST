from django import forms
from .models import Message, UserMessanger, Room, User

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']

class UserMessangerUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150, 
        required=False,
        label="New Username",
        widget=forms.TextInput(attrs={'placeholder': 'Enter new username'})  
        )
    
    image = forms.ImageField(
        required=False, 
        label="Profile Picture", 
        widget=forms.ClearableFileInput(attrs={'class': 'custom-class'})
        
    )

    class Meta:
        model = UserMessanger
        fields = ['image']  

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username


    def save(self, commit=True):
        user = User.objects.get(pk=self.instance.name.id)
        user.username = self.cleaned_data['username']
        
        if commit:
            user.save()
            user_messanger = super().save(commit=False)
            user_messanger.name = user
            if commit:
                user_messanger.save()
        return user_messanger

class RoomUpdateForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150, 
        required=False,
        label="New Name",
        widget=forms.TextInput(attrs={'placeholder': 'Enter new room name'})  
    )

    class Meta:
        model = Room
        fields = ['name']  

    def __init__(self, *args, **kwargs):
        room = kwargs.pop('room', None)  
        super().__init__(*args, **kwargs)
        if room:
            self.fields['name'].initial = room.name

    def save(self, commit=True):
        room = super().save(commit=False)
        room.name = self.cleaned_data['name']
        
        if commit:
            room.save()
        
        return room

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