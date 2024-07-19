#-plugin-sig:SrUceIxAp0yG3MQJc/uU8dVqMc+tLOzHayxKwNp5tCBJTpj0+8YmHk7PlyATlwaC+VjNuybA80LN8GlJkjc/zgepjbnVkkszpFULhPTjR70o3txt8v48Qz6usyTdTbCuxFKp9ZlgkbapwnxBfAhi2xhvF9feeyp/EaYm9W4SnvegG2jMp8o/V8MJ14smrl0lh4f9tc4p1QzshXZGsvDuGDDVeAPcuva+BEOL67mJ2ENaqCTdrlYGADcL9raoEMAmAHRKbUY/Djy0JRMwYlSiBCXqC0cKUs8hc9OgcTVG6dWhVIKOuaEagMKlkPajIGjRxjfbzYaHkA0NEj0kRSEcsQ==
"""
$description French free-to-air news channel, providing 24-hour national and global news coverage.
$url cnews.fr
$type live, vod
"""

import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate


@pluginmatcher(re.compile(
    r"https?://(?:www\.)?cnews\.fr",
))
class CNEWS(Plugin):
    _dailymotion_url = "https://www.dailymotion.com/embed/video/{}"

    def _get_streams(self):
        data = self.session.http.get(self.url, schema=validate.Schema(
            re.compile(r"jQuery\.extend\(Drupal\.settings, ({.*})\);"),
            validate.none_or_all(
                validate.get(1),
                validate.parse_json(),
                {
                    validate.optional("dm_player_live_dailymotion"): {
                        validate.optional("video_id"): str,
                    },
                    validate.optional("dm_player_node_dailymotion"): {
                        validate.optional("video_id"): str,
                    },
                },
                validate.union_get("dm_player_live_dailymotion", "dm_player_node_dailymotion"),
            ),
        ))
        if not data:
            return

        live, node = data

        if node:
            return self.session.streams(self._dailymotion_url.format(node["video_id"]))
        elif live:
            return self.session.streams(self._dailymotion_url.format(live["video_id"]))


__plugin__ = CNEWS
