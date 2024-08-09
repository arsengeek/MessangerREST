from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import Profil, MessageCreateView, ChatsList, RoomCreate, RoomDetailView, RoomList, ProfilView

urlpatterns = [
    path('myprofil/<int:pk>', Profil.as_view(), name='profil'),
    path('<int:pk>', MessageCreateView.as_view(), name='create_message'),
    path('home/', ChatsList.as_view(), name='chats'),
    path('creategroup', RoomCreate.as_view(), name='creategroup'),
    path('group/<int:pk>', RoomDetailView.as_view(), name='groupdetail'),
    path('groups/', RoomList.as_view(), name='groups'),
    path('profil', ProfilView.as_view(), name='profilView'),
    # path('user/<int:pk>', MessageCreateUserView.as_view(), name='create_message_user'),
    # path('add_user_to_room/', AddUserToRoomView.as_view(), name='add_user_to_room'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)