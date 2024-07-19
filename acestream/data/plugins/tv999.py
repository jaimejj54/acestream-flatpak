#-plugin-sig:BnW3rfBMAh3aGBTBd+UzwyhfPXx5EihgqmJRIz9v6mwcau9+ZxVSpU0a6aadqVeihjhGvkV/FMXdTIOGpm5br++faDdVEBZYy9gaw6T1/caywERoNU8+cFvzkI4O4WoHGLtegKnlktCRJk9AbFwYfLSnPXr011MFoL7YO4/dA4hrlZF+q6Gxh+wnCKRl/ieJabHCogCnYH3AX2DOr3qLyMnKvGzIojK5unmSQk5KwpXvUfhfOiOlaKSqiaH470AVqcdwcTQufgI+h5GCqX5bvYQR7JPCbZwgFfgd7pgIxh/tjLKzmZWgAz5WbUZaZaup45kYFz0Fc2rDJ8VDR2Ef5Q==
"""
$description Turkish live TV channel owned by Detelina Media.
$url tv999.bg
$type live
$region Bulgaria
"""

import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream
from streamlink.utils.url import update_scheme


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(
    r"https?://(?:www\.)?tv999\.bg/live",
))
class TV999(Plugin):
    title = "TV999"

    def _get_xpath_string(self, url, xpath):
        return self.session.http.get(
            url,
            schema=validate.Schema(
                validate.parse_html(),
                validate.xml_xpath_string(xpath),
                validate.any(None, validate.url()),
            ),
        )

    def _get_streams(self):
        iframe_url = self._get_xpath_string(self.url, ".//iframe[@src]/@src")
        if not iframe_url:
            return
        hls_url = self._get_xpath_string(iframe_url, ".//source[contains(@src,'m3u8')]/@src")
        if not hls_url:
            return
        return {"live": HLSStream(self.session, update_scheme("http://", hls_url))}


__plugin__ = TV999
