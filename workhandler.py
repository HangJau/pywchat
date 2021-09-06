import json
import time
import hashlib
from abc import ABC, abstractmethod
from pathlib import Path
import logging
import inspect
import configparser
from chatbot.chatapi import chat_api
import requests
import os


class WorkChatApi(ABC):
    """
    接口类，定义所有的接口
    """

    @abstractmethod
    def get_token(self, *args, **kwargs):
        pass

    @abstractmethod
    def send_text(self, *args, **kwargs):
        pass

    @abstractmethod
    def send_image(self, *args, **kwargs):
        pass

    @abstractmethod
    def send_voice(self, *args, **kwargs):
        pass

    @abstractmethod
    def send_video(self, *args, **kwargs):
        pass

    @abstractmethod
    def send_file(self, *args, **kwargs):
        pass

    @abstractmethod
    def send_textcard(self, *args, **kwargs):
        pass

    @abstractmethod
    def send_graphic(self, *args, **kwargs):
        pass

    @abstractmethod
    def upload_image(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_usersid(self, *args, **kwargs):
        pass


tokenp = Path.cwd().joinpath(".token.conf")


class HandlerTool:
    """
    处理类，封装请求，处理请求以及请求闭环。为上层接口提供处理逻辑
    """

    def __init__(self, corpid, corpsecret, agentid):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self._op = hashlib.md5(bytes(self.corpsecret + self.corpid, encoding='utf-8')).hexdigest()
        self.token = None
        self.conf = configparser.ConfigParser()
        self.url = 'https://qyapi.weixin.qq.com'

    @staticmethod
    def is_image(file):

        if not (file.suffix in (".JPG", ".PNG", ".jpg", ".png") and (5 <= file.stat().st_size <= 2 * 1024 * 1024)):
            raise TypeError({"Code": "ERROR", "message": '图片文件不合法, 请检查文件类型(jpg, png, JPG, PNG)或文件大小(5B~2M)'})

    @staticmethod
    def is_voice(file):

        if not (file.suffix in (".AMR", ".amr") and (5 <= file.stat().st_size <= 2 * 1024 * 1024)):
            raise TypeError({"Code": "ERROR", "message": '语音文件不合法, 请检查文件类型(AMR, amr)或文件大小(5B~2M)'})

    @staticmethod
    def is_video(file):

        if not (file.suffix in (".MP4", ".mp4") and (5 <= file.stat().st_size <= 10 * 1024 * 1024)):
            raise TypeError({"Code": "ERROR", "message": '视频文件不合法, 请检查文件类型(MP4, mp4)或文件大小(5B~10M)'})

    @staticmethod
    def is_file(file):
        if not (file.is_file() and (5 <= file.stat().st_size <= 10 * 1024 * 1024)):
            raise TypeError({"Code": "ERROR", "message": '普通文件不合法, 请检查文件类型或文件大小(5B~10M)'})

    def file_check(self, filetype, path):
        """
        验证上传文件是否符合标准
        :param filetype: 文件类型(image,voice,video,file)
        :param path:
        :return:
        """

        p = Path(path)
        filetypes = {"image": self.is_image, "voice": self.is_voice, "video": self.is_video, "file": self.is_file}

        try:

            chack_type = filetypes.get(filetype, None)

            if not chack_type:
                raise TypeError({"Code": 'ERROR', "message": '不支持的文件类型，请检查文件类型(image,voice,video,file)'})
            chack_type(p)

            return {"file": (p.name, p.read_bytes())}

        except TypeError as e:
            print(e)
            exit()

    def _get(self, uri, **kwargs):
        """
        发起get请求
        :param uri: 需要请求的Url
        :param kwargs: 需要带入的参数
        :return:
        """
        try:
            rsp = requests.get(self.url + uri, **kwargs)
            rsp.raise_for_status()
            return rsp.json()
        except requests.RequestException as e:
            return e

    def _post(self, uri, **kwargs):
        """
        发起Post请求
        :param uri: 需要请求的Url
        :param kwargs: 请求所需的参数
        :return:
        """
        try:
            self.get_token()
            requrl = self.url + uri
            for i in range(2):
                rsp = requests.post(requrl.format(self.token), **kwargs)
                rsp.raise_for_status()
                result = rsp.json()

                if result.get("errcode") == 0:
                    print("消息发送成功")
                    return result

                elif result.get("errcode") == 42001 or result.get("errcode") == 40014:
                    self.get_token()

                else:
                    print(f'消息发送失败！原因:{rsp}')
                    break

        except requests.exceptions.HTTPError as httperror:
            raise requests.exceptions.HTTPError(
                f"发送失败， HTTP error:{httperror.response.status_code} , 原因: {httperror.response.reason}")

        except requests.exceptions.ConnectionError:
            raise requests.exceptions.ConnectionError("发送失败，HTTP connection error!")

        except requests.exceptions.Timeout:
            raise requests.exceptions.Timeout("发送失败，Timeout error!")

        except requests.exceptions.RequestException:
            raise requests.exceptions.RequestException("发送失败, Request Exception!")

    def _writ_token(self, type, txt, path):
        """
        持久化token
        :param type: ini 文件中的父索引
        :param txt: 写入的数据信息
        :param path: 文件保存的目录
        :return:
        """
        try:
            self.conf[type] = txt
            with open(path, "w", encoding='utf-8') as fp:
                self.conf.write(fp)
                print('token 写入成功')
        except Exception as e:
            print(e)
            exit()

    # def _check_token(self):
    #     """
    #     确认本地token时限，以及判断本地是否存在token文件没有则自动获取
    #     :return:
    #     """
    #
    #     if not (self.corpid and self.corpsecret and self.agentid):
    #         raise IOError("未传入corpid, corpsecret, agentid")
    #
    #     if not self.conf.has_section('AccessToken') or int(time.time()) > int(
    #             self.conf.get("AccessToken", "timeout")):
    #         self.token = self.get_token()
    #     else:
    #         self.token = self.conf.get("AccessToken", "token")

    def get_token(self):
        """
        获取token
        :return:
        """

        # 先读文件如果没有就发起请求并写入文件返回，有就判断timeout失效就发起请求并写入文件返回，时效正常直接返回

        if tokenp.is_file():
            self.conf.read(tokenp, encoding="utf-8")
            try:
                if int(time.time()) > int(self.conf.get(self._op, "tokenout")):
                    gettoken_url = chat_api.get("GET_ACCESS_TOKEN").format(self.corpid, self.corpsecret)
                    rsp = self._get(gettoken_url)
                    tokeninfo = {"token": rsp.get("access_token"),
                                 "tokenout": str(int(time.time()) + rsp.get("expires_in"))}
                    self._writ_token(self._op, tokeninfo, tokenp)
                    self.token = rsp.get("access_token")
                    return rsp.get("access_token")
                return self.conf.get(self._op, "token")

            except configparser.NoSectionError:
                print({"Code": 'ERROR', "message": '未读取到 {} 请检查token文件是否存在该节点'.format(self._op)})

            except configparser.NoOptionError:
                print({"Code": 'ERROR', "message": f'未读取到 tokenout 请检查 {self._op} 节点下是否存在tokenout'})

        else:

            access_token = chat_api.get("GET_ACCESS_TOKEN").format(self.corpid, self.corpsecret)
            rsp = self._get(access_token)
            tokeninfo = {"token": rsp.get("access_token"), "tokenout": str(int(time.time()) + rsp.get("expires_in"))}
            self._writ_token(self._op, tokeninfo, tokenp)
            self.token = rsp.get("access_token")
            return rsp.get("access_token")

    def send_message(self, msgtype, message, users=None, departments=None, tags=None):
        """

        :param msgtype:
        :param message:
        :param users:
        :param departments:
        :param tags:
        :return:
        """
        data = {
            "msgtype": msgtype,
            "agentid": self.agentid,
            msgtype: message
        }

        if users:
            data["touser"] = users

        if departments:
            data["toparty"] = departments

        if tags:
            data["totag"] = tags

        # 判断是否需要上传
        if msgtype in ("image", "voice", "video", "file"):
            filepath = message.get("media_id")

            media_id = self.upload_media(msgtype, filepath)
            message["media_id"] = media_id

        self._post(chat_api.get('MESSAGE_SEND'), data=json.dumps(data))

    def upload_media(self, filetype, path):
        '''
        上传临时素材
        :return:
        '''

        fileinfo = self.file_check(filetype, path)
        rsp = self._post(chat_api.get("MEDIA_UPLOAD").format("{}", filetype), files=fileinfo)
        return rsp.get("media_id")

    def upload_image(self, photopath, enable=True):
        '''
        上传图片，返回图片url，url永久有效
        图片大小：图片文件大小应在 5B ~ 2MB 之间
        :param photopath:  图片路径
        :param enable:  是否开启上传记录

        :return: 图片url，永久有效
        '''

        p_imag = Path(photopath)

        if not p_imag.is_file() or p_imag.stat().st_size > 2 * 1024 * 1024 or p_imag.stat().st_size <= 5:
            raise TypeError({"error": '404', "message": '指向的文件不是一个正常的图片或图片大小未在5B ~ 2MB之间',
                             "massage": f"{p_imag.name}: {p_imag.stat().st_size} B"})
        files = {"file": p_imag.read_bytes(), "filename": p_imag.name}

        rsp = self._post(chat_api.get("IMG_UPLOAD"), files=files)
        if enable:
            with open('./imagesList.txt', "a+", encoding='utf-8') as fp:
                fp.write(f"{p_imag.name}: {rsp.get('url')}")

        return rsp.get("url")

    # def get_usersid(self, data):
    #
    #
    #
    #     data["access_token"] = self.token
    #
    #     rsp_users = self._get(chat_api.get('GET_USERS'), params=data)
    #
    #     for i in rsp_users.get("userlist"):
    #         print(i)


if __name__ == '__main__':
    # HandlerTool().upload_media(r"\work_chat\image\girl.jpg")
    # HandlerTool.is_image()
    # HandlerTool.is_image()
    print(Path.cwd().joinpath("token.json"))
    # app.get_token()
    # app._check_token()
