#-plugin-sig:i8y/rlbDsJvSvdnmXYZYcFIviys29rAgiroS+AtCF+KtzgsS1y2Cc/W4F/v2KO9OrlQUYj2rHbHCPAy2SdeiYhohn3UxEIscNrFzPHvhVtzYqZx6OIWDavTztVWNgs4iBIGMDfBn68zNZmjDuY+5YjLk4rtaMX0VzlTfA9kC4fXLN3tRvLauFi6xSSVV+TXd6yvgdk9aPb+q63ECkZ8gEOz0dTMUfBfLMS9o03wHWGTVfQeIoEm4NYKrdiaGMLbfBoRF5Vvt/7nAJ1lSdM7w872AhRpUB2egKFIgcYFI4uV4zp4Vj9FvO4N9azA7vIz4xwEgIsP6gQS4q1kI5fMFug==
"""
$description Global live streaming platform for live video game broadcasts and individual live streams.
$url live.bigo.tv
$url bigoweb.co
$type live
"""

import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import useragents, validate
from streamlink.stream.hls import HLSStream


@pluginmatcher(re.compile(
    r"https?://(?:www\.)?bigo\.tv/([^/]+)$",
))
class Bigo(Plugin):
    _api_url = "https://www.bigo.tv/OInterface/getVideoParam?bigoId={0}"

    _video_info_schema = validate.Schema({
        "code": 0,
        "msg": "success",
        "data": {
            "videoSrc": validate.any(None, "", validate.url()),
        },
    })

    def _get_streams(self):
        res = self.session.http.get(
            self._api_url.format(self.match.group(1)),
            allow_redirects=True,
            headers={"User-Agent": useragents.IPHONE_6},
        )
        data = self.session.http.json(res, schema=self._video_info_schema)
        videourl = data["data"]["videoSrc"]
        if videourl:
            yield "live", HLSStream(self.session, videourl)


__plugin__ = Bigo
