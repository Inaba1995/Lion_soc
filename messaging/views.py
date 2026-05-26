from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Conversation, Message
from notifications.models import Notification


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(participants=request.user)
    return render(request, "messaging/inbox.html", {"conversations": conversations})


@login_required
def conversation_view(request, pk):
    conv = get_object_or_404(Conversation, pk=pk, participants=request.user)
    conv.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    return render(request, "messaging/conversation.html", {"conversation": conv})


@login_required
def send_message(request):
    if request.method == "POST":
        recipient_id = request.POST.get("recipient_id")
        text = request.POST.get("text", "").strip()
        if not text or not recipient_id:
            messages.error(request, "Message and recipient required.")
            return redirect("inbox")

        from django.contrib.auth import get_user_model
        User = get_user_model()
        recipient = get_object_or_404(User, pk=recipient_id)

        conv = Conversation.objects.filter(participants=request.user).filter(participants=recipient).first()
        if not conv:
            conv = Conversation.objects.create()
            conv.participants.add(request.user, recipient)

        Message.objects.create(conversation=conv, sender=request.user, text=text)

        Notification.objects.create(
            recipient=recipient, sender=request.user,
            type="message", text=f"New message from {request.user.username}",
            link=f"/messages/{conv.pk}/",
        )

        return redirect("conversation", pk=conv.pk)

    from django.contrib.auth import get_user_model
    User = get_user_model()
    users = User.objects.exclude(pk=request.user.pk)
    return render(request, "messaging/new.html", {"users": users})
