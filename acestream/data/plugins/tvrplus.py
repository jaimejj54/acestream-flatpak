#-plugin-sig:TnTqYJR9tWWwO3CBw4z9C3ehJrzhU0kLEDU+axuTOyBoQBnFy6tSSdUiBJjJuwbR3kYEsjD1/sTC62oubLH8weVJnbyPKEg87Q67n63ynJ+V329f+OYIZYEpSwep4CbcWOqo/7b/eeFodylCYV+kqu/R2EQ1oafhopfSbeRUq5VdtcPXlivk+Umnzmoba8pHqUviOX5enPGYyx7kJbaM8jVIA5kwe5v6hTgBCcK5oMHROihJfxYttsl+nUVET948v83ZDChwbWYjl0E9SVsM4/Etg98NwexwPkRmWIZ3LKdhBBqAp6vmSjopOwuzzMiL1JdHBOXvTF55pdfVUKT3SQ==
"""
$description Live TV channels from TVR, a Romanian public, state-owned broadcaster.
$url tvrplus.ro
$type live
$region Romania
"""

import re

from streamlink.plugin import Plugin, PluginError, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


@pluginmatcher(re.compile(
    r"https?://(?:www\.)?tvrplus\.ro(?:/live/.+|/?$)",
))
class TVRPlus(Plugin):
    def _get_streams(self):
        try:
            hls_url = self.session.http.get(
                self.url,
                schema=validate.Schema(
                    re.compile(r"""(?P<q>["'])(?P<url>https?://\S+?\.m3u8\S*?)(?P=q)"""),
                    validate.get("url"),
                ),
            )
        except PluginError:
            return

        return HLSStream.parse_variant_playlist(self.session, hls_url, headers={"Referer": self.url})


__plugin__ = TVRPlus
