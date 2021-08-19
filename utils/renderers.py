from rest_framework import renderers
import json


def DictionaryHandler(data, status_code):

    response = dict()
    if 'ErrorDetail' in str(data):
        print(data.__reduce__())
        print(type(data.__reduce__()), "xyz")
        
        error_dict =  data.__reduce__()[1][0]
        print(error_dict)

        errors = list()

        for key in error_dict:
            error_msg = str(key) + " : " + str(error_dict[key][0])
            print(error_msg)
            errors.append(error_msg)
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
        response['status_code'] = status_code
        response = json.dumps(response)

    return response


def ListHandler(data, status_code):

    response = dict()
    print(data.__reduce__()[1][0][0])
    print(type(data.__reduce__()[1][0][0]))

    objects = data.__reduce__()[1][0]

    final_response = dict()
    
    final_response["status_code"] = status_code

    

    if 'ErrorDetail' in str(data):
        

        all_errors = list()
        for key in objects:
            error_dict =  key
            print(error_dict)
            errors = list()
            for key in error_dict:
                error_msg = str(key) + " : " + str(error_dict[key][0])
                print(error_msg)
                errors.append(error_msg)
            all_errors.append(errors)
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
            
        response['status_code'] = status_code
        response = json.dumps(response)

    return response



class CustomRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        if renderer_context is not None:
            status_code = renderer_context['response'].status_code
            print(renderer_context['response'].status_code)
        
        print(type(data))
        
        if "Dict" in str(type(data)):
            return DictionaryHandler(data, status_code)
            
        else:
            return ListHandler(data, status_code)

        


                


            
        











