from typing import Union

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

import logging

from django.views.decorators.http import require_http_methods

logger = logging.getLogger('debug')


@require_http_methods(["GET"])
def home(request) -> Union[JsonResponse, HttpResponse]:
    """
    :param request:
    :return:
    """
    logger.debug("Calling get chat lists method...")
    return render(request, 'homepage.html')
