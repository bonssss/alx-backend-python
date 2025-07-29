from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, get_user_model
from .models import Message

User = get_user_model()

@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')

@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user, parent_message__isnull=True).select_related('sender', 'receiver').prefetch_related('replies').order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'messages': messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        content = request.POST['content']
        receiver_id = request.POST['receiver']
        parent_id = request.POST.get('parent_id')
        msg = Message(sender=request.user, receiver_id=receiver_id, content=content)
        if parent_id:
            msg.parent_message_id = parent_id
        msg.save()
        return redirect('inbox')
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'messaging/send_message.html', {'users': users})
