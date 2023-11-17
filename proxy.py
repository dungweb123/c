import re
import requests
import threading
import random

urls = '''
https://www.proxy-list.download/api/v1/get?type=http
https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all
https://raw.githubusercontent.com/casals-ar/proxy.casals.ar/main/http
https://raw.githubusercontent.com/andigwandi/free-proxy/main/proxy_list.txt
https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/http.txt
https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt
https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt
https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt
https://raw.githubusercontent.com/fahimscirex/proxybd/master/proxylist/http.txt
https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt
https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt
https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt
https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt
https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt
https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt
https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt
https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt
https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/http_proxies.txt
https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt
https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt
https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt
https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt
https://proxyspace.pro/http.txt
https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt
https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies_anonymous/http.txt
https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt
https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt
https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt
https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt
https://sunny9577.github.io/proxy-scraper/proxies.txt
https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt
https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt
https://raw.githubusercontent.com/ItzRazvyy/ProxyList/main/http.txt
https://raw.githubusercontent.com/ItzRazvyy/ProxyList/main/https.txt
https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt
https://raw.githubusercontent.com/Natthanon823/steam-account-checker/main/http.txt
https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt
https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt
https://api.proxyscrape.com/?request=displayproxies&proxytype=http
https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt
https://api.openproxylist.xyz/http.txt
https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt
https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt
https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt
https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt
https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt
https://raw.githubusercontent.com/RX4096/proxy-list/main/online/http.txt
https://raw.githubusercontent.com/RX4096/proxy-list/main/online/https.txt
https://raw.githubusercontent.com/saisuiu/uiu/main/free.txt
https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt
https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt
https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt
https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxy-list/data.txt
https://raw.githubusercontent.com/Zaeem20/FREE_PROXY_LIST/master/http.txt
https://raw.githubusercontent.com/Zaeem20/FREE_PROXY_LIST/master/https.txt
https://www.freeproxychecker.com/result/http_proxies.txt
https://www.proxy-list.download/api/v1/get?type=http
https://www.proxy-list.download/api/v1/get?type=https
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt

'''


user_agents = [
    "POLARIS/6.01(BREW 3.1.5;U;en-us;LG;LX265;POLARIS/6.01/WAP;)MMP/2.0 profile/MIDP-201 Configuration /CLDC-1.1",
    "POLARIS/6.01 (BREW 3.1.5; U; en-us; LG; LX265; POLARIS/6.01/WAP) MMP/2.0 profile/MIDP-2.1 Configuration/CLDC-1.1",
	"Opera/6.0 (Windows XP; U)  [de]",
	"Opera/6.0 (Windows ME; U)  [de]",
	"Opera/6.0 (Windows 2000; U)  [fr]",
	"Opera/6.0 (Windows 2000; U)  [de]",
	"Opera/6.0 (Macintosh; PPC Mac OS X; U)",
	"Mozilla/4.76 (Windows NT 4.0; U) Opera 6.0  [de]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows XP) Opera 6.0  [en]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows XP) Opera 6.0  [de]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows NT 4.0) Opera 6.0  [en]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows NT 4.0) Opera 6.0  [de]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows ME) Opera 6.0  [de]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows 98) Opera 6.0 [en]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows 98) Opera 6.0  [fr]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows 98) Opera 6.0  [en]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows 98) Opera 6.0  [de]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows 2000) Opera 6.0 [en]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows 2000) Opera 6.0  [en]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows 2000) Opera 6.0  [de]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Mac_PowerPC) Opera 6.0  [en]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Mac_PowerPC) Opera 6.0  [de]",
	"More Opera 6.0 user agents strings -->>",
	"Opera/5.12 (Windows NT 5.1; U)  [de]",
	"Opera/5.12 (Windows 98; U)  [en]",
	"Mozilla/5.0 (Windows 98; U) Opera 5.12  [de]",
	"Mozilla/4.76 (Windows NT 4.0; U) Opera 5.12  [en]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows NT 4.0) Opera 5.12  [de]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows ME) Opera 5.12  [it]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows ME) Opera 5.12  [de]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows 98) Opera 5.12  [it]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows 98) Opera 5.12  [en]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows 98) Opera 5.12  [de]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Mac_PowerPC) Opera 5.12  [en]",
	"Opera/5.11 (Windows 98; U)  [en]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows NT 4.0) Opera 5.11  [de]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows ME) Opera 5.11 [en]",
	"Opera/5.02 (Windows 98; U)  [en]",
	"Opera/5.02 (Macintosh; U; id)",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows NT 5.1) Opera 5.02  [en]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows NT 4.0) Opera 5.02  [en]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Windows 98) Opera 5.02  [en]",
	"Opera/5.0 (Ubuntu; U; Windows NT 6.1; es; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13",
	"Opera/5.0 (SunOS 5.8 sun4u; U)  [en]",
	"Mozilla/5.0 (SunOS 5.8 sun4u; U) Opera 5.0 [en]",
	"Mozilla/4.0 (compatible; MSIE 5.0; SunOS 5.8 sun4u) Opera 5.0  [en]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Mac_PowerPC) Opera 5.0  [en]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Linux) Opera 5.0  [en]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Linux 2.4.4-4GB i686) Opera 5.0  [en]",
	"Mozilla/4.0 (compatible; MSIE 5.0; Linux 2.4.0-4GB i686) Opera 5.0  [en]",
	"Opera/4.02 (Windows 98; U) [en]",
	"Mozilla/5.0 (Macintosh; ; Intel Mac OS X; fr; rv:1.8.1.1) Gecko/20061204 Opera",
	"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera",
	"Mozilla/4.0 (compatible; MSIE 6.0; Windows CE) Opera",
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
	"Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
	"Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
	"Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0",
	"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0",
	"Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0",
	"Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0",
	"Mozilla/5.0 (Windows NT 6.1; rv:27.3) Gecko/20130101 Firefox/27.3",
	"Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:27.0) Gecko/20121011 Firefox/27.0",
	"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0",
	"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0",
	"Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0",
	"Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/23.0",
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0",
	"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:23.0) Gecko/20131011 Firefox/23.0",
	"Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/22.0",
	"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0",
	"Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0",
	"Mozilla/5.0 (Microsoft Windows NT 6.2.9200.0); rv:22.0) Gecko/20130405 Firefox/22.0",
	"Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1",
	"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1",
	"Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:21.0.0) Gecko/20121011 Firefox/21.0.0",
	"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0",
	"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0",
	"Mozilla/5.0 (X11; Linux i686; rv:21.0) Gecko/20100101 Firefox/21.0",
	"Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20130514 Firefox/21.0",
	"Mozilla/5.0 (Windows NT 6.2; rv:21.0) Gecko/20130326 Firefox/21.0",
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/21.0",
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130331 Firefox/21.0",
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130330 Firefox/21.0",
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0",
	"Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130401 Firefox/21.0",
	"Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130328 Firefox/21.0",
	"Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0",
	"Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130401 Firefox/21.0",
	"Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130331 Firefox/21.0",
	"Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20100101 Firefox/21.0",
	"Mozilla/5.0 (Windows NT 5.0; rv:21.0) Gecko/20100101 Firefox/21.0",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0",
	"Mozilla/5.0 (Windows NT 6.2; Win64; x64;) Gecko/20100101 Firefox/20.0",
	"Mozilla/5.0 (Windows x86; rv:19.0) Gecko/20100101 Firefox/19.0",
	"Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20100101 Firefox/19.0",
	"Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/18.0.1",
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0)  Gecko/20100101 Firefox/18.0",
	"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6",
	"Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:17.0) Gecko/20100101 Firefox/17.0",
	"Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1",
	"Mozilla/5.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1",
	"Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1",
	"Mozilla/5.0 (X11; NetBSD amd64; rv:16.0) Gecko/20121102 Firefox/16.0",
	"Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.16) Gecko/20120427 Firefox/15.0a1",
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1",
	"Mozilla/5.0 (Windows NT 6.2; WOW64; rv:15.0) Gecko/20120910144328 Firefox/15.0.2",
	"Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1",
    "SAMSUNG-SGH-A867/A867UCHJ3 SHP/VPP/R5 NetFront/35 SMM-MMS/1.2.0 profile/MIDP-2.0 configuration/CLDC-1.1 UP.Link/6.3.0.0.0"]


file = open('proxy.txt', 'w')
file.close()
file = open('proxy.txt', 'a')
good_proxies = list()


def pattern_one(url):
    ip_port = re.findall('(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3}:\d{2,5})', url)
    if not ip_port: pattern_two(url)
    else:
        for i in ip_port:
            file.write(str(i) + '\n')
            good_proxies.append(i)


def pattern_two(url):
    ip = re.findall('>(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3})<', url)
    port = re.findall('td>(\d{2,5})<', url)
    if not ip or not port: pattern_three(url)
    else:
        for i in range(len(ip)):
            file.write(str(ip[i]) + ':' + str(port[i]) + '\n')
            good_proxies.append(str(ip[i]) + ':' + str(port[i]))


def pattern_three(url):
    ip = re.findall('>\n[\s]+(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3})', url)
    port = re.findall('>\n[\s]+(\d{2,5})\n', url)
    if not ip or not port: pattern_four(url)
    else:
        for i in range(len(ip)):
            file.write(str(ip[i]) + ':' + str(port[i]) + '\n')
            good_proxies.append(str(ip[i]) + ':' + str(port[i]))


def pattern_four(url):
    ip = re.findall('>(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3})<', url)
    port = re.findall('>(\d{2,5})<', url)
    if not ip or not port: pattern_five(url)
    else:
        for i in range(len(ip)):
            file.write(str(ip[i]) + ':' + str(port[i]) + '\n')
            good_proxies.append(str(ip[i]) + ':' + str(port[i]))


def pattern_five(url):
    ip = re.findall('(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3})', url)
    port = re.findall('(\d{2,5})', url)
    for i in range(len(ip)):
        file.write(str(ip[i]) + ':' + str(port[i]) + '\n')
        good_proxies.append(str(ip[i]) + ':' + str(port[i]))


def start(url):
    try:
        user_agent = random.choice(user_agents)
        req = requests.get(url, headers={'user-agent': user_agent}).text
        pattern_one(req)
        print(f'')
    except requests.exceptions.SSLError: print(str(url) + ' [x] SSL Error')
    except: print('')


threads = list()
for url in urls.splitlines():
    if url:
        x = threading.Thread(target=start, args=(url, ))
        x.start()
        threads.append(x)


for th in threads:
    th.join()
