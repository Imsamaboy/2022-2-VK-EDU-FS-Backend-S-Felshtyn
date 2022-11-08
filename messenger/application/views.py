from typing import Union

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template import loader

import logging

from django.views.decorators.http import require_http_methods
from rest_framework.response import Response

logger = logging.getLogger('debug')


@require_http_methods(["GET"])
def get_homepage(request) -> Union[JsonResponse, HttpResponse]:
    """
    :param request:
    :return:
    """
    logger.debug("Calling get chat lists method...")
    # template = loader.get_template('messenger/templates/homepage.html')
    return render(request, 'homepage.html')
