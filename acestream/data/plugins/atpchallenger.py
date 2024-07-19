#-plugin-sig:WDAGXXnsjNonOI1AjP0ziN4pL254HErVmiOZth03FoKsxHlUmKFbZ0a1whaNc2MJOxHSeCyF/Dt/6ufuOGHqomknp1gBC+jE0pDfBIkt/2NRTGN3blEYquN9y5cxKNOVJa4eseUIGYQ1M6lFbnE3/bkt+a1RTbXEF2cFaZTwFyZTT9defwjVDiMWU6oD4eksRhTaKeBBF7fD7nT9N6k+9pg1sYEmKw1elICFvr4dJ8J4+uB0cLvLpP1xpcvtgFpyd9QLrVIfzkh2UDjyC/6NoQfwy06NIP+vgkT8gWNfgiiJNNl/fzAbKWdrcdUHBmSR5dJaU3S9Bf4xf9FLovyTFg==
"""
$description Tennis tournaments organized by the Association of Tennis Professionals.
$url atptour.com/en/atp-challenger-tour/challenger-tv
$type live, vod
"""

import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate


@pluginmatcher(re.compile(
    r"https?://(?:www\.)?atptour\.com/(?:en|es)/atp-challenger-tour/challenger-tv",
))
class AtpChallengerTour(Plugin):
    def _get_streams(self):
        iframe_url = self.session.http.get(self.url, schema=validate.Schema(
            validate.parse_html(),
            validate.xml_xpath_string(".//iframe[starts-with(@id,'vimeoPlayer_')][@src][1]/@src"),
            validate.any(None, validate.url()),
        ))
        if iframe_url:
            return self.session.streams(iframe_url)


__plugin__ = AtpChallengerTour
