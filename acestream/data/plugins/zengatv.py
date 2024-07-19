#-plugin-sig:JOqs8k6/3gMYouAx9UrJd74IqE5zSE+9751K+Xn6HQg0lkdY63IXgTNk+xD7d/5OG8GtcU4BBKeau8Vg8p95ur6wrmphbgkCwOb6cCZxn4D/1GfPh2P/hprLQGhHNwKlctcKTnEplfL3OTtsjo0JBanrjhyMAfgM86LGZHTqfI//WEzKDx2oe54kRwXtUwiCUdRoaO6/soFMpL+Dr7hdeqZVsR2ic/ENtMf2PTXYu6dXOCaSgGt1fqokI3Q2SSECXhwWOYCrSDLy8Di7NBUbUsmXOj1mmyOjQr4haI4sUghU+wAOCxHQgcXMwyW/uty7yvicg77lu7mec+k+tjvEMw==
"""
$description Indian live TV channels. OTT service from Zenga TV.
$url zengatv.com
$type live
"""

import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.stream.hls import HLSStream


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(
    r"https?://(www\.)?zengatv\.com/\w+",
))
class ZengaTV(Plugin):
    """Streamlink Plugin for livestreams on zengatv.com"""

    _id_re = re.compile(r"""id=(?P<q>["'])dvrid(?P=q)\svalue=(?P=q)(?P<id>[^"']+)(?P=q)""")
    _id_2_re = re.compile(r"""LivePlayer\(.+["'](?P<id>D\d+)["']""")

    api_url = "http://www.zengatv.com/changeResulation/"

    def _get_streams(self):
        headers = {"Referer": self.url}

        res = self.session.http.get(self.url, headers=headers)
        for id_re in (self._id_re, self._id_2_re):
            m = id_re.search(res.text)
            if not m:
                continue
            break

        if not m:
            log.error("No video id found")
            return

        dvr_id = m.group("id")
        log.debug("Found video id: {0}".format(dvr_id))
        data = {"feed": "hd", "dvrId": dvr_id}
        res = self.session.http.post(self.api_url, headers=headers, data=data)
        if res.status_code == 200:
            yield from HLSStream.parse_variant_playlist(self.session, res.text, headers=headers).items()


__plugin__ = ZengaTV
