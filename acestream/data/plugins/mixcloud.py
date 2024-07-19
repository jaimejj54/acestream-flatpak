#-plugin-sig:SiPVe8bFPJRU3jo99TDMHli3RqPZgMnUDViXC7dlGxLYW+R3SMn4XCilXVeNQlyQw+syvV7ExfSeYJyZdt1+MZyDD4qTy3SA7MfGWz26c6uQpQ150CZQzzOxENanr0GXNkAvuZna4+BmFWQ1I7USAoHjTBn0d3fxQloq64SPkwOAvrT3jx2ANFwhc/Ov8Z3G1z2G6lDVjQmCItRNGFbqibZfSWMdvK5bTUne5yL1x6sskq5fXUeb4Np7itA3eiiK/zU7D2whmmx6wM+5BBHG75pUvK8cMBSX1/U2TlxbkCei/46JI2tak75wkYV5CPaAeG+ijg8pjCbN2kY3ZsxzUw==
"""
$description British music live-streaming platform for radio shows and DJ mixes.
$url mixcloud.com
$type live
"""

import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(r"https?://(?:www\.)?mixcloud\.com/live/(?P<user>[^/]+)"))
class Mixcloud(Plugin):
    def _get_streams(self):
        data = self.session.http.post(
            "https://www.mixcloud.com/graphql",
            json={
                "query": """
                    query streamData($user: UserLookup!) {
                        userLookup(lookup: $user) {
                            id
                            displayName
                            liveStream(isPublic: false) {
                                name
                                streamStatus
                                hlsUrl
                            }
                        }
                    }
                """,
                "variables": {"user": {"username": self.match.group("user")}},
            },
            schema=validate.Schema(
                validate.parse_json(),
                {
                    "data": {
                        "userLookup": validate.none_or_all(
                            {
                                "id": str,
                                "displayName": str,
                                "liveStream": {
                                    "name": str,
                                    "streamStatus": validate.any("ENDED", "LIVE"),
                                    "hlsUrl": validate.none_or_all(validate.url()),
                                },
                            },
                        ),
                    },
                },
                validate.get(("data", "userLookup")),
            ),
        )
        if not data:
            log.error("User not found")
            return

        self.id = data.get("id")
        self.author = data.get("displayName")
        data = data.get("liveStream")

        if data.get("streamStatus") == "ENDED":
            log.info("This stream has ended")
            return

        self.title = data.get("name")

        if data.get("hlsUrl"):
            return HLSStream.parse_variant_playlist(self.session, data.get("hlsUrl"))


__plugin__ = Mixcloud
