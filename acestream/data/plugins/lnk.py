#-plugin-sig:jTs3jNF4wAkdbGKmsRwX0TmFqqE8KBQElwTrNqPdd+QK6g2LTw9imrYiWuaS9wEF/rOq/oNFrX1eiDKCeF7OosmcZrqxsI+1LaQjgjj3ZYhI792xA+1jMHmeDa8pth5WcHS5s83DYTnp/H9K+wWDdhdGvWVFCzqxUf7g9RwKJZckpxo8VZyeXp25Sk0oEYH8TvBRfiGO7jLmmkTxumWSCsHIR+3hlupcODBIoB2L7Lk/wnkkvL3pMwIBlRl3ixu9PGkpPyErZfqPT0nxrbue1aZtt97MqsWSfvi5tjUHboTIGFDkfQUuEsQhob3FscslXWjlRbp6CzDy8DbxpEvyew==
"""
$description Lithuanian live TV channels from LNK Group, including 2TV, BTV, Info TV, LNK and TV1.
$url lnk.lt
$type live
$region Lithuania
"""

import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(
    r"https?://(?:www\.)?lnk\.lt/tiesiogiai(?:#(?P<channel>[a-z0-9]+))?",
))
class LNK(Plugin):
    API_URL = "https://lnk.lt/api/video/video-config/{0}"

    CHANNEL_MAP = {
        "lnk": 137535,
        "btv": 137534,
        "2tv": 95343,
        "infotv": 137748,
        "tv1": 106791,
    }

    def _get_streams(self):
        channel = self.match.groupdict().get("channel") or "lnk"
        if channel not in self.CHANNEL_MAP:
            log.error(f"Unknown channel: {channel}")
            return

        self.id = self.CHANNEL_MAP.get(channel)
        self.author, self.category, self.title, hls_url = self.session.http.get(
            self.API_URL.format(self.id),
            schema=validate.Schema(
                validate.parse_json(),
                {"videoInfo": {
                    "channel": str,
                    "genre": validate.any(None, str),
                    "title": validate.any(None, str),
                    "videoUrl": validate.any(
                        "",
                        validate.url(path=validate.endswith(".m3u8")),
                    ),
                }},
                validate.get("videoInfo"),
                validate.union_get("channel", "genre", "title", "videoUrl"),
            ),
        )
        if not hls_url:
            log.error("The stream is not available in your region")
            return

        return HLSStream.parse_variant_playlist(self.session, hls_url)


__plugin__ = LNK
