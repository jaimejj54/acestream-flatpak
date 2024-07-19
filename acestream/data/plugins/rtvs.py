#-plugin-sig:Ckqkjm2nZRPAY3tViFZo180eNkUN5ar5iCP8yiqEruL2jtS/p/jeEs+Dg/VTsFRzewo02ltryueqqwQ0KW/QVxFfpnzw6P8yadupAOBH6d7lZ2v7neIAOL10IgIMcvPTWfa4rKllGycDey8hrdSO1WMsGluDjCAY/eNq+KnWux4E3oyaHrg2PyaFturoriRCSDmiQLMDY6kJZBgiQWi2M5xhR+JdE2DlX9NLr9arj6UMSqFVQqsqUsS+vZPF+h4+BZx3rJXaBjqOa/bFcmRQYxLeca0GCDxGyicyZkTy5ONpMQcLatiq4lPrE0hnWGnHVuHAETjtLzWmmy3knOkskw==
"""
$description Live TV channels from RTVS, a Slovak public, state-owned broadcaster.
$url rtvs.sk
$type live
$region Slovakia
"""

import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream
from streamlink.utils.parse import parse_json


@pluginmatcher(re.compile(
    r"https?://www\.rtvs\.sk/televizia/live-[\w-]+",
))
class Rtvs(Plugin):
    _re_channel_id = re.compile(r"'stream':\s*'live-(\d+)'")

    def _get_streams(self):
        res = self.session.http.get(self.url)
        m = self._re_channel_id.search(res.text)
        if not m:
            return

        res = self.session.http.get(
            "https://www.rtvs.sk/json/live5f.json",
            params={
                "c": m.group(1),
                "b": "mozilla",
                "p": "win",
                "f": "0",
                "d": "1",
            },
        )
        videos = parse_json(res.text, schema=validate.Schema({
            "clip": {
                "sources": [{
                    "src": validate.url(),
                    "type": str,
                }],
            }},
            validate.get(("clip", "sources")),
            validate.filter(lambda n: n["type"] == "application/x-mpegurl"),
        ))
        for video in videos:
            yield from HLSStream.parse_variant_playlist(self.session, video["src"]).items()


__plugin__ = Rtvs
