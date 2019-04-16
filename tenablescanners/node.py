import logging
import json

import requests
import pandas as pd
from bs4 import BeautifulSoup

from minemeld.ft.basepoller import BasePollerFT

LOG = logging.getLogger(__name__)


class Miner(BasePollerFT):
    def configure(self):
        super(Miner, self).configure()

        self.polling_timeout = self.config.get('polling_timeout', 20)
        self.verify_cert = self.config.get('verify_cert', True)

        self.url = 'https://docs.tenable.com/cloud/Content/Scans/Scanners.htm'
        )

    def _build_iterator(self, item):
        # builds the request and retrieves the page
        rkwargs = dict(
            stream=False,
            verify=self.verify_cert,
            timeout=self.polling_timeout
        )

        r = requests.get(
            self.url,
            **rkwargs
        )

        try:
            r.raise_for_status()
        except:
            LOG.debug('%s - exception in request: %s %s',
                      self.name, r.status_code, r.content)
            raise

        # parse the page
        table = soup.find_all('table')[0]
        df = pd.read_html(str(table))[0]
        addresses = df[df.columns[1]].tolist()

        html_soup = BeautifulSoup(r.content, "lxml")
        table = html_soup.find_all('table')[0]
        df = pd.read_html(str(table))[0]
        result = df[df.columns[1]].tolist()

        return result

    def _process_item(self, item):

        #indicator = item
        value = {
            'type': 'IPv4',
            'confidence': 100
        }

        return [[item, value]]



