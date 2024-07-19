#-plugin-sig:TpoN4aMrh5T/qNgyNHmMQVzl4L6QVzTA2xG6sIKw816qfXQrvskoES29+rollRN1SQWqH5lwb1wRNcUsLvZuvqxZQs2dWrR9ku12oIUTVEpNBHOAX6Yb5nV3eCaO8W0ZSxcFNUpBgGVgtR/WAMRt7C1munB4O+6q3XHl7ujkgDXJD8i+HUyh4eLkMvVF+lpiGHyptwkNAvvkJaSVQ7ahbLEhyVZ9NWA41RtcVwa6UkhLP+cmQXfCDkpjD3VXV8B4LTeSqYgabkpP/w9KLdGBqyySmuaLaixAMQml01BJaYiKDBCXE1YSvZqPCDX+5pBFT0RN5MImadjLwDK02rlJUQ==
"""
$description Indian Hindi-language news channel covering world & Indian news, business, entertainment and sport.
$url zeenews.india.com
$type live
"""

import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.stream.hls import HLSStream


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(
    r"https?://zeenews\.india\.com/live-tv",
))
class ZeeNews(Plugin):
    HLS_URL = "https://z5ams.akamaized.net/zeenews/index.m3u8{0}"
    TOKEN_URL = "https://useraction.zee5.com/token/live.php"

    title = "Zee News"

    def _get_streams(self):
        res = self.session.http.get(self.TOKEN_URL)
        token = self.session.http.json(res)["video_token"]
        log.debug("video_token: {0}".format(token))
        yield from HLSStream.parse_variant_playlist(self.session, self.HLS_URL.format(token)).items()


__plugin__ = ZeeNews
