#-plugin-sig:FN+iFXDsBL6PIfnEHKCG/dfEgChUvhmPLX4LO6KHS1j84uldFphB8pExXtohxCqyGDswdAXCIoBKsMRIbvn5h0WaJWX9rPxb5Zp+cVFkPsPYRVEhh+Ft26y8PLuMg0kiLnfaCNZCtDGrERnl2en9bFvCBw/6b9l173cB/QfYiLNlJujV2N05joN57u60060V1O0gXXv9KcChb5OGqpGqfyiYGL0ZuGhnUP2suUMVaa7/5bpyVRR5ZTE/f5p8EO4h5iPQ7wZ0A8vE85dYRYruDEQByITv2kVHnIx64CtjzPCIPxjUNzSnUklGS3d+mId/+PQdC8Ruqb6MYggmt9GKgQ==
"""
$description Live TV channels and video on-demand service from IndiHome TV, owned by Telkom Indonesia.
$url indihometv.com
$type live, vod
$region Indonesia
"""

import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.dash import DASHStream
from streamlink.stream.hls import HLSStream


@pluginmatcher(re.compile(r"https?://(?:www\.)?indihometv\.com/"))
class IndiHomeTV(Plugin):
    def _get_streams(self):
        url = self.session.http.get(self.url, schema=validate.Schema(
            validate.parse_html(),
            validate.any(
                validate.all(
                    validate.xml_xpath_string("""
                        .//script[contains(text(), 'laylist.m3u8') or contains(text(), 'manifest.mpd')][1]/text()
                    """),
                    str,
                    re.compile(r"""(?P<q>['"])(?P<url>https://.*?/(?:[Pp]laylist\.m3u8|manifest\.mpd).+?)(?P=q)"""),
                    validate.none_or_all(
                        validate.get("url"),
                        validate.url(),
                    ),
                ),
                validate.all(
                    validate.xml_xpath_string(".//video[@id='video-player'][1]/source[1]/@src"),
                    validate.none_or_all(
                        validate.url(),
                    ),
                ),
            ),
        ))

        if url and ".m3u8" in url:
            return HLSStream.parse_variant_playlist(self.session, url)
        elif url and ".mpd" in url:
            return DASHStream.parse_manifest(self.session, url)


__plugin__ = IndiHomeTV
