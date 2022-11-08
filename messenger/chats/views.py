import json

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.db.models import Q

import logging
from datetime import datetime

from chats.models import Chats, Message
from users.models import User

logger = logging.getLogger('debug')


@require_POST
@csrf_exempt
def create_chat(request) -> JsonResponse:
    """
    :param request: request to create new chat with 2 users
    :return: JsonResponse: created / not created
    """
    logger.info("Calling create chat method...")
    print(request.body)
    print(request.POST)
    print(request.POST.get("Hey"))
    first_user = request.POST.get("firstUser")
    second_user = request.POST.get("secondUser")
    if first_user != second_user:
        logger.info("Getting users from db...")
        first_user_entity = get_object_or_404(User, username=first_user)
        second_user_entity = get_object_or_404(User, username=second_user)
        if not list(Chats.objects.filter(first_user=first_user_entity, second_user=second_user_entity)):
            chat = Chats(first_user=first_user_entity, second_user=second_user_entity, created_date=datetime.now(),
                         mute_notifications=True)
            chat.save()
            logger.info(f"New chat was created with id: {chat.id}")
        else:
            return JsonResponse({"created": False, "message": "chat already exist"}, status=400)
        return JsonResponse({"created": True, "new_chat_id": chat.id}, status=201)
    else:
        logger.error("Trying to chat with myself...")
        return JsonResponse({
            "created": False,
            "info": "Trying to chat with myself..."
        }, status=400)


@require_GET
def get_chat(request, chat_id) -> JsonResponse:
    """
    :param chat_id: chat id
    :param request: request to get chat object by id
    :return: JsonResponse
    """
    logger.info(f"Trying to get chat with id: {chat_id}")
    chat = list(Chats.objects.filter(id=chat_id).values())
    for key, value in chat[0].items():
        if isinstance(value, datetime):
            chat[0][key] = value.strftime("%d/%m/%Y, %H:%M:%S")
    logger.info(f"Successfully got chat with id: {chat_id}")
    return JsonResponse({"chatInfo": chat}, status=200)


@require_http_methods(['DELETE'])
@csrf_exempt
def delete_chat(request, chat_id) -> JsonResponse:
    """
    delete chat by id
    :param request:
    :param chat_id: specified chat id
    :return: JsonResponse
    """
    logger.info(f"Trying to get chat with id: {chat_id}")
    chat = get_object_or_404(Chats, id=chat_id)
    if chat:
        Chats(id=chat_id).delete()
        logger.info(f"Successfully deleted chat with id: {chat_id}")
        return JsonResponse({"deleted": True}, status=200)
    logger.info(f"Chat with id doesn't exist: {chat_id}")


@require_POST
@csrf_exempt
def create_message(request) -> JsonResponse:
    """
    create new message by user
    :param request:
    :return: JsonResponse
    """
    message_dto = json.loads(request.body)
    chat_id = message_dto.get("chatId")
    sender_id = message_dto.get("senderId")
    recipient_id = message_dto.get("recipientId")
    message_text = message_dto.get("message")
    chat = get_object_or_404(Chats, id=chat_id)
    logger.info(f"Trying to create new message: {message_text}")
    if message_text and sender_id in (chat.first_user.id, chat.second_user.id) \
            and recipient_id in (chat.first_user.id, chat.second_user.id):
        first_user = get_object_or_404(User, id=sender_id)
        second_user = get_object_or_404(User, id=recipient_id)
        message = Message(chat=chat,
                          sender=first_user,
                          recipient=second_user,
                          message=message_text,
                          send_time=datetime.now())
        message.save()
        logger.info(f"Successfully created new message: {message.id}")
        return JsonResponse({"created": True}, status=201)
    logger.error(f"Check your dto body!")
    return JsonResponse({"created": False}, status=400)


@require_http_methods(['DELETE'])
def delete_message(request, message_id) -> JsonResponse:
    """
    delete message by id
    :param request:
    :param message_id:
    :return: JsonResponse
    """
    logger.info(f"Trying to get message with id: {message_id}")
    message = get_object_or_404(Message, id=message_id)
    if message:
        Message(id=message_id).delete()
        logger.info(f"Successfully deleted message with id: {message_id}")
        return JsonResponse({"deleted": True}, status=200)
    logger.info(f"Message with id doesn't exist: {message_id}")
    return JsonResponse({"deleted": False}, status=400)


@require_GET
def get_message(request, message_id) -> JsonResponse:
    """
    getting message by id
    :param request:
    :param message_id: message id
    :return: JsonResponse
    """
    logger.info(f"Trying to get message with id: {message_id}")
    message_entity = get_object_or_404(Message, id=message_id)
    messages = list(Message.objects.filter(id=message_entity.id).values())
    for key, value in messages[0].items():
        if isinstance(value, datetime):
            messages[0][key] = value.strftime("%d/%m/%Y, %H:%M:%S")
    logger.info(f"Successfully got message with id: {message_id}")
    return JsonResponse({"message": messages}, status=200)


@require_GET
def get_user_chats(request, user_id) -> JsonResponse:
    """
    getting all chats where user is consisting
    :param request:
    :param user_id: user id
    :return: JsonResponse
    """
    user = get_object_or_404(User, id=user_id)
    if user:
        chats = list(Chats.objects.filter(Q(first_user_id=user.id) | Q(second_user_id=user.id)).values())
        return JsonResponse({"chats": chats}, status=200)
    return JsonResponse({"message": "Chats didn't found"}, status=400)


@require_GET
def get_messages_by_chat_and_user_id(request) -> JsonResponse:
    """
    getting all messages by {user_id} in chat with {chat_id}
    :param request:
    :return: JsonResponse
    """
    dto = json.loads(request.body)
    print(dto)
    chat_id = dto.get("chatId")
    user_id = dto.get("userId")
    chat = get_object_or_404(Chats, id=chat_id)
    user = get_object_or_404(User, id=user_id)
    messages = list(Message.objects.filter(Q(chat_id=chat.id) & Q(sender=user.id)))
    if messages:
        messages_text = [message.message for message in messages]
        return JsonResponse({"messages": messages_text}, status=200)
    else:
        return JsonResponse({"message": "No messages"}, status=200)


@require_http_methods(['PUT'])
@csrf_exempt
def update_notification_status_in_chat(request, chat_id) -> JsonResponse:
    """
    Updates notification status
    :param chat_id: chat id
    :param request:
    :return: JsonResponse
    """
    # request.PUT
    dto = json.loads(request.body)
    status = dto.get("status")
    chat = get_object_or_404(Chats, id=chat_id)
    last_status = chat.mute_notifications
    chat.mute_notifications = status
    chat.save()
    return JsonResponse({"message": f"status was updated from {last_status} to {status}"})
