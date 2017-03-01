# -*- coding: utf-8 -*-
# Created by apple on 2017/2/6.

from sanic import Blueprint
from ..utils import JsonResult
from ..exceptions import BadRequest
from sanic.exceptions import NotFound, ServerError, FileNotFound, RequestTimeout, PayloadTooLarge, InvalidUsage

exception_blueprint = Blueprint('exception')


@exception_blueprint.exception(NotFound)
def not_fond(request, exception):
    return JsonResult.not_ok('not found').response_json()


@exception_blueprint.exception(ServerError)
def server_error(request, exception):
    return JsonResult.not_ok('server error').response_json()


@exception_blueprint.exception(FileNotFound)
def file_not_found(request, exception):
    return JsonResult.not_ok('file not found').response_json()


@exception_blueprint.exception(RequestTimeout)
def request_timeout(request, exception):
    return JsonResult.not_ok('request timeout').response_json()


@exception_blueprint.exception(InvalidUsage)
def request_invalid_usage(request, exception):
    return JsonResult.not_ok('invalid usage').response_json()


@exception_blueprint.exception(PayloadTooLarge)
def request_payload_tool_large(request, exception):
    return JsonResult.not_ok('payload tool large').response_json()


@exception_blueprint.exception(BadRequest)
def request_timeout(request, exception):
    return JsonResult.not_ok(exception.args[0] or 'bad request').response_json()


@exception_blueprint.exception(KeyError)
def request_timeout(request, exception):
    return JsonResult.not_ok('bad request').response_json()
