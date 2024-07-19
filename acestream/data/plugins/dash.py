#-plugin-sig:n6Sujik7VnN+LAcL4M+K0PHYrFiCgtUv+69es5cjZGArfUVKCEmiQesqdVD+JiY41mTp9MGDdVj7oXXiDvAYePLJGlFp4wuhRoBxGu4L7/wI4J/O3hoxWQeHepK4ky5ApKNsc64Fc5R6uBH7tpNRFQ9mOtoMi9/+mcDVTclXjXXaRxulQ1fn3Zuw1VKRtsZK7+t1p04kd/o90XsLAGMQBgdqdXi1uL8SlF0NAj1pxB0aMho0DW9Bqz47yqgK6iwjfdziqdxRnR3erGzrErx7Rc0RrQ4UlaIQHaPqT+p3jZ87Ap562TG3GFplz3qcMAXEsNwsxW0hoJOtwyXXRVolkA==
import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.plugin import LOW_PRIORITY, parse_params, stream_weight
from streamlink.stream.dash import DASHStream
from streamlink.utils.url import update_scheme


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(
    r"dash://(?P<url>\S+)(?:\s(?P<params>.+))?$",
))
@pluginmatcher(priority=LOW_PRIORITY, pattern=re.compile(
    r"(?P<url>\S+\.mpd(?:\?\S*)?)(?:\s(?P<params>.+))?$",
))
class MPEGDASH(Plugin):
    @classmethod
    def stream_weight(cls, stream):
        match = re.match(r"^(?:(.*)\+)?(?:a(\d+)k)$", stream)
        if match and match.group(1) and match.group(2):
            weight, group = stream_weight(match.group(1))
            weight += int(match.group(2))
            return weight, group
        elif match and match.group(2):
            return stream_weight(f"{match.group(2)}k")
        else:
            return stream_weight(stream)

    def _get_streams(self):
        data = self.match.groupdict()
        url = update_scheme("https://", data.get("url"), force=False)
        params = parse_params(data.get("params"))
        log.debug(f"URL={url}; params={params}")

        return DASHStream.parse_manifest(self.session, url, **params)


__plugin__ = MPEGDASH
