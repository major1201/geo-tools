#! /usr/bin/env python
# encoding: utf-8
from __future__ import division, absolute_import, with_statement, print_function
import sys
import os
import socket
import re
import geoip
import strings


def write(s):
    sys.stdout.write(s.decode('utf-8') if geoip.PY2 else s)


class Geo(object):

    LANGUAGE_PACK = {
        "de": ["ISO-Ländercode ", "Ländername", "Vorort ISO-Code",
               "Vorort Name", "Stadtname", "Postleitzahl", "Breite", "Länge"],
        "en": ["Country ISO code", "Country name", "Subdivision ISO code",
               "Subdivision name", "City name", "Postal code", "Latitude", "Longitude"],
        "es": ["código de país ISO", "Nombre del país", "Barrio código ISO",
               "nombre de la subdivisión", "Nombre de la ciudad", "Código postal", "Latitud", "Longitud"],
        "fr": ["Code ISO du pays", "Nom du pays", "Barrio código ISO",
               "Nom de lotissement", "Nom de Ville", "Code postal", "Latitude", "Longitude"],
        "ja": ["国のISOコード", "国名", "区ISOコード",
               "区名", "市名", "郵便番号", "緯度", "経度"],
        "pt-BR": ["código de país ISO", "Nome do país", "código ISO subdivisão",
                  "nome do Bairro", "Nome da Cidade", "Código postal", "Latitude", "Longitude"],
        "ru": ["Код страны ISO", "Имя страны", "Код подразделения ISO",
               "название Район", "Название города", "Почтовый индекс", "широта", "долгота"],
        "zh-CN": ["国家ISO代码", "国家", "省级ISO代码",
                  "省级名称", "城市名称", "邮政编码", "纬度", "经度"]
    }

    def __init__(self):
        self._args = self._get_args()

    def __enter__(self):
        # load geoip database
        geoip.load_data(os.path.join(os.path.dirname(__file__), "GeoLite2-City.mmdb"), self._args.language)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # close geoip reader
        geoip.close_data()

    def _get_args(self):
        import argparse
        parser = argparse.ArgumentParser(prog="geo-info", description="Display the geo info of hosts/IPs", formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1a")
        parser.add_argument("hosts", metavar="hosts/IPs", nargs='*', help="host names or IP addresses")
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-d", "--detail", dest="detail", action="store_true", help="display geo info in detail")
        group.add_argument("-f", "--format", dest="format",
                           help="display geo info in format specified\n"
                                "%%h -- hostname given\n"
                                "%%i -- first ip address resolved\n"
                                "%%I -- country iso code\n"
                                "%%C -- country name\n"
                                "%%S -- subdivision iso code\n"
                                "%%s -- subdivision name\n"
                                "%%c -- city name\n"
                                "%%p -- postal code\n"
                                "%%l -- latitude\n"
                                "%%g -- longitude")
        parser.add_argument("-l", "--language", dest="language", default="en",
                            choices=["de", "en", "es", "fr", "ja", "pt-BR", "ru", "zh-CN"],
                            help="display language, default is english(en)\n"
                            "* de -- German\n"
                            "* en -- English names may still include accented characters if that\n"
                            "  is the accepted spelling in English. In other words, English does\n"
                            "  not mean ASCII.\n"
                            "* es -- Spanish\n"
                            "* fr -- French\n"
                            "* ja -- Japanese\n"
                            "* pt-BR -- Brazilian Portuguese\n"
                            "* ru -- Russian\n"
                            "* zh-CN -- Simplified Chinese.")
        _args = parser.parse_args()
        assert isinstance(_args, argparse.Namespace)
        return _args

    def _get_one(self, ip):
        _data = geoip.find(ip, self._args.language)
        if self._args.detail:
            return "\n".join([
                self.LANGUAGE_PACK[self._args.language][0] + ": " + _data.country_iso_code,
                self.LANGUAGE_PACK[self._args.language][1] + ": " + _data.country_name,
                self.LANGUAGE_PACK[self._args.language][2] + ": " + _data.subdivision_iso_code,
                self.LANGUAGE_PACK[self._args.language][3] + ": " + _data.subdivision_name,
                self.LANGUAGE_PACK[self._args.language][4] + ": " + _data.city_name,
                self.LANGUAGE_PACK[self._args.language][5] + ": " + _data.postal_code,
                self.LANGUAGE_PACK[self._args.language][6] + ": " + str(_data.latitude),
                self.LANGUAGE_PACK[self._args.language][7] + ": " + str(_data.longitude),
            ])
        else:
            return ", ".join(filter(lambda e: strings.is_not_blank(e), [_data.country_name, _data.subdivision_name, _data.city_name]))

    def _get_output(self, hostname):
        try:
            _hostname, _aliaslist, _ipaddrlist = socket.gethostbyname_ex(hostname)
        except socket.gaierror:
            return [hostname + "(Can't resolve the host)."]
        else:
            arr = []
            for ip in _ipaddrlist:
                if self._args.detail:
                    arr.append(hostname + "(" + ip + "):\n" + self._get_one(ip))
                else:
                    arr.append(hostname + "(" + ip + ") - " + self._get_one(ip))
            return arr

    def _format(self, host, _format):
        assert isinstance(_format, str)
        ip = socket.gethostbyname(host)
        data = geoip.find(ip, self._args.language)
        _format = _format.replace("%h", host)\
            .replace("%i", ip)\
            .replace("%I", str(data.country_iso_code))\
            .replace("%C", str(data.country_name))\
            .replace("%S", str(data.subdivision_iso_code))\
            .replace("%s", str(data.subdivision_name))\
            .replace("%c", str(data.city_name))\
            .replace("%p", str(data.postal_code))\
            .replace("%l", str(data.latitude))\
            .replace("%g", str(data.longitude))
        return _format

    def gen_std_line(self):
        buf_in = sys.stdin.readline()
        while strings.is_not_empty(buf_in):
            try:
                yield buf_in[:-1]
                buf_in = sys.stdin.readline()
            except IOError:
                pass

    def start(self):
        if len(self._args.hosts) == 0:
            # read from stdin
            for line in self.gen_std_line():
                search = re.search(strings.REG_IP, line)
                _format = self._args.format if self._args.format else '%C %s %c'
                if search:
                    write(line + "\t" + self._format(search.group(0), _format))
                else:
                    write(line)
                write("\n")
        else:
            if self._args.format:
                try:
                    write(self._format(self._args.hosts[0], self._args.format))
                except socket.gaierror:
                    sys.stderr.write("Can't resolve name: " + self._args.hosts[0])
            else:
                for host in self._args.hosts:
                    if self._args.detail:
                        write("\n\n".join(self._get_output(host)))
                        write("\n")
                    else:
                        write("\n".join(self._get_output(host)))
                    write("\n")


if __name__ == "__main__":
    try:
        with Geo() as geo:
            geo.start()
    except (KeyboardInterrupt, SystemExit):
        exit(1)
