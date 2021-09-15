from .workhandler import WorkChatApi, HandlerTool


class Sender(WorkChatApi):
    def __init__(self, corpid=None, corpsecret=None, agentid=None, **kwargs):
        self._Handler = HandlerTool(corpid, corpsecret, agentid, **kwargs)

    def get_token(self):
        """
        获取token
        :return: token
        """
        return self._Handler.get_token()

    def send_text(self, message, **kwargs):
        """
        发送文本消息，支持换行、以及A标签，大小最长不超过2048字节
        :param message:  消息内容
        :param kwargs:  可选择发送对象，tousers(用户), todept(部门), totags(标签用户). 默认为发送全部人
        """

        text_msg = {"content": message}
        self._Handler.send_message("text", text_msg, **kwargs)

    def send_image(self, iamge_path, **kwargs):
        """
        发送图片消息，仅支持jpg,png格式，大小5B~2M
        :param iamge_path: 发送图片的本地路径
        :param kwargs: 可选择发送对象，tousers(用户), todept(部门), totags(标签用户).
        """

        image_msg = {"media_id": iamge_path}
        self._Handler.send_message("image", image_msg, **kwargs)

    def send_voice(self, voice_path, **kwargs):
        """
        发送语音消息，仅支持amr格式，大小5B~2M
        :param voice_path: 发送语音文件的本地路径
        :param kwargs: 可选择发送对象，tousers(用户), todept(部门), totags(标签用户).
        :return:
        """

        voice_msg = {"media_id": voice_path}
        self._Handler.send_message("voice", voice_msg, **kwargs)

    def send_video(self, video_path, title=None, desc=None, **kwargs):
        """
        发送视频消息，仅支持MP4格式的视频消息，大小5B~10M
        :param video_path: 发送视频文件的本地路径
        :param title: 视频消息的标题，不超过128个字节，超过会自动截断.当不指定时默认为上传视频的文件名
        :param desc: 视频消息的描述，不超过512个字节，超过会自动截断
        :param kwargs: 可选择发送对象，tousers(用户), todept(部门), totags(标签用户).
        :return:
        """

        video_msg = {"media_id": video_path}

        if title:
            video_msg["title"] = title

        if desc:
            video_msg["description"] = desc

        self._Handler.send_message("video", video_msg, **kwargs)

    def send_file(self, file_path, **kwargs):
        """
        发送文件消息, 大小5B~10M
        :param file_path: 发送文件的本地路径
        :param kwargs: tousers(用户), todept(部门), totags(标签用户).
        :return:
        """

        file_msg = {"media_id": file_path}
        self._Handler.send_message("file", file_msg, **kwargs)

    def send_textcard(self, card_title, desc, link, btn="详情", **kwargs):
        """
        发送文本卡片消息
        :param card_title: 标题，不超过128个字节，超过会自动截断
        :param desc: 描述，不超过512个字节，超过会自动截断
        :param link: 点击后跳转的链接。最长2048字节，请确保包含了协议头(http/https)
        :param btn: 按钮文字。 默认为“详情”， 不超过4个文字，超过自动截断。
        :param kwargs: tousers(用户), todept(部门), totags(标签用户).
        :return:
        """

        textcard_msg = {
            "title": card_title,
            "description": desc,
            "url": link,
            "btntxt": btn
        }
        self._Handler.send_message("textcard", textcard_msg, **kwargs)

    def send_graphic(self, card_title, desc, link, image_link, **kwargs):
        """
        发送图文卡片消息
        :param card_title: 卡片标题
        :param desc:  卡片描述
        :param link:  点击后跳转的链接
        :param image_link: 图片url
        :param kwargs: tousers(用户), todept(部门), totags(标签用户).
        :return:
        """

        graphic_msg = {"articles": [{
            "title": card_title,
            "description": desc,
            "url": link,
            "picurl": image_link
        }]}
        self._Handler.send_message("news", graphic_msg, **kwargs)

    def upload_image(self, image_path, enable=True):
        """
        上传图片，返回图片链接，永久有效，主要用于图文消息卡片. imag_link参数
        图片大小：图片文件大小应在 5B ~ 2MB 之间
        :param image_path:  图片路径
        :param enable:  是否开启记录上传图片返回的url,会在当前文件夹下创建一个imagesList.txt.置为False 不持久化，默认True
        :return: 图片链接，永久有效
        """

        image_url = self._Handler.upload_image(image_path, enable=enable)
        return image_url

    def get_users_id(self, department_id=1, fetch_child=0):
        """
        通过部门ID查询部门下的员工
        :param department_id: 部门ID,默认根部门ID为1
        :param fetch_child:  是否递归查询子部门员工
        :return: 会显示所有的员工信息，主要用于查询对应用户的userid进行发送
        """

        params = {"department_id": department_id, "fetch_child": fetch_child}
        self._Handler.get_users_id(params)


