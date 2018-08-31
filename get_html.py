

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
    return None

def download(queue):
    count = 1
    while True:
        if queue.empty():
            print("视频下载完毕")
            break
        url = queue.get()
        print("获取队列数据：",url)
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
                print("第", count, "个视频,正在下载...", c_fule_name + ".ts")
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
        count += 1
def queue_url(queue):
    #打开的文件必须存有m3u8文件地址
    #可手动修改
    with open("m3u8UI.txt",'r') as f:
        for url in f:
            queue.put(url.strip())
            time.sleep(0.2)

if __name__ == "__main__":
    print("程序运行当中，请不要进入下载视频的文件，避免程序中断。代码经过测试，视频下载无误。"
          "请等待下载完成后再进入文件夹，2s后视频程序开始执行")
    time.sleep(2)
    queue = multiprocessing.Manager().Queue()
    pool = Pool(3)
    print("数据加入队列中...")
    result = pool.apply_async(queue_url,(queue,))
    result.wait()
    print("数据加入队列完毕，开始准备下载...")
    pool.apply_async(download,(queue,))
    pool.close()
    pool.join()


































