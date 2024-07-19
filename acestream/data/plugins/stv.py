#-plugin-sig:Fol7ad12yrkUpsMezIRWgR5Vb/RyXCrm5/RRmXclYvoIiB0FjluTuQeS2yyD7R2kmzJ4fS3NBO+tJ6IBQetpW+M3Tk0Rf/Olupko6CGTm89B6oqrX40i0aPXTDaZ/D50OeAmDfootRDp0bzwIgCHM1PhUfX04UPCDTLeKCCwVUTAY5QxhiyMWZX0AyEe7IUzC2VVdpBgtpWCJeRONOXZWBVeDFBy+Y7vsLw3xdmOztWM61G+zhPcpLKj5SgvpISufVFWLPcu33XOtNMDwDY/7qO2p8fIfysBl3Sp2wc7VB+KCmiWnT7uqkq3zyZGkKwD8gJMdgMt83NlyBN6zMXksA==
"""
$description Live TV channels from STV, a Scottish free-to-air broadcaster.
$url player.stv.tv
$type live
$region United Kingdom
"""

import logging
import re

from streamlink.plugin import Plugin, PluginError, pluginmatcher
from streamlink.stream.hls import HLSStream


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(
    r"https?://player\.stv\.tv/live",
))
class STV(Plugin):
    API_URL = "https://player.api.stv.tv/v1/streams/stv/"

    def get_title(self):
        if self.title is None:
            self._get_api_results()
        return self.title

    def _get_api_results(self):
        res = self.session.http.get(self.API_URL)
        data = self.session.http.json(res)

        if data["success"] is False:
            raise PluginError(data["reason"]["message"])

        try:
            self.title = data["results"]["now"]["title"]
        except KeyError:
            self.title = "STV"

        return data

    def _get_streams(self):
        hls_url = self._get_api_results()["results"]["streamUrl"]
        return HLSStream.parse_variant_playlist(self.session, hls_url)


__plugin__ = STV
