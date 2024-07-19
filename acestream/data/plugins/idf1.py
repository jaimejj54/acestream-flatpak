#-plugin-sig:E+xEgzjdOgzN8LPvp+m8AZNzQB/4Otdz4ZAEcjuMBKneC0hjnl8408IXWnhkUylqfqjSYDfOHpeaV+ZpLJmv9s9R3fZqlBH7u70mk7V5vO+cTDOxRRcyncBsjNj11fAVAABv/0TYEcBAIN6nHOzKr2v5OmPhQu7G88by09aHodOy7cW1RDL296z3QBsnEGlTaZ26YvtDf6CB/eb6a61duvWiYt6HiW1ZWUXz9a6yZf3BxB6vNA4kqNmCwIFEHR75O/0oxIj5XPfsCMY4zbfCyeMPfWAcRSy7NPrwI4W2uHPcbiEbGL3Z0OAZIjcCTW1PfytmHJfG9s8daUUCFeddkw==
"""
$description French live TV channel and video on-demand service owned by IDF1.
$url idf1.fr
$type live, vod
"""

import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(
    r"https?://www\.idf1\.fr/(videos/[^/]+/[^/]+\.html|live\b)",
))
class IDF1(Plugin):
    def _get_streams(self):
        self.id, self.title = self.session.http.get(
            self.url,
            schema=validate.Schema(
                validate.parse_html(),
                validate.union((
                    validate.xml_xpath_string(".//script[@class='dacast-video'][@id]/@id"),
                    validate.xml_xpath_string(".//head/title[1]/text()"),
                )),
            ),
        )

        if not self.id:
            return

        if re.match(r"\w+_\w+_\w+", self.id):
            provider = "dacast"
        else:
            provider = "universe"

        data = self.session.http.get(
            f"https://playback.dacast.com/content/access?contentId={self.id}&provider={provider}",
            acceptable_status=(200, 400, 403, 404),
            schema=validate.Schema(
                validate.parse_json(),
                validate.any(
                    {"error": str},
                    {"hls": validate.url()},
                ),
            ),
        )

        if data.get("error"):
            log.error(data["error"])
            return

        return HLSStream.parse_variant_playlist(self.session, data["hls"])


__plugin__ = IDF1
