import json
import os


class InvalidJsonPathError(Exception):
    """Exception raised for errors in the input path from a json arq.

    Attributes:
        path -- input path which caused the error
        message -- explanation of the error
    """

    def __init__(self, path, message="the path is not a valid for a json arq"):
        self.path = path
        self.message = message
        super().__init__(self.message)


class JsonMutableType:
    types = {}
    primitive = None
    def __init_subclass__(cls, **kwargs):
        JsonMutableType.types[cls.primitive] = cls

    @staticmethod
    def parse(value, arq):
        if type(value) in JsonMutableType.types:
            return JsonMutableType.types[type(value)](arq, value)

        if isinstance(value, tuple):
            return tuple(JsonMutableType.parse(i, arq) for i in value)


        return value

class JsonList(list, JsonMutableType):
    primitive = list
    def __init__(self, arq, l:list = None):
        self.json_arq = arq
        super(JsonList, self).__init__([] if l is None else [JsonMutableType.parse(i, arq) for i in l])

    def append(self, item):
        super(JsonList, self).append(JsonMutableType.parse(item, self.json_arq))
        if self.json_arq.auto_save:
            self.json_arq.save()

    def insert(self, index, item):
        super(JsonList, self).insert(index, JsonMutableType.parse(item, self.json_arq))
        if self.json_arq.auto_save:
            self.json_arq.save()

    def __setitem__(self, key, item):
        super().__setitem__(key, JsonMutableType.parse(item, self.json_arq))
        if self.json_arq.auto_save:
            self.json_arq.save()

    def __delitem__(self, key):
        super(JsonList, self).__delitem__(key)
        if self.json_arq.auto_save:
            self.json_arq.save()


class JsonDict(dict, JsonMutableType):
    primitive = dict
    def __init__(self, arq, d:dict = None):
        self.json_arq = arq
        super(JsonDict, self).__init__({} if d is None else {str(k): JsonMutableType.parse(v, arq) for k, v in d.items()})

    def __setitem__(self, key, item):
        super().__setitem__(str(key), JsonMutableType.parse(item, self.json_arq))
        if self.json_arq.auto_save:
            self.json_arq.save()

    def update(self, d, **kwargs):
        d = {str(k): JsonMutableType.parse(v, self.json_arq) for k, v in d.items()}
        super(JsonDict, self).update(d, **kwargs)
        if self.json_arq.auto_save:
            self.json_arq.save()

    def __delitem__(self, key):
        super().__delitem__(str(key))
        if self.json_arq.auto_save:
            self.json_arq.save()


class JsonArq(JsonDict):
    @staticmethod
    def valid_path(caminho):
        return isinstance(caminho, str) \
               and len(caminho) > 5 \
               and caminho.endswith('.json')

    def __init__(self, caminho, overwrite_if_exists: bool = False, auto_save: bool = False):
        super(JsonArq, self).__init__(arq=self)
        self.__caminho = caminho
        self.auto_save = auto_save

        # gerar erro caso caminho não seja válido
        if not JsonArq.valid_path(caminho):
            raise InvalidJsonPathError(caminho)

        # criar arquivo caso nescessário
        if not os.path.isfile(caminho) or overwrite_if_exists:
            with open(caminho, 'w') as arq:
                arq.write(json.dumps({}))

        # carrega informações do arquivo
        else:
            with open(caminho, 'r') as arq:
                self.update(json.loads(arq.read()))

    def save(self):
        with open(self.__caminho, 'w') as arq:
            arq.write(json.dumps(self))

    @property
    def caminho(self):
        return self.__caminho

    @caminho.setter
    def caminho(self, value):
        # gerar erro caso caminho não seja válido
        if not JsonArq.valid_path(value):
            raise InvalidJsonPathError(value)

        os.rename(self.__caminho, value)
        self.__caminho = value