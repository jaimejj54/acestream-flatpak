#-plugin-sig:l+noF5NLm0y7eCrcXtuZ58szwePEtExXPKwfcsX8pQeEkdPY0G/n9iqSfLQ/Om8+LcHQ04aGgnLNQ2TDkyputVphSby2Xm6+D0KWn7MFuMk4XU0DOpoQeWqh2u0kbzJmj4JtxbjU0vvH/U2yoeuFQocYH7UxjzNuY3krLgnl9N5iaCRDpmCq9e4PvdsOj7VT+pfAJ4hkc64B/sqKxaYtw/wOouePSXKTf6NGOY6WcXpj3s2y8i97sxRkXeBR/ozAzpDR7fKpGCLKEKxu0Wumjywsz//blrkDWRuG3bUFsd0Jc/j/QrUuVmzqfsc1U7CgUkjMofGtZUFwR0TZA7BzUQ==
"""
$description Sporting channel live stream owned by Sportal, a Bulgarian sports media website.
$url sportal.bg
$type live
"""

import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.stream.hls import HLSStream


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(
    r"https?://(?:www\.)?sportal\.bg/sportal_live_tv\.php",
))
class Sportal(Plugin):
    _hls_re = re.compile(r"""["'](?P<url>[^"']+\.m3u8[^"']*?)["']""")

    def _get_streams(self):
        res = self.session.http.get(self.url)
        m = self._hls_re.search(res.text)
        if not m:
            return

        hls_url = m.group("url")
        log.debug("URL={0}".format(hls_url))
        log.warning("SSL certificate verification is disabled.")
        return HLSStream.parse_variant_playlist(
            self.session, hls_url, verify=False).items()


__plugin__ = Sportal
