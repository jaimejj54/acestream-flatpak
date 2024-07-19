#-plugin-sig:Bn6spEpskiKVWGgG4S4al6rpKHUp8UKfK+CDbU0u2JijDP77/bw798m7d6kEZjUOkFOj2/3fZOqIfHQsaTSTBsHuBwKJzBHs3AsUVtU+9W/C02tqmQk4TjPDLiDklkfMhcqlJcil9Pdbzf5jigMpIAH3mhdIaJeOgwEB3lLsmBDPEX7ty5YWKMad1uVsODz+P29qOhfvCOzUC/RMEseJnjR2A7x1ocSwsxKZ5v6xxMCl7HT8uxk7MYMo15jmDH/Gbogd0qzbPZtKyYrkeVpOrSy9fNEXKK7xhREMMyzsLc6A+deXr7WsA3+mguzYoBFFf6qtD0gqI0AeNZuBZuRriA==
"""
$description Live TV channels and video on-demand service from CCMA, a Catalan public, state-owned broadcaster.
$url ccma.cat
$type live, vod
$region Spain
"""

import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(
    r"https?://(?:www\.)?ccma\.cat/tv3/directe/(?P<ident>.+?)/",
))
class TV3Cat(Plugin):
    _URL_STREAM_INFO = "https://dinamics.ccma.cat/pvideo/media.jsp"

    _MAP_CHANNELS = {
        "tv3": "tvi",
    }

    def _get_streams(self):
        ident = self.match.group("ident")

        schema_media = {
            "geo": str,
            "url": validate.url(path=validate.endswith(".m3u8")),
        }

        stream_infos = self.session.http.get(
            self._URL_STREAM_INFO,
            params={
                "media": "video",
                "versio": "vast",
                "idint": self._MAP_CHANNELS.get(ident, ident),
                "profile": "pc",
                "desplacament": "0",
                "broadcast": "false",
            },
            schema=validate.Schema(
                validate.parse_json(),
                {
                    "media": validate.any(
                        [schema_media],
                        validate.all(
                            schema_media,
                            validate.transform(lambda item: [item]),
                        ),
                    ),
                },
                validate.get("media"),
            ),
        )

        for stream in stream_infos:
            log.info(f"Accessing stream from region {stream['geo']}")
            try:
                return HLSStream.parse_variant_playlist(self.session, stream["url"], name_fmt="{pixels}_{bitrate}")
            except OSError:
                pass


__plugin__ = TV3Cat
