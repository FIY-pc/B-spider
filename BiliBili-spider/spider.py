from symtable import Class

import requests
import datetime

from paramiko import agent

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
RESET = '\033[0m'

class Header:
    def __init__(self,user_agent,referer,cookie):
        self.user_agent = user_agent
        self.referer = referer
        self.cookie = cookie
    def Header(self)->dict:
        headers = {
            'user-agent': self.user_agent,
            'referer': self.referer,
            'cookie': self.cookie
        }
        return headers

class BiliBiliSpider:
    """
    BiliBili爬虫类，使用时必须传入Header参数，可以是Header实例调用Header方法生成的字典，也可以是自己按格式写的字典
    格式：headers: {'user-agent':"",'referer':"",'cookie':"",}
    """
    def __init__(self,headers):
        """
        :param headers: dict
        """
        self.headers = headers
    def Getavid(self,bvid:str)->int:
        """
        :param bvid: BiliBili视频的bvid，是一个字符串，可以点开视频，video/后面的一串神秘字母就是bvid，例：https://www.bilibili.com/video/abcdefg，这里的bvid就是abcdefg
        :return:
        """
        url = "https://api.bilibili.com/x/web-interface/view?bvid=" + bvid
        response = requests.get(url=url, headers=self.headers).json()
        data = response['data']
        avid = data['aid']
        return avid

    def VideoBasicInfoPrint(self,bvid:str):
        """
        :param bvid: BiliBili视频的bvid
        :return:
        """
        url = "https://api.bilibili.com/x/web-interface/view?bvid="+bvid
        response = requests.get(url=url,headers=self.headers).json()
        data = response['data']

        avid = data['aid']
        title = data['title']
        pubdate = datetime.datetime.fromtimestamp(data['pubdate'])
        owner = data['owner']
        ctime = datetime.datetime.fromtimestamp(data['ctime'])
        duration = data['duration']

        messages={
            "视频avid":avid,
            "视频标题":title,
            "Up主信息":owner,
            "视频投稿时间":ctime,
            "视频发表时间":pubdate,
            "视频时长":str(duration)+"秒"
        }

        for key,value in messages.items():
            print(key,":",value)

    def VideoCommentPrint(self,avid:str,like_limit:int=1000):
        """
        :param avid: BiliBili视频的avia，是一串数字，可以使用Getavid方法获取
        :param like_limit:
        :return:
        """
        url = "https://api.bilibili.com/x/v2/reply?type=1&sort=1&oid="+avid+"&pn="+str(1)
        response = requests.get(url=url,headers=self.headers).json()
        # 获取页数
        acount = response['data']['page']['acount']
        size = response['data']['page']['size']
        pages = int(acount/size)

        print(RED+"高赞评论:"+RESET)
        index = 1
        for i in range(1,pages+1):
            url = "https://api.bilibili.com/x/v2/reply?type=1&sort=2&oid=" + avid + "&pn=" + str(i)
            response = requests.get(url=url, headers=self.headers).json()
            for j in range(1,size):
                reply = response['data']['replies'][j]
                like = reply['like']
                if like >= like_limit:
                    content = reply['content']['message']
                    member = reply['member']

                    messages={
                        YELLOW+"序号"+RESET:index,
                        BLUE+"评论者昵称"+RESET:member['uname'],
                        BLUE+"评论赞数"+RESET:like,
                        BLUE+"评论内容"+RESET :content,
                    }

                    for key,value in messages.items():
                        print(key,":",value)
                    print("\n","-"*200,"\n")
                    index = index+1



if __name__ == '__main__':

    spider = BiliBiliSpider(headers)
    spider.VideoBasicInfoPrint("BV1aW411P7UJ")
    print("\n\n",'-'*200,"\n\n")
    spider.VideoCommentPrint("24149246")