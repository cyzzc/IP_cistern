from com.detect.proxynova_scraper import get_proxies, get_proxies_by_country
from com.other.log import log_ip
from com.pysqlit.py3 import insert_data


def get_proxynova(area="CN"):
    try:
        if area == ' ':
            proxies = get_proxies()
        else:
            proxies = get_proxies_by_country("CN")
        if len(proxies) <= 3:
            return get_proxynova(' ')
        for i in range(len(proxies)):
            insert_data(proxies[i].get('proxyIp') + ':' + proxies[i].get('proxyPort'),
                        proxies[i].get('proxyIp'),
                        int(proxies[i].get('proxyPort')), "HTTP",
                        proxies[1].get('proxyCountry'), 'filter')

    except Exception as e:
        log_ip("异常问题，com-->ipS-->get_proxynova.py: " + str(e))
