import json

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods

import logging

from chats.models import Chats, Message
from users.models import User

logger = logging.getLogger('debug')


# TODO: поменять PUT на PATCH (там где я обновляю данные)
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


@require_http_methods(['PUT'])
@csrf_exempt
def update_chat_name(request, chat_id) -> JsonResponse:
    """
    :param request: request to update chat name
    :param chat_id: chat in which we have to update name
    :return: JsonResponse
    """
    new_name = json.loads(request.body).get("name")
    chat = get_object_or_404(Chats, id=chat_id)
    last_name = chat.chat_name
    chat.chat_name = new_name
    chat.save()
    return JsonResponse({
        "message": f"Chat name was changed from {last_name} to {new_name}"
    }, status=200)


@require_http_methods(['PUT'])
@csrf_exempt
def update_chat_description(request, chat_id) -> JsonResponse:
    """
    :param request: request to update chat description
    :param chat_id: chat in which we have to update description
    :return: JsonResponse
    """
    new_description = json.loads(request.body).get("description")
    chat = get_object_or_404(Chats, id=chat_id)
    last_description = chat.chat_description
    chat.chat_description = new_description
    chat.save()
    return JsonResponse({
        "message": f"Chat name was changed from {last_description} to {new_description}"
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


@require_http_methods(['PUT'])
@csrf_exempt
def add_new_member_in_chat(request, chat_id) -> JsonResponse:
    """
    :param request: request object to add new user
    :param chat_id: chat in which we have to add new user
    :return: JsonResponse
    """
    user_id_to_add = json.loads(request.body).get("id")
    chat = get_object_or_404(Chats, id=chat_id)
    user = get_object_or_404(User, id=user_id_to_add)
    if not Chats.objects.filter(id=chat_id, users__in=[user_id_to_add]).exists():
        # TODO: <- тут должен быть какой-то запрос на .value_list(), поменять проверку
        chat.users.add(user)
        chat.save()
        return JsonResponse({
            "message": f"Successfully added new member with id: {user_id_to_add}"
        }, status=200)
    else:
        return JsonResponse({
            "message": f"User with id: {user_id_to_add} is already in chat!"
        }, status=400)


@require_http_methods(['PUT'])
@csrf_exempt
def delete_member_from_chat(request, chat_id) -> JsonResponse:
    """
    :param request: request object to delete user
    :param chat_id: chat in which we have to delete user
    :return: JsonResponse
    """
    user_id_to_delete = json.loads(request.body).get("id")
    chat = get_object_or_404(Chats, id=chat_id)
    user = get_object_or_404(User, id=user_id_to_delete)
    if Chats.objects.filter(id=chat_id, users__in=[user_id_to_delete]).exists():
        chat.users.remove(user)
        chat.save()
        return JsonResponse({
            "message": f"Successfully deleted member with id: {user_id_to_delete}"
        }, status=200)
    else:
        return JsonResponse({
            "message": f"User with id: {user_id_to_delete} is not in the chat!"
        }, status=400)


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


"""-> MESSAGES -> """


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


@require_http_methods(['PUT'])
@csrf_exempt
def update_message_content(request, message_id) -> JsonResponse:
    """
    :param message_id: message which content we have to update
    :param request: request to update message content
    :return: JsonResponse
    """
    refactored_message = json.loads(request.body).get("message")
    message = get_object_or_404(Message, id=message_id)
    message_text = message.message
    message.message = refactored_message
    message.save()
    return JsonResponse({
        "message": f"Message content has changed from {message_text} to {refactored_message}"
    }, status=200)


@require_http_methods(['PUT'])
@csrf_exempt
def update_message_status(request, message_id) -> JsonResponse:
    """
    :param message_id: message which status we have to update
    :param request: request to update message status
    :return: JsonResponse
    """
    status = json.loads(request.body).get("status")
    message = get_object_or_404(Message, id=message_id)
    last_status = message.is_read
    message.is_read = status
    message.save()
    return JsonResponse({
        "message": f"Message status has changed from {last_status} to {status}"
    }, status=200)


@require_http_methods(['DELETE'])
def delete_message(request, message_id) -> JsonResponse:
    """
    delete message by id
    :param request: request to delete message by id
    :param message_id: message id which we have to delete
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
def get_chats_list_by_user_id(request, user_id) -> JsonResponse:
    """
    :param user_id:
    :param request:
    :return: JsonResponse
    """
    chats = list(Chats.objects.filter(users__in=[user_id]))
    if chats:
        return JsonResponse({
            "chats": [
                {
                    "id": chat.id,
                    "chat": chat.chat_name,
                    "description": chat.chat_description
                }
                for chat in chats
            ]
        }, status=200)
    else:
        return JsonResponse({
            "message": f"Chats weren't found by user: {user_id}"
        }, status=400)


@require_GET
def get_all_messages_by_chat_id(request, chat_id) -> JsonResponse:
    """
    :param request: request to get all messages by chat id
    :param chat_id: chat which messages we'll check
    :return: JsonResponse
    """
    messages = list(Message.objects.filter(chat=chat_id))
    if messages:
        return JsonResponse({
            "messages": [
                {
                    "id": message.id,
                    "message": message.message,
                    "sender": message.sender.username,
                    "is_read": message.is_read,
                    "time": message.send_time
                }
                for message in messages
            ]
        }, status=200)
    else:
        return JsonResponse({
            "message": f"Messages weren't found. Try to check your chat id: {chat_id}"
        }, status=400)


@require_GET
def get_info_about_user_by_id(request, user_id) -> JsonResponse:
    """
    :param request:
    :param user_id:
    :return:
    """
    user = get_object_or_404(User, id=user_id)
    return JsonResponse({
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "description": user.description,
        "phone_number": user.phone_number
    })
