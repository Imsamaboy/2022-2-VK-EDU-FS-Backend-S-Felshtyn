import json

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.db.models import Q

import logging

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
    logger.info("Getting users from db...")
    body = json.loads(request.body)
    user_entities = []
    for user in body.get("users"):
        user_entity = get_object_or_404(User, username=user)
        if user_entity not in user_entities:
            user_entities.append(user_entity)
    if len(user_entities) == 1:
        return JsonResponse({"created": False, "message": "Trying to create chat with yourself"}, status=400)
    chat = Chats(chat_name=body.get("name"),
                 chat_description=body.get("description"))
    chat.save()
    for user_entity in user_entities:
        chat.users.add(user_entity)
    logger.info("Chat was created...")
    return JsonResponse({
        "created": True,
        "new_chat_id": chat.id
    }, status=201)


@require_GET
def get_chat(request, chat_id) -> JsonResponse:
    """
    :param chat_id: chat id
    :param request: request to get chat object by id
    :return: JsonResponse
    """
    logger.info(f"Trying to get chat with id: {chat_id}")
    chat = get_object_or_404(Chats, id=chat_id)
    users = list(chat.users.all().values()) if chat else []
    logger.info(f"Successfully got chat with id: {chat_id}")
    return JsonResponse({
        "chat": {
            "name": chat.chat_name,
            "description": chat.chat_description
        },
        "users": [
            {
                "id": user.get("id"),
                "username": user.get("username"),
                "description": user.get("description")
            }
            for user in users if users
        ]},
        status=200)


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
    chat.delete()
    logger.info(f"Successfully deleted chat with id: {chat_id}")
    return JsonResponse({
        "deleted": True
    }, status=200)


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
    message_text = message_dto.get("message")
    chat = get_object_or_404(Chats, id=chat_id)
    user = get_object_or_404(User, id=sender_id)
    logger.info(f"Trying to create new message: {message_text}")
    message = Message(chat=chat, sender=user, message=message_text)
    logger.info(f"Successfully created new message: {message_text}")
    message.save()
    return JsonResponse({
        "message": f"Successfully created new message: {message_text}"
    }, status=200)


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
    message.delete()
    logger.info(f"Successfully deleted message with id: {message_id}")
    return JsonResponse({
        "deleted": True
    }, status=200)


@require_GET
def get_message(request, message_id) -> JsonResponse:
    """
    getting message by id
    :param request:
    :param message_id: message id
    :return: JsonResponse
    """
    logger.info(f"Trying to get message with id: {message_id}")
    message = get_object_or_404(Message, id=message_id)
    logger.info(f"Successfully got message with id: {message_id}")
    return JsonResponse({
        "message": {
            "id": message.id,
            "chat_id": message.chat.id,
            "username": message.sender.username,
            "chat_name": message.chat.chat_name,
            "content": message.message,
            "send_time": message.send_time
        }
    }, status=200)


@require_GET
def get_user_chats(request, user_id) -> JsonResponse:
    """
    getting all chats where user is consisting
    :param request:
    :param user_id: user id
    :return: JsonResponse
    """
    user = get_object_or_404(User, id=user_id)
    chats = list(Chats.objects.filter(Q(first_user_id=user.id) | Q(second_user_id=user.id)).values())
    return JsonResponse({
        "chats": chats
    }, status=200)


@require_GET
def get_messages_by_chat_and_user_id(request) -> JsonResponse:
    """
    getting all messages by {user_id} in chat with {chat_id}
    :param request:
    :return: JsonResponse
    """
    dto = json.loads(request.body)
    chat_id = dto.get("chatId")
    user_id = dto.get("userId")
    chat = get_object_or_404(Chats, id=chat_id)
    user = get_object_or_404(User, id=user_id)
    messages = list(Message.objects.filter(Q(chat_id=chat.id) & Q(sender=user.id)))
    if messages:
        messages_text = [message.message for message in messages]
        return JsonResponse({
            "messages": messages_text
        }, status=200)
    else:
        return JsonResponse({
            "message": "No messages"
        }, status=200)


@require_http_methods(['PUT'])
@csrf_exempt
def update_notification_status_in_chat(request, chat_id) -> JsonResponse:
    """
    Updates notification status
    :param chat_id: chat id
    :param request:
    :return: JsonResponse
    """
    status = json.loads(request.body).get("status")
    chat = get_object_or_404(Chats, id=chat_id)
    last_status = chat.mute_notifications
    chat.mute_notifications = status
    chat.save()
    return JsonResponse({
        "message": f"Status was updated from {last_status} to {status}"
    }, status=200)
