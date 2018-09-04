



import requests
import re, os, random
import datetime
from Crypto.Cipher import AES
from multiprocessing import Pool
import multiprocessing
from hashlib import md5
import time
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Origin': 'http://tts.tmooc.cn',
    'Referer': 'http://tts.tmooc.cn/video/showVideo?menuId=637841&version=AIDTN201805'
}
def get_tss_urls(url):
    html = requests.get(url, headers=headers)
    if html.status_code == 200:
        html = html.text
        pattern_key = re.compile('URI=\"(http://videotts.it211.com.cn/.*?/static.key)\"')
        pattern_urls = re.compile('http://videotts.it211.com.cn/.*?ts')
        ts_urls = re.findall(pattern_urls,html)
        key_url = re.findall(pattern_key,html)[0]
        key = requests.get(key_url,headers=headers).content
        return {
            'key': key,
            'ts_urls': ts_urls
        }
    return html.status_code
def download(url):
    if url:
        download_path = os.getcwd() + '\download'
        if not os.path.exists(download_path):
            os.mkdir(download_path)
        download_paths = os.path.join(download_path,"UI")
        if not os.path.exists(download_paths):
            os.mkdir(download_paths)
        dic = get_tss_urls(url)
        if dic:
            key = dic.get('key')
            c_fule_name = dic.get('ts_urls')[0].split('/')[-2]
            do_filed = download_paths + ("\\" + c_fule_name + ".ts")
            print("视频正在下载...", c_fule_name + ".ts")
            if not os.path.exists(do_filed):
                for ts_url in dic.get('ts_urls'):
                    res = requests.get(ts_url,headers=headers)
                    cryptor = AES.new(key, AES.MODE_CBC, key)
                    with open("{0}/{1}.{2}".format(download_paths,c_fule_name,"ts"),'ab') as f:
                        f.write(cryptor.decrypt(res.content))
                        f.close()
            else:
                print("视频已经下载过..")
                print("正在下下一个视频...")
        else:
            print("地址里没有视频!")
if __name__ == "__main__":
    pool = Pool(3)
    with open("m3u8UI.txt", 'r') as f:
        for url in f:
            result=pool.apply_async(download,(url.strip(),))
    result.wait()
    pool.close()
    pool.join()



































































