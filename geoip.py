# encoding=utf-8
import sys
import strings

reader = None
_DEFAULT_LOCALE = 'en'
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


def load_data(filename, *locale):
    import geoip2.database
    global reader
    _locale = list(set(list(locale) + [_DEFAULT_LOCALE]))
    reader = geoip2.database.Reader(filename, _locale)


def close_data():
    reader.close()


class IPData(object):
    def __init__(self, response, locale):
        self._response = response
        if response is not None:
            self.country_iso_code = self._format(response.country.iso_code)
            self.country_name = self._format(response.country.names, locale)
            self.subdivision_iso_code = self._format(response.subdivisions.most_specific.iso_code)
            self.subdivision_name = self._format(response.subdivisions.most_specific.names, locale)
            self.city_name = self._format(response.city.names, locale)
            self.postal_code = self._format(response.postal.code)
            self.latitude = response.location.latitude
            self.longitude = response.location.longitude
        else:
            self.country_iso_code = ''
            self.country_name = ''
            self.subdivision_iso_code = ''
            self.subdivision_name = ''
            self.city_name = ''
            self.postal_code = ''
            self.latitude = 0.0
            self.longitude = 0.0

    @staticmethod
    def _format(o, locale=None):
        temp = strings.strip_to_empty(o) if locale is None else o.get(locale, o.get(_DEFAULT_LOCALE, ""))
        return temp.encode('utf-8') if PY2 else temp


def find(ip, locale=_DEFAULT_LOCALE):
    """
    Get geo ip data
    :param ip: ip address
    :param locale:
        * de -- German
        * en -- English names may still include accented characters if that
          is the accepted spelling in English. In other words, English does
          not mean ASCII.
        * es -- Spanish
        * fr -- French
        * ja -- Japanese
        * pt-BR -- Brazilian Portuguese
        * ru -- Russian
        * zh-CN -- Simplified Chinese.
    :return:
    """
    import re
    if not re.match(strings.REG_IP, ip):
        raise ValueError("IP address format is not correct!")
    global reader
    try:
        response = reader.city(ip)
    except:
        response = None
    ip_data = IPData(response, locale)
    if strings.is_blank(ip_data.country_name):
        ip_data.country_name = "LAN"
    return ip_data
