from chatbot.workhandler import WorkChatApi, HandlerTool


class Sender(WorkChatApi):

    def __init__(self, corpid=None, corpsecret=None, agentid=None):
        self._Handler = HandlerTool(corpid, corpsecret, agentid)

    def get_token(self):
        '''
        获取token
        :return:
        '''
        return self._Handler.get_token()

    def send_text(self, message, users=None, **kwargs):
        '''
        发送text类型的消息,支持html标签展示
        :param message:  消息内容
        :param kwargs:  参考send_message函数入参
        :return:
        '''
        text_msg = {"content": message}

        self._Handler.send_message("text", text_msg, users=users, **kwargs)

    def send_image(self, iamgepath, users=None, **kwargs):
        """
        发送图片类型消息
        :param image: 图片ID
        :param kwargs: 参考send_message函数入参
        :return:
        """
        image_msg = {"media_id": iamgepath}
        self._Handler.send_message("image", image_msg, users=users, **kwargs)

    def send_voice(self, voicepath, users=None, **kwargs):
        """
        发送语音类型消息
        :param voicepath: 语音文件的路径
        :param users:  发送的用户
        :param kwargs: 参考send_message入参
        :return:
        """
        voice_msg = {"media_id": voicepath}
        self._Handler.send_message("voice", voice_msg, users=users, **kwargs)

    def send_video(self, videopath, title=None, desc=None, users=None, **kwargs):

        video_msg = {"media_id": videopath}

        if title:
            video_msg["title"] = title

        if desc:
            video_msg["description"] = desc

        self._Handler.send_message("video", video_msg, users=users, **kwargs)

    def send_file(self, filepath, users=None, **kwargs):
        """
        发送图片类型消息
        :param image: 图片ID
        :param kwargs: 参考send_message函数入参
        :return:
        """

        file_msg = {"media_id": filepath}

        self._Handler.send_message("file", file_msg, users=users, **kwargs)

    def send_textcard(self, cardtitle, desc, url, users=None, btn="详情", **kwargs):
        '''
        发送文本消息卡片
        :param cardtitle: 标题，不超过128个字节，超过会自动截断
        :param desc: 描述，不超过512个字节，超过会自动截断
        :param URL: 点击后跳转的链接。最长2048字节，请确保包含了协议头(http/https)
        :param btn: 按钮文字。 默认为“详情”， 不超过4个文字，超过自动截断。
        :param kwargs: 参考send_message函数入参
        :return:
        '''
        textcard_msg = {
            "title": cardtitle,
            "description": desc,
            "url": url,
            "btntxt": btn
        }
        self._Handler.send_message("textcard", textcard_msg, users, **kwargs)

    def send_graphic(self, cardtitle, desc, url, photourl, users=None, **kwargs):
        '''
        发送图文消息卡片
        :param cardtitle: 卡片标题
        :param desc:  卡片描述
        :param URL:  点击后跳转的链接
        :param photourl: 图片url
        :param kwargs: 参考send_message函数入参
        :return:
        '''
        graphic_msg = {"articles": [{
            "title": cardtitle,
            "description": desc,
            "url": url,
            "picurl": photourl
        }]}
        self._Handler.send_message("news", graphic_msg, users=users, **kwargs)

    def upload_image(self, photopath, enable=True):
        '''
        上传图片，返回图片url，url永久有效
        图片大小：图片文件大小应在 5B ~ 2MB 之间
        :param photopath:  图片路径
        :param enable:  是否开启记录上传图片返回的url
        :return: 图片url，永久有效
        '''

        image_url = self._Handler.upload_image(photopath, enable=enable)
        return image_url

    def get_usersid(self, departmentid=1, fetch_child=0):
        '''
        通过部门ID查询部门下的员工，默认根部门ID为1
        :param departmentid: 根部门ID
        :param fetch_child:  是否递归查询子部门员工
        :return:
        '''

        params = {"department_id": departmentid, "fetch_child": fetch_child}
        self._Handler.get_usersid(params)


if __name__ == '__main__':
    corpid = "XXXX"
    corpsecret = "XXXXX"
    agentid = 1
    app = Sender(corpid, corpsecret, agentid)
    # app.send_graphic("富婆新动态", "您的年轻富婆发布了新的照片", "http://www.zuoyazi.com.cn/",
    #                "https://wework.qpic.cn/wwpic/978819_WioVcFVxRhK8FbC_1628349205/0", "Zhuren")
    # app.send_text('测试新版', "ZhaoHeng")
    # app.send_image(r"G:\爬虫\chatbot\image\fupo1.JPG", "Zhuren")
    # app.send_video(r"G:\爬虫\chatbot\image\扭腰.mp4", users="Zhuren")
    # app.send_file(r"G:\爬虫\chatbot\image\Web前端开发规范手册.doc", users="Zhuren")
    # app.send_textcard("富婆任务通知",
    #                   "<div class=\"gray\">2021年10月24日</div>\n <div class= \"highlight\"> 您关注的富婆发布了最新的任务. </div>",
    #                   "http://www.zuoyazi.com.cn/", users="Zhuren")


