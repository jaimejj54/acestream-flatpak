#-plugin-sig:N3960/IBSRNnOhVIsgiwdTH5X0RCk7IkRut9LXqT1/3ZjDXV+0twvSBNYzjG5wVjqubxuCj08iEAc7xjGht0Iw7BbNGTZp9+q589REMuT9BAUzDaEefkE36JO96Bp/0zdT/ALBSprsIQ013NfqfSVvT2NqCzHttb/+gioalt8Nj4DwEc6Ume3UQWEJsbv0JkXIQSyVbLnJXx7EgbaTiABnZwbeMmYC3iPr78MamRGYuqA2/CeTLaTTcIktBBq64sgm6vDTlExfMC45iS00yOiPfJGvpLUNRsrcT4AH8616PVY8Wddl652oEm3br5m4AKzRd5cK/ExSEi9ETVt3j16g==
"""
$description Live TV channels from RSI and SRF, operations of SRG SSR, a Swiss public broadcaster.
$url srf.ch
$url rsi.ch
$type live
$region Switzerland
"""

import logging
import re
from urllib.parse import parse_qsl, urlparse, urlunparse

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.stream.hls import HLSStream


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(r"""
    https?://(?:
        live\.(rsi)\.ch/|
        (?:www\.)?(srf)\.ch/sport/resultcenter
    )
""", re.VERBOSE))
class Swisstxt(Plugin):
    api_url = "http://event.api.swisstxt.ch/v1/stream/{site}/byEventItemIdAndType/{id}/HLS"

    def get_stream_url(self, event_id):
        site = self.match.group(1) or self.match.group(2)
        api_url = self.api_url.format(id=event_id, site=site.upper())
        log.debug("Calling API: {0}".format(api_url))

        stream_url = self.session.http.get(api_url).text.strip("\"'")

        parsed = urlparse(stream_url)
        query = dict(parse_qsl(parsed.query))
        return urlunparse(parsed._replace(query="")), query

    def _get_streams(self):
        event_id = dict(parse_qsl(urlparse(self.url).query.lower())).get("eventid")
        if event_id is None:
            return

        stream_url, params = self.get_stream_url(event_id)
        return HLSStream.parse_variant_playlist(self.session,
                                                stream_url,
                                                params=params)


__plugin__ = Swisstxt
