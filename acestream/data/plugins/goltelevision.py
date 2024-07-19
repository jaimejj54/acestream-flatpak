#-plugin-sig:GPjSA+gmN+kUE6w/YI1fuLSS0NG84OeJ17g2O4Ew3AO9DEF8s09ch9BXe3yevnPBytp4DURHY3mQ6jZPj9gmf0iyF6M9j/r+2GXcQcZEPR/3K8byemXn6TKX1YZzys+iXtkJ/1QwoII5tWfJR1cJuLwiS+alwoJubkmjYdvTv8lJgTkHlwqRWyeh2U0pDJ8ji7bbMKZoKA+CW5rGWuRXlZhJKJsEtQKOJQNtZq8qoNXj+iKuxjI+HIBIQ7Lc+2gl9o9L4GZhxXsZ9MJChcQWPc2DWAcmP9poTcs472I+aFXuLetSxy2PzJ5gnBkOE+1AqriX5OpuJ2ST0kIY/rxfYw==
"""
$description Spanish live TV sports channel owned by Gol Network.
$url goltelevision.com
$type live
$region Spain
"""

import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


@pluginmatcher(re.compile(
    r"https?://(?:www\.)?goltelevision\.com/en-directo",
))
class GOLTelevision(Plugin):
    def _get_streams(self):
        self.session.http.headers.update({
            "Origin": "https://goltelevision.com",
            "Referer": "https://goltelevision.com/",
        })
        url = self.session.http.get(
            "https://play.goltelevision.com/api/stream/live",
            schema=validate.Schema(
                validate.parse_json(),
                {"manifest": validate.url()},
                validate.get("manifest"),
            ),
        )
        return HLSStream.parse_variant_playlist(self.session, url)


__plugin__ = GOLTelevision
