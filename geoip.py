# encoding=utf-8
import geoip2.database
import strings

reader = None


def load_data(filename, locale='en'):
    global reader
    reader = geoip2.database.Reader(filename, [locale])


def close_data():
    reader.close()


class IPData(object):
    _response = None
    country_iso_code = ''
    country_name = ''
    subdivision_iso_code = ''
    subdivision_name = ''
    city_name = ''
    postal_code = ''
    latitude = 0.0
    longitude = 0.0

    def __init__(self, response, locale):
        self._response = response
        if response is not None:
            try:
                self.country_iso_code = strings.strip_to_empty(response.country.iso_code_)
            except:
                pass
            try:
                self.country_name = strings.strip_to_empty(response.country.names[locale])
            except:
                pass
            try:
                self.subdivision_iso_code = strings.strip_to_empty(response.subdivisions.most_specific.iso_code)
            except:
                pass
            try:
                self.subdivision_name = strings.strip_to_empty(response.subdivisions.most_specific.names[locale])
            except:
                pass
            try:
                self.city_name = strings.strip_to_empty(response.city.names[locale])
            except:
                pass
            try:
                self.postal_code = strings.strip_to_empty(response.postal.code)
            except:
                pass
            try:
                self.latitude = response.location.latitude
            except:
                pass
            try:
                self.longitude = response.location.longitude
            except:
                pass


def find(ip, locale='en'):
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
    global reader
    try:
        response = reader.city(ip)
    except:
        response = None
    ip_data = IPData(response, locale)
    if strings.is_blank(ip_data.country_name):
        ip_data.country_name = "LAN"
    return ip_data
