#-plugin-sig:PC4ThIPNDQem8sVj5pDxY+cf862fp0Wml5ISc6E8oVcS9sw4oHeEMj0keQgSIQl7Ibd5e8iK1g/SrKNvhd8DbL3iYu5F1u/pT4plijnImQKuI5eeUmOrXNGqOJ/Bki4h1xSXS8r64izotRIF11S5qQBONGpRVKrO6ZfbWBYJj3vl5B6qlqadxw1N5g7q0I3QPlp1+nenPV4dIR/s9Gie9T2s0Q+NpuSEAcky6WkqecRWfG7XT5OyfpqMcO+kuyD0zrC9/GTX5xg9FtguhFIXZ2+Gk+clZXQ/RfxEvb2+a4A0rf32JowcpABlzoC5hADgmKKfEsAVZBY2xDVlneb2aA==
"""
$description Japanese live-streaming and video hosting social platform.
$url live.line.me
$type live, vod
"""

import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


@pluginmatcher(re.compile(
    r"https?://live\.line\.me/channels/(?P<channel>\d+)/broadcast/(?P<broadcast>\d+)",
))
class LineLive(Plugin):
    _URL_API = "https://live-api.line-apps.com/web/v4.0/channel/{channel}/broadcast/{broadcast}/player_status"

    def _get_streams(self):
        channel = self.match.group("channel")
        broadcast = self.match.group("broadcast")

        schema_hls_urls = validate.any(None, {
            str: validate.any(None, validate.url(path=validate.endswith(".m3u8"))),
        })

        status, liveUrls, vodUrls = self.session.http.get(
            self._URL_API.format(channel=channel, broadcast=broadcast),
            schema=validate.Schema(
                validate.parse_json(),
                {
                    "liveStatus": str,
                    "liveHLSURLs": schema_hls_urls,
                    "archivedHLSURLs": schema_hls_urls,
                },
                validate.union_get("liveStatus", "liveHLSURLs", "archivedHLSURLs"),
            ),
        )
        streams = {"LIVE": liveUrls, "FINISHED": vodUrls}.get(status, {})

        if streams.get("abr"):
            return HLSStream.parse_variant_playlist(self.session, streams.get("abr"))

        return {
            f"{quality}p": HLSStream(self.session, url)
            for quality, url in streams.items()
            if url and quality.isdecimal()
        }


__plugin__ = LineLive
