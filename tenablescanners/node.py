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

        self.polling_timeout = self.config.get('polling_timeout', 30)
        self.verify_cert = self.config.get('verify_cert', True)
        self.url = self.config.get('url', 'https://docs.tenable.com/cloud/Content/Scans/Scanners.htm')
        self.table = self.config.get('table', 0)
        self.column = self.config.get('column', 1)

    def _build_iterator(self, item):
        # builds the request and retrieves the page
        rkwargs = dict(
            stream=False,
            verify=self.verify_cert,
            timeout=self.polling_timeout,
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
        LOG.info('nessuscanner table: %s - colmun: %s', self.table, self.column)
        # parse the table
        html_soup = BeautifulSoup(r.content, "lxml")
        table = html_soup.find_all('table')[self.table]
        df = pd.read_html(str(table))[self.table]
        result = df[df.columns[self.column]].tolist()
        result = ' '.join(result).split()
        return result

    def _process_item(self, item):

        #indicator = item
        value = {
            'type': 'IPv4',
            'confidence': 100
        }

        return [[item, value]]



