from jsonpath import JSONPath

object = {

    'abc' : {
        'xyz' : 3
    }

}

print(JSONPath("$.abc").parse(object))