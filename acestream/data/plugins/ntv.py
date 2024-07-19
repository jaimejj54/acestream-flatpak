#-plugin-sig:V7pLICc0Rr9sDc/7sNfU/BtgzkKuh4+LHSxBTCLpDQQGka2f7d3K0uGaGelGMhpaUwWD+2vKvP5GJcxgW5WFOZL6d2pGX2aRkDPEDjUqouzzbeq3DQF9jkDOMiM8upMz5+ey9bTrubReDGxsJDpvGRC8hdFmM3ydLHAq7FImKaeA9KF5pwBoExoTl9FQnxaMQf1zKSb9T9Cfvszf91tl0jwP6nU6TsLgfgLzNegCOcdVhRxjLwkB28d6GrYVt3rTA/EWlYHsgGo8yXhLsFTif8Ztf7Assimc6wIkgKN7xUc39GWRNJk0dZQSYp4olnBwQ+bvb9VdtRenvtUkUmnCIQ==
"""
$description Russian live TV channel owned by Gazprom Media.
$url ntv.ru
$type live
"""

import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.stream.hls import HLSStream


@pluginmatcher(re.compile(
    r"https?://www\.ntv\.ru/air/",
))
class NTV(Plugin):
    def _get_streams(self):
        body = self.session.http.get(self.url).text
        mrl = None
        match = re.search(r"var camHlsURL = \'(.*)\'", body)
        if match:
            mrl = f"http:{match.group(1)}"
        else:
            match = re.search(r"var hlsURL = \'(.*)\'", body)
            if match:
                mrl = match.group(1)
        if mrl:
            return HLSStream.parse_variant_playlist(self.session, mrl)


__plugin__ = NTV
