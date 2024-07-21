from django.shortcuts import render
from django.views.generic import UpdateView,CreateView, ListView, FormView
from .models import UserMessanger, Message, Room
from .forms import MessageForm, ProfilUpdate, CreateGroup
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import request
from django.shortcuts import render, get_object_or_404


class Profil(LoginRequiredMixin, UpdateView):
    permission_required = ('ModalsDateBase.change_post')
    form_class = ProfilUpdate
    model = UserMessanger
    template_name = 'profil.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.room = UserMessanger.objects.get(pk=self.kwargs['pk'])
        context['pk'] = self.kwargs['pk']
        return context
    
    def __str__(self):
        return self.name
    
class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'messanger.html'
    success_url = reverse_lazy('')  

    def form_valid(self, form):
        form.instance.sender = self.request.user
        self.room = Room.objects.get(pk=self.kwargs['pk'])
        form.instance.room = self.room
        self.object = form.save()
        print(f"Message saved: {self.object.text}") 
        return JsonResponse({'success': True, 'message': 'Message created successfully!'})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.room = Room.objects.get(pk=self.kwargs['pk'])
        context['pk'] = self.kwargs['pk']
        context['room'] = Room.objects.get(pk=self.kwargs['pk'])
        messages = Message.objects.filter(room=self.room).order_by('time')
        context['messages'] = messages
        return context
    
class ChatsList(ListView):
    model = UserMessanger
    ordering = ''
    template_name = 'chats.html'
    context_object_name = 'chats'
    paginate_by=15
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return self.form.qs

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context
    
    
class MessageList(ListView):
    model = Message
    ordering = ''
    template_name = 'messanger.html'
    context_object_name = 'messages'
    paginate_by=1000

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Room, UserMessanger
from .forms import CreateGroup  # Замените на вашу форму

class RoomCreate(LoginRequiredMixin, CreateView):
    model = Room
    form_class = CreateGroup
    template_name = 'createGroup.html'
    success_url = reverse_lazy('success_url')  # Замените на ваш URL

    def form_valid(self, form):
        response = super().form_valid(form)
        user_messanger = UserMessanger.objects.get(name_id=self.request.user.id)
        room = form.instance
        room.admin.set([user_messanger])
        room.save()
        room.members.add(user_messanger) 
        return response

    def get_success_url(self):
        return reverse_lazy('groupdetail', kwargs={'pk': self.object.pk})
    
    # def post(self, request,  **kwargs):
    #     return redirect('groups')
    
class RoomDetailView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'room_detail.html'
    context_object_name = 'messages'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = Room.objects.get(pk=self.kwargs['pk'])
        return context
    
class RoomList(ListView):
    model = Room
    ordering = ''
    template_name = 'groupview.html'
    context_object_name = 'rooms'
    paginate_by=1000
    
    # def get_queryset(self):
    #     user_messanger = UserMessanger.objects.get(name=self.request.user)
    #     return Room.objects.filter(members=user_messanger)
        
# class AddUserToRoomView(LoginRequiredMixin, FormView):
#     template_name = 'add_user_to_room.html'
#     form_class = AddUserForm
#     success_url = reverse_lazy('groups')

#     def form_valid(self, form):
#         return super().form_valid(form)

