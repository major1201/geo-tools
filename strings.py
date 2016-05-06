# encoding= utf-8
import string


REG_IP = "(([2][5][0-5]|[2][0-4][0-9]|[1][0-9]{2}|[1-9][0-9]|[0-9])[.]){3}([2][5][0-5]|[2][0-4][0-9]|[1][0-9]{2}|[1-9][0-9]|[0-9])"

def is_none(s):
    return s is None


def is_not_none(s):
    return not is_none(s)


def is_empty(s):
    return is_none(s) or len(str(s)) == 0


def is_not_empty(s):
    return not is_empty(s)


def is_blank(s):
    if is_empty(s):
        return True
    for char in s:
        if char not in string.whitespace:
            return False
    return True


def is_not_blank(s):
    return not is_blank(s)


def strip_to_none(s):
    if is_blank(s):
        return None
    else:
        return s.strip()


def strip_to_empty(s):
    if is_blank(s):
        return ""
    else:
        return s.strip()


def ltrim(s, replacement=" "):
    if s.startswith(replacement):
        return s[len(replacement):]
    return s


def rtrim(s, replacement=" "):
    if s.endswith(replacement):
        return s[:-len(replacement)]
    return s


def trim(s, replacement=" "):
    return rtrim(ltrim(s, replacement), replacement)


def equals_ignore_case(s1, s2):
    return False if s1 is None or s2 is None else s1.lower() == s2.lower()


def to_json(o):
    import json
    from datetime import date
    from datetime import datetime

    class CJsonEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(obj, date):
                return obj.strftime("%Y-%m-%d")
            else:
                return json.JSONEncoder.default(self, obj)
    return json.dumps(o, cls=CJsonEncoder, ensure_ascii=False)


def uuid():
    import uuid
    return str(uuid.uuid4()).replace("-", "")


def get_between(ori, start, end):
    ori = str(ori)
    start = str(start)
    end = str(end)
    s = ori.find(start)
    if s >= 0:
        e = ori.find(end, s + len(start))
        if e >= 0:
            return ori[s + len(start):e]
    return ""


def get_all_between(ori, start, end):
    ret = []
    ori = str(ori)
    start = str(start)
    end = str(end)
    find_start = 0
    ls = len(start)
    le = len(end)
    while True:
        s = ori.find(start, find_start)
        if s >= 0:
            e = ori.find(end, s + ls)
            if e >= 0:
                ret.append(ori[s + ls:e])
                find_start = e + le
                continue
        break
    return ret
