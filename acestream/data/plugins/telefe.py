#-plugin-sig:Lk7BrNxXz8ny/IKovLnAG95CgK9EaZ4I2qXlbTVULYVvklHdonXCJG/JEszhVNWzzFaGZevmH/qGMkMb4+OH01mepyFa1xvDxTHboBCFy+2Jspt3/jekLJzD/6puuWI9foZ6jx6uBPCLp+92T6SdTkREI62b91fexKjQ47EZjm7Rxlbt0Tt/MJq9CX+DdplKjrgwH54T8kKMbWHzZ7EOD6096ikh6XROEX3Yw2k7zALDMONg5lXRjNbpkN5ttJjzsvEqQgLg7uPeDyajsLYqaD1sqWXaH16c6t+TH5ROYDLhCM9BobAkQTiRY43AfwR41tXglDgn8aJcDl/r7jZNjQ==
"""
$description Video content from Telefe, an Argentine TV station.
$url mitelefe.com
$type live
$region Argentina
"""

import logging
import re
from urllib.parse import urljoin

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(r"https://mitelefe\.com/vivo"))
class Telefe(Plugin):
    def _get_streams(self):
        self.title, hls_url = self.session.http.get(
            self.url,
            schema=validate.Schema(
                validate.parse_html(),
                validate.xml_xpath_string(".//script[contains(text(), 'HLS')]/text()"),
                validate.none_or_all(
                    re.compile(r"=\s*(\{.+?});", re.DOTALL | re.MULTILINE),
                    validate.none_or_all(
                        validate.get(1),
                        validate.parse_json(),
                        {str: {"children": {"top": {"model": {"videos": [{
                            "title": str,
                            "sources": validate.all(
                                [{"url": str, "type": str}],
                                validate.filter(lambda p: p["type"].lower() == "hls"),
                                validate.get((0, "url")),
                            ),
                        }]}}}}},
                        validate.transform(lambda k: next(iter(k.values()))),
                        validate.get(("children", "top", "model", "videos", 0)),
                        validate.union_get("title", "sources"),
                    ),
                ),
            ),
        )
        return HLSStream.parse_variant_playlist(self.session, urljoin(self.url, hls_url))


__plugin__ = Telefe
