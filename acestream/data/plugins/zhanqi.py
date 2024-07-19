#-plugin-sig:ddB+ptaI5eRFhwcJQSftnDjeN1z6lcNiYyI0S8hrcMG3swo6/YWGVA1DfE0esdijyXYWCuhVvpJaxmXK4eYtuD+h3rIviFVD5jTLVe9v1K9Wv/vmj/+U0iII4IdQIkl9pJTJvoVNqIyioqhziLu2JEHZpXlnVrxaMeq2NQ8bbe6M5gWWn7USb+ubbEFBo3LxIrB1N2wtqqgiTgta2PvTVCd0TbVVmanpu8Bm4sWNrWEvy7hKMAgqeyrK3pViNulAYX/mSNwmYiD2ztmzqpFQ4e/jQRQ/k440ocabbsvd9ws1UB6FDhcdtp1nuAAJt1gFld5mazBl4MnLDo0+yJTICQ==
"""
$description Chinese live streaming platform for live video game broadcasts.
$url zhanqi.tv
$type live
"""

import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream
from streamlink.stream.http import HTTPStream


log = logging.getLogger(__name__)

API_URL = "https://www.zhanqi.tv/api/static/v2.1/room/domain/{0}.json"

STATUS_ONLINE = 4
STATUS_OFFLINE = 0

_room_schema = validate.Schema(
    {
        "data": validate.any(None, {
            "status": validate.all(
                str,
                validate.transform(int),
            ),
            "videoId": str,
        }),
    },
    validate.get("data"),
)


@pluginmatcher(re.compile(
    r"https?://(www\.)?zhanqi\.tv/(?P<channel>[^/]+)",
))
class Zhanqitv(Plugin):
    def _get_streams(self):
        channel = self.match.group("channel")

        res = self.session.http.get(API_URL.format(channel))
        room = self.session.http.json(res, schema=_room_schema)
        if not room:
            log.info("Not a valid room url.")
            return

        if room["status"] != STATUS_ONLINE:
            log.info("Stream currently unavailable.")
            return

        url = "http://wshdl.load.cdn.zhanqi.tv/zqlive/{room[videoId]}.flv?get_url=".format(room=room)
        stream = HTTPStream(self.session, url)
        yield "live", stream

        url = "http://dlhls.cdn.zhanqi.tv/zqlive/{room[videoId]}_1024/index.m3u8?Dnion_vsnae={room[videoId]}".format(room=room)
        stream = HLSStream(self.session, url)
        yield "live", stream


__plugin__ = Zhanqitv
