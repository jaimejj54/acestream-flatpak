#-plugin-sig:jokRTJ3o2i0vbL6q6YewwJ6FK/UJBJeTIoX5fkU3osS14o+zGr3IeHHGDQgAHHwxXmaWcG3cuOx0IHZqKFqQ5KqGxT7HmWUgDY72XoLpVfNxoZbtsDP/qnJpGw8pWXzBcCgm7QWK8ZaoCeXUaLvs28o2LInZu+RY+pKR4mL2Wx9fX3HFw2z6F1ACLYTCLYYb4+FOFfnhEKjn9IeAU/aIr0+olFuwzWFyvW/ED+MjZ1bw81R0nzddzDt/HO61Sft+4xJOYFCuQOnL1H91VTxnlLCZwTT+Ynt3ZJz2MQO7R4yHAVXPHGxj8PAP0DS2QpoxIrqIM1MXQ64lBAnxTz3f1g==
"""
$description Turkish live TV channel owned by Fox Network.
$url fox.com.tr
$type live
"""

import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


@pluginmatcher(re.compile(
    r"https?://(?:www\.)?fox(?:play)?\.com\.tr/",
))
class FoxTR(Plugin):
    def _get_streams(self):
        re_streams = re.compile(r"""(['"])(?P<url>https://\S+/foxtv\.m3u8\S+)\1""")
        res = self.session.http.get(self.url, schema=validate.Schema(
            validate.transform(re_streams.findall),
        ))
        for _, stream_url in res:
            return HLSStream.parse_variant_playlist(self.session, stream_url)


__plugin__ = FoxTR
