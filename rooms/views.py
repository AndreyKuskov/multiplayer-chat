from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView, LoginView
from django.utils.safestring import mark_safe
import typing as tp
import json
from . import models

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name: str = 'chat/registration.html'
    success_url = '/'
    
class Logout(LogoutView):
    next_page = '/'

class HomeView(LoginView):
    template_name: str = 'chat/index.html'
    next_page = '/'

    def get_context_data(self, **kwargs: tp.Any) -> tp.Dict[str, tp.Any]:
        context = super().get_context_data(**kwargs)
        if (self.request.user.is_authenticated):
            context.update({
                'chats': models.Chat.objects.all()
            })
        return context

class RoomView(TemplateView):
    template_name: str = 'chat/chat_room.html'

    def get_context_data(self, **kwargs: tp.Any) -> tp.Dict[str, tp.Any]:
        context = super().get_context_data(**kwargs)
        room_name = self.request.get_full_path().split('/')[1]
        context.update({
                'chats': models.Chat.objects.all(),
                'messages': models.Messages.objects.filter(chat__name=room_name).order_by('-id')[:3],
                'room_name': room_name,
                'room_name_json': mark_safe(json.dumps(room_name))
        })
        return context
    