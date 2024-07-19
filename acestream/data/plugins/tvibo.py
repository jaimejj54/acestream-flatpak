#-plugin-sig:UuKgsp/cZwWwfyoq/MvRuaNDN3qdLPF+ZrqW7Wmv25qxV97cXCPe9VxBCJtufMRBCp2dCkbvCxveQ80M/FhoAoGjwrYb404ZwSIBTQMp62GriAJUY1ek0Huo8dHPjt3lTBjfE9xKjwDbPS5zB8z4WAb2NtV7uC7kYtlmAIal0NYnZlETn++LLY9uKoAI3/pxy9aFZsY03GQpVlIhYgBxY+GfxJzMxdDgqAjZorKLU/JHCKPePWDMBBDGtPCk60bFkVArmFaHGlnCn5UZjmATFnHnt7JGH5hH5HwIUkRyG9sXuAtQGHYYVyEGktoW8/dfjdbqIK/8i+pnhIvA3XxLgw==
"""
$description Global live streaming and video hosting platform.
$url player.tvibo.com
$type live
"""

import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.stream.hls import HLSStream


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(
    r"https?://player\.tvibo\.com/\w+/(?P<id>\d+)",
))
class Tvibo(Plugin):
    _api_url = "http://panel.tvibo.com/api/player/streamurl/{id}"

    def _get_streams(self):
        channel_id = self.match.group("id")

        api_response = self.session.http.get(
            self._api_url.format(id=channel_id),
            acceptable_status=(200, 404))

        data = self.session.http.json(api_response)
        log.trace("{0!r}".format(data))
        if data.get("st"):
            yield "source", HLSStream(self.session, data["st"])
        elif data.get("error"):
            log.error(data["error"]["message"])


__plugin__ = Tvibo
