import json


def _obj_to_dict(obj):
    result = {}
    for key in obj.__mapper__.c.keys():
        attr = getattr(obj, key)
        result[key] = str(attr) if attr else attr
    return result


def ls_to_json(ls):
    v = [x.to_dict() for x in ls]
    return json.dumps(v)


def json_able(cls):
    def _to_dict(self):
        return _obj_to_dict(self)

    cls.to_dict = _to_dict
    return cls
