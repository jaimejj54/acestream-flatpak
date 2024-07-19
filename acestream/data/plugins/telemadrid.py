#-plugin-sig:npNU6id32NM3E1abjCDSHvPWLnODYVguzgLk6EpsEJgXKiHQD7KgU5TRcEce9DDnKDPEtYJkOHuyDwr84pDVr4UGMoeiuJ0Yt1x6NXUICQWZgWx+xuvAAANtbWeYJtqVmeDmg7xWpAPEBtvx+YkJazpv+nVTYB9Bqf4nGqpRvBrahf2mrE+ZFgA7PHLwlMS5Ja7AV264W9JpNOZOHIw3KAJ/HMjxkOmgmhsUjlRo/l+Y9/lMBnbngpyHVd8Qt1Mq/CHUCoeBIY9bg327Ed0vZ45L1iBHS6LL93O+4fuWh/bOIo1RhEe9LOc7siPK/jhEITGduX4VApUwUmaMplAx8A==
"""
$description Spanish live TV channel for Telemadrid, a public regional television station.
$url telemadrid.es
$type live, vod
$region Spain
"""

import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.plugins.brightcove import BrightcovePlayer


@pluginmatcher(re.compile(
    r"https?://(?:www\.)?telemadrid\.es/",
))
class Telemadrid(Plugin):

    def _get_streams(self):
        data = self.session.http.get(self.url, schema=validate.Schema(
            validate.parse_html(),
            validate.xml_find(".//video[@class='video-js'][@data-video-id][@data-account][@data-player][1]"),
            validate.union_get("data-video-id", "data-account", "data-player"),
        ))
        data_video_id, data_account, data_player = data
        player = BrightcovePlayer(self.session, data_account, f"{data_player}_default")
        return player.get_streams(data_video_id)


__plugin__ = Telemadrid
