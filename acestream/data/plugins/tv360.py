#-plugin-sig:IEuOnAbp2GOrsbH6lEkU36L1IPZP0budMnovMYYmlWjUt9tVl/xj/v8sUHARGeC5jpLUbAHPfAMQzexPB6krhTVXaiEBWvVpgmfMR9646jXarM1xSLfreYCa3bUOowGDHP4LPvCtHNu5+RV2lOs+rlByO5BQ7O3i1HLj8jpuOVe6o7sDka7MHDlkGy6sP0ig5tYhQe3GpB0+ZQbjXu3CtdvZWuiPJ6/K9szlI6nwpp4R/RjUIJJHHpdEv6M52i1/HvV8pMr4kHq4kzIncbrKxk7p63ZDL2x5eKT5++sR1NbQF44W/pYNpJMRN4GXRUJOaX40Srzc14tc+G14zyMilQ==
"""
$description A privately owned Turkish live TV channel.
$url tv360.com.tr
$type live
"""

import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


@pluginmatcher(re.compile(
    r"https?://(?:www\.)?tv360\.com\.tr/canli-yayin",
))
class TV360(Plugin):
    def _get_streams(self):
        hls_url = self.session.http.get(self.url, schema=validate.Schema(
            validate.parse_html(),
            validate.xml_xpath_string(".//video/source[@src][@type='application/x-mpegURL'][1]/@src"),
            validate.none_or_all(validate.url()),
        ))
        if hls_url:
            return HLSStream.parse_variant_playlist(self.session, hls_url)


__plugin__ = TV360
