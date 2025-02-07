from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from .models import ChatGroup, GroupMessage, User
from .forms import ChatmessageCreateForm, NewGroupForm, ChatRoomEditForm

@login_required
def chat_view(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    
    # Assurer que l'utilisateur est membre du chat
    if request.user not in chat_group.members.all():
        if chat_group.is_private:
            raise Http404("Vous n'avez pas accès à ce chat.")
        chat_group.members.add(request.user)

    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()
    
    other_user = None
    if chat_group.is_private:
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break

    # Gestion de l'envoi des messages avec HTMX
    if request.method == "POST" and request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user  # ✅ Vérification que l'auteur est bien assigné
            message.group = chat_group
            message.save()
            return render(request, 'AM/partials/chat_message_p.html', {"message": message})

    context = {
        'chat_messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'chatroom_name': chatroom_name,
        'chat_group': chat_group
    }
    return render(request, 'AM/chat.html', context)

@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')

    other_user = get_object_or_404(User, username=username)
    chatroom = ChatGroup.objects.filter(is_private=True, members=request.user).filter(members=other_user).first()

    if not chatroom:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)
        
    return redirect('chatroom', chatroom.group_name)

@login_required
def create_groupchat(request):
    form = NewGroupForm()

    if request.method == 'POST':
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect('chatroom', new_groupchat.group_name)

    return render(request, 'AM/create_groupchat.html', {"form": form})

@login_required
def chatroom_edit_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    
    if request.user != chat_group.admin:
        raise Http404("Vous n'avez pas la permission d'éditer ce chat.")

    form = ChatRoomEditForm(instance=chat_group)
    
    if request.method == 'POST':
        form = ChatRoomEditForm(request.POST, instance=chat_group)
        if form.is_valid():
            form.save()
            remove_members = request.POST.getlist('remove_members')
            User.objects.filter(id__in=remove_members).update(chat_groups=None)
            return redirect('chatroom', chatroom_name)

    return render(request, 'AM/chatroom_edit.html', {"form": form, "chat_group": chat_group})

@login_required
def chatroom_delete_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    
    if request.user != chat_group.admin:
        raise Http404("Vous n'avez pas la permission de supprimer ce chat.")

    if request.method == "POST":
        chat_group.delete()
        messages.success(request, "Le chat a été supprimé.")
        return redirect('home')

    return render(request, 'AM/chatroom_delete.html', {'chat_group': chat_group})

@login_required
def chatroom_leave_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)

    if request.user in chat_group.members.all():
        if request.method == "POST":
            chat_group.members.remove(request.user)
            messages.success(request, "Vous avez quitté le chat.")
            return redirect('home')
    else:
        raise Http404("Vous n'êtes pas membre de ce chat.")

    return render(request, 'AM/chatroom_leave.html', {"chat_group": chat_group})

@login_required
def chat_file_upload(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)

    if request.htmx and request.FILES:
        file = request.FILES['file']
        message = GroupMessage.objects.create(
            file=file,
            author=request.user,
            group=chat_group,
        )
        channel_layer = get_channel_layer()
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        async_to_sync(channel_layer.group_send)(chatroom_name, event)

        return JsonResponse({"status": "Fichier envoyé", "message_id": message.id})

    return HttpResponse(status=400)
