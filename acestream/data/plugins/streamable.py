#-plugin-sig:GbY7UGvgwpTKHoPZYEZisMKlAli8WZtlSeK5cLLTtoiFXtxfaUNg6JnpJ5DMoOI+Z28woOjepAswjiwc2D0LurQ8dVcu2ehr3ZIap8XsYNtr5rs0uWwGyujmpPWujd5vK0laxk/v4DoVXePSW8312KbzUPpGur6gRjOAe8wHrNOhUq5yW99WlGQFDeOzMqSW7p8TIFf7A3WqDIU0L1VvTLQBmCfVM5eZyed1bcs4WtykvJ05DeLi2Ov6qKJhm880tGsxxL9bNiWgeM/spPh9e1BMrNsTlVuI9xlYrlDJp9UiCTKufUVBqDsKldm5EV/0wK09b88UDKQdwY+VtIvBZQ==
"""
$description Global video hosting platform.
$url streamable.com
$type vod
"""

import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.http import HTTPStream
from streamlink.utils.url import update_scheme


@pluginmatcher(re.compile(
    r"https?://(?:www\.)?streamable\.com/(.+)",
))
class Streamable(Plugin):
    def _get_streams(self):
        data = self.session.http.get(self.url, schema=validate.Schema(
            re.compile(r"var\s*videoObject\s*=\s*({.*?});"),
            validate.none_or_all(
                validate.get(1),
                validate.parse_json(),
                {
                    "files": {
                        str: {
                            "url": validate.url(),
                            "width": int,
                            "height": int,
                            "bitrate": int,
                        },
                    },
                },
            ),
        ))

        for info in data["files"].values():
            stream_url = update_scheme("https://", info["url"])
            # pick the smaller of the two dimensions, for landscape v. portrait videos
            res = min(info["width"], info["height"])
            yield f"{res}p", HTTPStream(self.session, stream_url)


__plugin__ = Streamable
