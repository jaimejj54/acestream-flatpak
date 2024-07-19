#-plugin-sig:jne8Y8VVijRQJ10opNgRvf/54MCFHU8nLha6zrnAUt0CbUnRE6jZvycG+WQVEjFqayp75uPD2UjIJKA+ISxWzYaYqEROqlYqGHdPwz00RIB1lrn/GNFAc2aEsRd10iEcO8znvi4AajRlgFuF70THm9VVEzg1EFSFA+MjBpL4G/RHdaqptB8Ht/pzK1PAZR1Z3A5uIMZERm21IxFbxSghpdAne3P8wun9i1zuo2jWVQpGJp0jQDX8JpYSPEhYHzTH/Nwr/moX9HFKZk7hufnIeXEroMtJ+7md4+KxUz5l2UfDne1VRrrzr3HDARpRRSSHMqkPNFjsqWEGzxdag5DcYQ==
"""
$description Current affairs and cultural channel owned by NHK, a Japanese public, state-owned broadcaster.
$url nhk.or.jp/nhkworld
$type live
"""

import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.stream.hls import HLSStream


API_URL = "http://{}.nhk.or.jp/nhkworld/app/tv/hlslive_web.json"


@pluginmatcher(re.compile(
    r"https?://(?:(\w+)\.)?nhk\.or\.jp/nhkworld",
))
class NHKWorld(Plugin):
    def _get_streams(self):
        # get the HLS json from the same sub domain as the main url, defaulting to www
        sdomain = self.match.group(1) or "www"
        res = self.session.http.get(API_URL.format(sdomain))

        stream_url = self.session.http.json(res)["main"]["wstrm"]
        return HLSStream.parse_variant_playlist(self.session, stream_url)


__plugin__ = NHKWorld
