#-plugin-sig:hBf8mCobNVXHHqN2WbSNvYzO+Zg22+tt2GQXoPLOa6qdA9VX0RL9pNRO+c9LZzqvQDm+Q+X7t1nuLuokksmA1xx3UOsOomXvDr9jn7oH9BAXDQbe+O/0GpDLPfB6FEFbwkyYVFGYvxE4oI9s46eyQQVtr3nGP4aA4gqxNilpmAtI275VWoGeMkc64gWmwAgBWTEuRyrqp6rRB1UHhPcBY9m2cy+Wu33IZ4WvcnhqxqOrMATB4aahjp/UQyOSoHzjXdxHh8XvpuN/vS3G7iBmJyiqirJot8H5aK7QqY26GUQcI3RTZgg3IQ+SHhJFFiO2Az7C4Tcy8JKVrgk7wpEq7A==
"""
$description Turkish live TV channel owned by Galatasaray TV.
$url galatasaray.com
$type live
"""

import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.stream.hls import HLSStream


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(
    r"https?://(?:www\.)?galatasaray\.com",
))
class GalatasarayTV(Plugin):
    playervars_re = re.compile(r"sources\s*:\s*\[\s*\{\s*type\s*:\s*\"(.*?)\",\s*src\s*:\s*\"(.*?)\"", re.DOTALL)

    title = "Galatasaray TV"

    def _get_streams(self):
        res = self.session.http.get(self.url)
        match = self.playervars_re.search(res.text)
        if match:
            stream_url = match.group(2)
            log.debug("URL={0}".format(stream_url))
            return HLSStream.parse_variant_playlist(self.session, stream_url)


__plugin__ = GalatasarayTV
