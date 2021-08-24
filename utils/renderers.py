import re
from rest_framework import renderers
import json


def DictionaryErrorHandler(data, status_code, types):

    response = dict()
    # if "ErrorDetail" in str(data):
    error_dict = data.__reduce__()[1][0]
    print(error_dict)

    errors = list()

    for key in error_dict:
        red = error_dict[key][0].__reduce__()
        error = {
            "field": str(key),
            "object": str(1),
            "detail_code": str(red[2]["code"]),
            "detail": str(error_dict[key][0]),
        }
        errors.append(error)
    response = json.dumps({"errors": errors, "status_code": status_code})
    # else:

    #     relationships = dict()
    #     data_dict = data.__reduce__()[1][0]
    #     print(type(data_dict))

    #     for key in data_dict:

    #         if "fk_" in str(key):
    #             temp = data.pop(key)
    #             relationships[key] = temp

    #     response["data"] = data
    #     response["data"]["relationships"] = relationships
    #     response["type"] = types
    #     response["status_code"] = status_code
    #     response = json.dumps(response)

    return response


def ListErrorHandler(data, status_code, types):

    response = dict()
    # print(data.__reduce__()[1][0][0])
    # print(type(data.__reduce__()[1][0][0]))

    objects = data.__reduce__()[1][0]
    # print("Objects:", objects)
    final_response = dict()
    print(objects, "objects")
    final_response["status_code"] = status_code

    # if "ErrorDetail" in str(data):

    all_errors = list()
    for i in range(len(objects)):
        error_dict = objects[i]
        # print(error_dict)
        for key2 in error_dict:
            # print("Error_Dict:", error_dict[key2])
            # print("Key2", key2)
            red = error_dict[key2][0].__reduce__()
            error = {
                "field": str(key2),
                "object": str(i + 1),
                "detail_code": str(red[2]["code"]),
                "detail": str(error_dict[key2][0]),
            }
            all_errors.append(error)
        # all_errors.append(errors)
        response = json.dumps({"errors": all_errors, "status_code": status_code})

    # else:

    #     all_objects = list()

    #     for key in objects:
    #         object_dict = key.copy()
    #         relationships = dict()

    #         print(type(object_dict))
    #         for field in object_dict:

    #             if "fk_" in str(field):
    #                 temp = key.pop(field)
    #                 relationships[field] = temp
    #         key["relationships"] = relationships

    #         all_objects.append(key)

    #     response["data"] = all_objects
    #     response["type"] = types
    #     response["status_code"] = status_code
    #     response = json.dumps(response)

    return response


def AuthenticationThrottleHandler(data, status_code):
    response = dict()
    error_dict = data
    if "ErrorDetail" in str(data):
        errors = list()
        for key in error_dict:
            red = error_dict[key].__reduce__()
            print("Key", key)
            print("red", red)
            error = {
                "field": str(key),
                "object": str(1),
                "detail_code": str(red[2]["code"]),
                "detail": str(error_dict[key]),
            }
            errors.append(error)
        response = json.dumps({"errors": errors, "status_code": status_code})

    return response


def ParseData(data):

    temp_data = data.copy()

    if "Dict" in str(type(data)) or "dict" in str(type(data)):
        return_data = dict()
        relationships = dict()
        data_dict = temp_data.copy()
        data_dict2 = temp_data.copy()
        # .__reduce__()[1][0]

        for key in data_dict:

            key_type = str(type(data[key]))
            print("key type", key, type)
            if (
                "dict" in key_type
                or "list" in key_type
                or "List" in key_type
                or "Dict" in key_type
            ):

                nested_parse = ParseData(data[key])

                if "fk_" in str(key):

                    relationships[key] = nested_parse
                else:
                    return_data[key] = nested_parse

            elif "fk_" in str(key):
                relationships[key] = data_dict2.pop(key)
            else:
                return_data[key] = temp_data.pop(key)

        return_data["relationships"] = relationships

        return return_data

    else:
        print("list data", temp_data)
        return_data = list()
        objects = temp_data.copy()
        # .__reduce__()[1][0]

        for obj in objects:
            object_dict = obj.copy()
            object_dict2 = obj.copy()
            relationships = dict()

            for field in object_dict:

                field_type = str(type(object_dict[field]))
                print(field_type)
                if (
                    "dict" in field_type
                    or "list" in field_type
                    or "List" in field_type
                    or "Dict" in field_type
                ):
                    # print(data[1]["name"])
                    nested_parse = ParseData(object_dict[field])

                    if "fk_" in str(field):

                        object_dict2[field] = nested_parse

                    else:

                        object_dict2[field] = nested_parse
                elif "fk_" in str(field):
                    relationships[field] = object_dict2.pop(field)
                else:
                    object_dict2[field] = object_dict[field]
            object_dict2["relationships"] = relationships

            return_data.append(object_dict2)

        return return_data


# class CustomRenderer(renderers.JSONRenderer):
#     charset = "utf-8"

#     def render(self, data, media_type=None, renderer_context=None):
#         if renderer_context is not None:
#             string = str(renderer_context["view"]).split(".")
#             types = string[2].split("ViewSet")[0]
#             status_code = renderer_context["response"].status_code

#         final_response = dict()
#         final_response["status_code"] = status_code
#         final_response["types"] = types

# if "Dict" in str(type(data)):

#     data = data.__reduce__()[1][0]
#     print(data)
#     print("dict data", type(data))
#     final_response["data"] = dict()

# else:

#     data = data.__reduce__()[1][0]
#     print(data)
#     print("list data", type(data))
#     final_response["data"] = list()


#         # print(data, "received data")
#         # data = data.__reduce__()[1][0]
#         # print(data)


#         final_response["data"] = ParseData(data)

#         return json.dumps(final_response)


class CustomRenderer(renderers.JSONRenderer):
    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):
        if renderer_context is not None:
            string = str(renderer_context["view"]).split(".")
            types = string[2].split("ViewSet")[0]
            status_code = renderer_context["response"].status_code
            print(renderer_context["response"].status_code)

        print(type(data))
        print(data)
        if "dict" in str(type(data)):
            return AuthenticationThrottleHandler(data, status_code)

        if "ErrorDetail" in str(data):
            if "Dict" in str(type(data)):
                return DictionaryErrorHandler(data, status_code, types)
            else:
                return ListErrorHandler(data, status_code, types)

        elif "Message" in str(data):
            final_response = dict()
            final_response["status_code"] = status_code
            final_response["types"] = types
            final_response["errors"] = data
            return json.dumps(final_response)
        else:
            final_response = dict()
            final_response["status_code"] = status_code
            final_response["types"] = types
            data = data.__reduce__()[1][0]
            final_response["data"] = ParseData(data)
            return json.dumps(final_response)

        # test = dict()

        # test = {
        #     "name": "string",
        #     "description": "string",
        #     "fk_goal": [
        #         {"key_result_area": "string", "weightage": 100, "max_score": 4, "fk_xyz" : [{
        #             "name" : 5
        #         }]}
        #     ],
        # }
        # print(type(test["fk_goal"][0]))
        # print("test data", test)
        # return json.dumps(ParseData(test))
