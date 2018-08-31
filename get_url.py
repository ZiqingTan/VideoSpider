

import requests

from pyquery import PyQuery as pq
import re
"""
cookie 请手动修改，如果想获取其它专业视频的m3u8文件的话


"""
def get_page(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Cookie":".local.language=zh-CN; UM_distinctid=165794f125d60b-0650f2888991c8-43480420-1fa400-165794f125ea02; cloudAuthorityCookie=0; TMOOC-SESSION=6CD4F2CC368F4C79BC5EC6A0B0212A94; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1535366049,1535419695,1535431323,1535438117; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1535438117; sessionid=6CD4F2CC368F4C79BC5EC6A0B0212A94|498260906%40qq.com; versionListCookie=UIDTN201803; defaultVersionCookie=UIDTN201803; versionAndNamesListCookie=UIDTN201803N22NUI%25E8%25AE%25BE%25E8%25AE%25A1%25E5%25B8%2588%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV08; courseCookie=UID; stuClaIdCookie=591654; isCenterCookie=yes; Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1535422125,1535422994,1535431393,1535438147; JSESSIONID=9D118A7AD837337E71C89D71AFD486D4; Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1535438180"
    }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def get_url(text):
    doc  = pq(text)
    items = doc(".sp a").items()
    for item in items:
        yield item.attr("href")


def get_m3u8(reult):
    resp = re.compile("<p id=.*?active_.*?><a href=.*?\('(.*?)',this\)")
    pages = re.findall(resp,reult)
    if pages:
        for page in pages:
            url = "http://videotts.it211.com.cn/"
            m3u8 = url + str(page)[:-5] + "/" + str(page)
            yield m3u8
    

    

def main():
    url = "http://tts.tmooc.cn/studentCenter/toMyttsPage"
    text = get_page(url)
    html = get_url(text)
    for item in html:
        reult = get_page(item)
        m3u8s = get_m3u8(reult)
        for m3u8 in m3u8s:
            save_file(m3u8)
def save_file(m3):

    with open("m3u8UI.txt","a") as d:
        d.write(m3+"\n")
                
        
            
        



if __name__ == "__main__":
    main()
  
















    
