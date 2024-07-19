#-plugin-sig:DP8QgazgocGQLdwLCDp5dHLvihnC1Dgyz/I3Mlli5VQ475ci0ThbWBiJCuPmP+Sdec2x/AfXxuN07lAN+OXz1whNIXEQdnM9e20ZLvMjzNn4Sz9G/dqzUTGgpN+5v5xGCD4kDe5OHcl+MiO9FKdhFM5nRnQfLNeO/O4sxM0Hq6FyijF6WhpZP/Y9X7CItNKposU9Ms0Vokj3nSPgIr5ZL3X75vxBS3UBaysT8vRfoAikTGbxuuJ8uq0e3AnQ4iOwjypqy5sV6H1RQocLWh2h4IFhiomKJwWgB0Qkr28GFt4dyXhttZPuBfstkLgzMV6QGUUlKqfQOTfsLAeoJehaUg==
"""
$description Live TV channels from VTV, a Vietnamese public, state-owned broadcaster.
$url vtvgo.vn
$type live
"""

import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(
    r"https?://vtvgo\.vn/xem-truc-tuyen-kenh-",
))
class VTVgo(Plugin):
    AJAX_URL = "https://vtvgo.vn/ajax-get-stream"

    def _get_streams(self):
        # get cookies
        self.session.http.get("https://vtvgo.vn/")

        self.session.http.headers.update({
            "Origin": "https://vtvgo.vn",
            "Referer": self.url,
            "Sec-Fetch-Site": "same-origin",
            "X-Requested-With": "XMLHttpRequest",
        })

        params = self.session.http.get(self.url, schema=validate.Schema(
            validate.parse_html(),
            validate.xml_xpath_string(".//script[contains(text(),'setplayer(')][1]/text()"),
            validate.none_or_all(
                validate.regex(
                    re.compile(r"""var\s+(?P<key>(?:type_)?id|time|token)\s*=\s*["']?(?P<value>[^"']+)["']?;"""),
                    method="findall",
                ),
                [
                    ("id", int),
                    ("type_id", str),
                    ("time", str),
                    ("token", str),
                ],
            ),
        ))
        if not params:
            return

        log.trace(f"{params!r}")
        hls_url = self.session.http.post(
            self.AJAX_URL,
            data=dict(params),
            schema=validate.Schema(
                validate.parse_json(),
                {"stream_url": [validate.url()]},
                validate.get(("stream_url", 0)),
            ),
        )

        return HLSStream.parse_variant_playlist(self.session, hls_url)


__plugin__ = VTVgo
