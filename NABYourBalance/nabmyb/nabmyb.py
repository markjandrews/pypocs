import sys
import time

import libmproxy
from libmproxy import proxy
from libmproxy.proxy import ProxyServer
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType

from .refererproxy import RefererMaster

proxy_address = '127.0.0.1'
proxy_port = 8888


def selenium_proxy():
    proxy_url = '{0}:{1}'.format(proxy_address, proxy_port)

    p = Proxy({'proxyType': ProxyType.MANUAL,
               'httpProxy': proxy_url,
               'ftpProxy': proxy_url,
               'sslProxy': proxy_url,
               'noProxy': 'localhost, 127.0.0.1'})

    return p


def main(argv=sys.argv[1:]):

    referer = 'http://www.nab.com.au/'

    port = proxy_port
    config = proxy.ProxyConfig(port=int(port))
    server = ProxyServer(config=config)
    m = RefererMaster(server, referer)
    m.run_async()

    driver = webdriver.Firefox(proxy=selenium_proxy())
    driver.get('https://www.nab.com.au/cgi-bin/ib/301_start.pl?browser=correct')
    try:
        print('Loading complete')
        time.sleep(30)
        print('Shutdown proxy server')
        m.shutdown_async()
    finally:
        driver.quit()
