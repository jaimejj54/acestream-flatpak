#-plugin-sig:UINlfGNW2mRacCrw7hQ9ic6bkMWYqQjxRAY1FeRwjYchrkXcL6MLHfQNeNvh0D1UEqD5EWd6XN4sycnQjQitjGcPh9vw+ROmXQAcmHC/wn4+oEF3DyVp02LW8ogNU3ZruqLEABzjRhRLdpxLSXyKw+TBn6p0IrPHDYnuKjE6mwefxt/b6jtS74HJdWrukV/gagPS9qWsHezb9bM/hKVIrb7FplJTyWFB2e/dIvrTprT/Fj/KnuvAyU9QOK3veWIRnp2BY9aLyfqlPj3VeAldqwYrfWhFbJpgLGe2yFM0IdTMF9jHI4Q+1wdJrhYtbYAZ+De7HSoTxopl8I4UjPRfHQ==
"""
$description Polish live TV channel owned by Toya.
$url tvtoya.pl
$type live
"""

import re

from streamlink.plugin import Plugin, PluginError, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


@pluginmatcher(re.compile(
    r"https?://(?:www\.)?tvtoya\.pl/player/live",
))
class TVToya(Plugin):
    def _get_streams(self):
        try:
            hls = self.session.http.get(self.url, schema=validate.Schema(
                validate.parse_html(),
                validate.xml_xpath_string(".//script[@type='application/json'][@id='__NEXT_DATA__']/text()"),
                str,
                validate.parse_json(),
                {
                    "props": {
                        "pageProps": {
                            "type": "live",
                            "url": validate.all(
                                str,
                                validate.transform(lambda url: url.replace("https:////", "https://")),
                                validate.url(path=validate.endswith(".m3u8")),
                            ),
                        },
                    },
                },
                validate.get(("props", "pageProps", "url")),
            ))
        except PluginError:
            return

        return HLSStream.parse_variant_playlist(self.session, hls)


__plugin__ = TVToya
