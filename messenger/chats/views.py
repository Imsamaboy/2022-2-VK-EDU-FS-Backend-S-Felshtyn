from typing import Union

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from rest_framework.response import Response

import logging
import random

logger = logging.getLogger('debug')

chats = [
    {
        'id': 1,
        'name': 'Ivan B',
        'message': 'вообще то в python есть...'
    },
    {
        'id': 2,
        'name': 'Patrick Bateman',
        'message': 'Oh... Impressive'
    },
    {
        'id': 3,
        'name': 'Vladislav L',
        'message': 'Когда скинешь фотки с дз?'
    },
]

messages = [
    "OMG",
    "Hi!",
    "Как дела?",
    "ok!"
]


@require_GET
def get_chats_list(request) -> Union[JsonResponse, Response]:
    """
    :param request:
    :return:
    """
    logger.debug("Calling get chat lists method...")
    return JsonResponse({"chats": chats})


@require_GET
def get_chat_page(request, id) -> Union[JsonResponse, Response]:
    """
    :param id:
    :param request:
    :return:
    """
    logger.debug(f"Calling get chat page {id} method...")
    return render(request, 'chat.html', {"id": id})


@require_POST
@csrf_exempt
def create_chat(request) -> Union[JsonResponse, Response]:
    """
    :param request:
    :return:
    """
    logger.debug("Calling create chat method...")
    next_id = len(chats) + 1
    chats.append({
        "id": f"{next_id}",
        "name": f"Person{next_id}",
        "message": random.choice(messages)
    })
    return JsonResponse({"Response": f"New chat {next_id} created!"})
