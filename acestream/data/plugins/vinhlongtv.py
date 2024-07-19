#-plugin-sig:b4bxhA1LYNx8zz3BbSXnjacgKdBIjPOMxL7k064TMsZoR5Kcn8WW1/nQVJdV5DRAP1U0hiTF83fqM8eQLnPQdzb9AfwOvsw1bNs0e66rdtjof/czM5mlQZEJhCzWRQp9C5rvnpYKEnYy/TcbLrrKlo7pU9b0Yzc8hC6jWWxoeI3fkYc6V3qxIK+EzrrQslUy3hBA/Wckahhlfw9IfrhcxX0KzRtwMwpbx8JDHqRzDiswybVEMEKn2mu3dgbr3low9RJThGKK/sWu7gy2DP7ET5kWJJLS6w8oLOAPKTxLxz7CqqkuN5dnt99icxR66TxU//Otlg2FCoqriPDpab+lLA==
"""
$description Vietnamese live TV channels from THVL, including THVL1, THVL2, THVL3 and THVL4.
$url thvli.vn
$type live
$region Vietnam
"""

import logging
import re
from datetime import datetime, timezone
from hashlib import md5

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(
    r"https?://(?:www\.)?thvli\.vn/live/(?P<channel>[^/]+)",
))
class VinhLongTV(Plugin):
    _API_URL = "https://api.thvli.vn/backend/cm/get_detail/{channel}/"
    _API_KEY_DATE = "Kh0ngDuLieu"
    _API_KEY_TIME = "C0R0i"
    _API_KEY_SECRET = "Kh0aAnT0an"

    def _get_headers(self):
        now = datetime.now(tz=timezone.utc)
        date = now.strftime("%Y%m%d")
        time = now.strftime("%H%M%S")
        dtstr = f"{date}{time}"
        dthash = md5(dtstr.encode()).hexdigest()
        key_value = f"{dthash[:3]}{dthash[-3:]}"
        key_access = f"{self._API_KEY_DATE}{date}{self._API_KEY_TIME}{time}{self._API_KEY_SECRET}{key_value}"

        return {
            "X-SFD-Date": dtstr,
            "X-SFD-Key": md5(key_access.encode()).hexdigest(),
        }

    def _get_streams(self):
        channel = self.match.group("channel")
        params = {"timezone": "UTC"}
        headers = self._get_headers()

        self.id, self.title, hls_url = self.session.http.get(
            self._API_URL.format(channel=channel),
            params=params,
            headers=headers,
            schema=validate.Schema(
                validate.parse_json(),
                {
                    "id": str,
                    "title": str,
                    "link_play": str,
                },
                validate.union_get(
                    "id",
                    "title",
                    "link_play",
                ),
            ),
        )

        return HLSStream.parse_variant_playlist(self.session, hls_url)


__plugin__ = VinhLongTV
