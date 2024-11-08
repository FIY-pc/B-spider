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

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'referer': 'https://www.bilibili.com',
    'cookie': "buvid3=A23251E1-2EA9-BDA9-6A6F-292FE1BD971E51823infoc; b_nut=1730965251; _uuid=106883E7B-E8B2-9861-E69E-AFA2871B109DF52790infoc; CURRENT_FNVAL=4048; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzEyMjQ0NTMsImlhdCI6MTczMDk2NTE5MywicGx0IjotMX0._WcgxQMe2FCaXrwib5mANbUxnPIfIJO6YutLayT354Q; bili_ticket_expires=1731224393; buvid_fp=96480076448c300b6641ff40e6016fd1; buvid4=2D88C154-AC83-5F33-6452-4EA482710E8353269-024110707-dlMQ19Nmd0LIG7llyBF0dQ%3D%3D; rpdid=|(umJmYJmm)m0J'u~J|mYlklJ; SESSDATA=b91e4b57%2C1746517298%2Ca3f69%2Ab1CjCSn811yRrPU0d4uIgFdsUZ6iMnY_bcHaJgUoebmUz0vNWnSTNgulWnoEujPSXeEPcSVmFGLVNZd0kxSGF3LWdKRzRZZWVzZ0RXcFhRT2RnOG1aMjZMWXNUSXdvOEo2S2REZTk5ak1Lbkh3cUpaeFlENXJSdTFHQ3JQMW0zZDJiMXZYZF8zS3RnIIEC; bili_jct=352459a97484c9416aae523fda001548; DedeUserID=1071575921; DedeUserID__ckMd5=7d2f4ceb0476cb14; bp_t_offset_1071575921=996981558600531968; b_lsid=46F973610_193060CFC67; sid=4iaf6c4r"
}

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