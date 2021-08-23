import re
from rest_framework import renderers
import json


def DictionaryHandler(data, status_code, types):

    response = dict()
    if 'ErrorDetail' in str(data):
        error_dict = data.__reduce__()[1][0]
        print(error_dict)

        errors = list()

        for key in error_dict:
            red = error_dict[key][0].__reduce__()
            error = {
                'field': str(key),
                'object': str(1),
                'detail_code': str(red[2]['code']),
                'detail': str(error_dict[key][0])

            }
            errors.append(error)
        response = json.dumps({
            'errors': errors,
            'status_code': status_code
        })
    else:

        relationships = dict()
        data_dict = data.__reduce__()[1][0]
        print(type(data_dict))
        for key in data_dict:

            if "fk_" in str(key):
                temp = data.pop(key)
                relationships[key] = temp

        response["data"] = data
        response['data']["relationships"] = relationships
        response["type"] = types
        response['status_code'] = status_code
        response = json.dumps(response)

    return response


def ListHandler(data, status_code, types):

    response = dict()
    # print(data.__reduce__()[1][0][0])
    # print(type(data.__reduce__()[1][0][0]))

    objects = data.__reduce__()[1][0]
    # print("Objects:", objects)
    final_response = dict()

    final_response["status_code"] = status_code

    if 'ErrorDetail' in str(data):

        all_errors = list()
        for i in range(len(objects)):
            error_dict = objects[i]
            # print(error_dict)
            for key2 in error_dict:
                # print("Error_Dict:", error_dict[key2])
                # print("Key2", key2)
                red = error_dict[key2][0].__reduce__()
                error = {
                    'field': str(key2),
                    'object': str(i+1),
                    'detail_code': str(red[2]['code']),
                    'detail': str(error_dict[key2][0])

                }
                all_errors.append(error)
            # all_errors.append(errors)
            response = json.dumps({
                'errors': all_errors,
                'status_code': status_code
            })
    else:

        all_objects = list()

        for key in objects:
            object_dict = key.copy()
            relationships = dict()

            print(type(object_dict))
            for field in object_dict:

                if "fk_" in str(field):
                    temp = key.pop(field)
                    relationships[field] = temp
            key["relationships"] = relationships

            all_objects.append(key)

        response["data"] = all_objects
        response["type"] = types
        response['status_code'] = status_code
        response = json.dumps(response)

    return response


class CustomRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        if renderer_context is not None:
            string = str(renderer_context['view']).split(".")
            types = string[2].split("ViewSet")[0]
            status_code = renderer_context['response'].status_code
            print(renderer_context['response'].status_code)

        print(type(data))
        print(data)

        if "Dict" in str(type(data)):
            return DictionaryHandler(data, status_code, types)

        else:
            return ListHandler(data, status_code, types)
