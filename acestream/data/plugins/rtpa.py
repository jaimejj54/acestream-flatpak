#-plugin-sig:d6iDIg8LnPr9bQKLRyiUqVIY+HScso02jucPFa4V2Tea7E7z4lsQYYQDgsgCezbWhC7yZPxyHtdJNo0IzWDDB3rt1J5MuICiXf/05/Mav7TMElzdAWcnXjFRcPwY78dUkOIUi2StqZPOnHoGBywPSv/Zg7qt8g8V053rWwvuAcHgc6Ljvpe6I2+yG2QmH4TsB7AK/aXhwdfuB2unuDi0CBcIVDbpFw0qYwcDpgydOHK3iNPNyzCrDhFSveBRokGv3T10BwV6Kn2j4EHKdhy4NlESuWiWxo/Ey+6jhmMX/DhTammS8b4DSf253nG2ZJ78nR13UCGqhMgoUnrZ7JK3aw==
"""
$description Live TV channels and video on-demand service from RTPA, a Spanish public broadcaster.
$url rtpa.es
$type live, vod
"""

import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


@pluginmatcher(re.compile(r"https?://(?:www\.)?rtpa\.es"))
class RTPA(Plugin):
    def _get_streams(self):
        hls_url, self.title = self.session.http.get(self.url, schema=validate.Schema(
            validate.parse_html(),
            validate.union((
                validate.xml_xpath_string(".//video/source[@src][@type='application/x-mpegURL'][1]/@src"),
                validate.xml_xpath_string(".//head/title[1]/text()"),
            )),
        ))
        if not hls_url:
            return
        return HLSStream.parse_variant_playlist(self.session, hls_url, headers={"Referer": self.url})


__plugin__ = RTPA
