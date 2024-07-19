#-plugin-sig:QHjWDZDfuRwInWAXMFBZn1kZLGAjTKAHc+enCVcsO11oh63Gcppx8I+sLiCukbfNg+7npJno0vqiiGtDIFqSYkI0H3xgiL+WCD7f93iB9rVhUqI2YudhMKtrY7JxwM5owiXe+Li7CaxPnWbrWHAdi3r86OMlUSw1C3QKh6ocTJtOO3NMY1Q2tAnTe4xJUCepMeF07wo/I3FbpH5EmnGiAF4/KZNzfGsqWRJeQty8cYQcuOpJnFfzlJKM+p2S93qkiTUgo3ydKaA+rniDGYdZrG/KkvY2WXtii9+B8DESkBaQYGYmjcI1Ux9UX/9TYCu1DPr9kmRMuYO7KfWzezoxJQ==
"""
$description 24-hour live-streaming world news channel, based in the United States of America.
$url cbsnews.com
$type live
"""

import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


@pluginmatcher(re.compile(
    r"https?://(?:www\.)?cbsnews\.com/(?:\w+/)?live/?",
))
class CBSNews(Plugin):
    def _get_streams(self):
        data = self.session.http.get(self.url, schema=validate.Schema(
            re.compile(r"CBSNEWS\.defaultPayload\s*=\s*(\{.*?})\s*\n"),
            validate.none_or_all(
                validate.get(1),
                validate.parse_json(),
                {
                    "items": [{
                        "id": str,
                        "canonicalTitle": str,
                        "video": validate.url(),
                        "format": "application/x-mpegURL",
                    }],
                },
                validate.get(("items", 0)),
                validate.union_get("id", "canonicalTitle", "video"),
            ),
        ))
        if not data:
            return

        self.id, self.title, hls_url = data

        return HLSStream.parse_variant_playlist(self.session, hls_url)


__plugin__ = CBSNews
