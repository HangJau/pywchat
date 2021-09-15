# pychatbot
### 项目介绍

项目是根据企业微信可与微信进行互通的前提，通过操作企业微信的开放API达到将消息通知到微信.只封装了**微信能够接收的信息类型**以及上传临时素材等一些辅助接口. 
要使用该项目请先自己注册一个企业微信(无需认证) 注册文档

### 项目相关文档

​		**项目地址** ：https://github.com/HangJau/pywchat.git

​		**企业微信API**：[ 企业微信API (qq.com)](https://work.weixin.qq.com/api/doc/90000/90135/90236)

### 项目实现	

1. 已实现配置信息进行初始化.

2. 已实现对token的离线保存，以及token失效的自动获取.

3. 已实现对[text](#send_text)、[image](#send_image)、[voice](#send_voice)、[video](#send_video)、[file](#send_file)、[textcard](#send_textcard)、[graphic](#send_graphic)、[upload_image](#upload_image)、[get_user_id](#get_user_id)消息的发送封装.

4. 已实现对错误返回的处理.

  

### 项目下载		

```
pip install pychatbot	
```



### 三种初始化方法

    第一种：直接传入，只会在当前路径生成一个.token文件
    app = Sender(corpid,corpsecret,agentid)
    
    第二种：传入配置文件路径.读取配置并在当前路径生成一个.token文件(理论上文件也可无后缀且能读取成text即可，格式可参考配置介绍)
    app = Sender(path=r"G:\chat\conf.ini")
    
    第三种：不传任何参. 动态输入所需的corpid,corpsecret,agentid,并在当前路径生成一个.chatkey,.token两个文件
    app = Sender()


​    

### 配置介绍

    目前会有两个文件“ .chatkey” “ .token”
    .token: 保存获取到的token信息,保存在项目目录下
    .chatkey: 初始化的时候动态创建的配置文件，保存在项目目录下
    
    .token文件内容:
    [md5(corpid, corpsecret)]
    token=skdjwakljdslakjdw
    tokenout=1631451895
    
    .chatkey文件内容:
    [Chatinfo]
    corpid=dwajdlwajdlwa
    corpsecret=dsjdwaljfkleajdwa
    agentid=00001


​    

### 消息发送



#### <span id="send_text">send_text</span>

      发送纯文本消息，支持换行、以及A标签，大小最长不超过2048字节
      
      参数：
           message: 需要发送的消息
           kwargs:  可选择发送对象，tousers(用户), todept(部门), totags(标签用户)可同时填入,默认touser=@all
           
      例：
           app.send_text("又有一个富婆看了你的帅照啦..", touser="ZhuRen|user1")
           app.send_text("又有一个富婆看了你的帅照啦..", todept="1|2")
           app.send_text("又有一个富婆看了你的帅照啦..", totags="A")
      		
      tips:
      		默认为touser=@all, 发送全体用户，注意指定接收对象
      		接收的多个用户用 | 拼接

![send_text](https://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_msg$5bc63c26.png)



#### <span id="send_image">send_image</span>

      发送纯图片消息，仅支持jpg,png格式，大小5B~2M
      接收的多个用户用 | 拼接
      参数：
           iamge_path: 发送图片的本地路径
           kwargs:  可选择发送对象，tousers(用户), todept(部门), totags(标签用户)可同时填入,默认为发送全部人
    
      例：
           app.send_image(r"G:\caht\image.jpg", touser="ZhuRen|user1")
           app.send_image(r"G:\caht\image.jpg", todept="1|2")
           app.send_image(r"G:\caht\image.jpg", totags="A")
           
      tips:
      		默认为touser=@all, 发送全体用户，注意指定接收对象
      		接收的多个用户用 | 拼接


​         

#### <span id="send_voice">send_voice</span>

      发送语音消息，仅支持amr格式，大小5B~2M
      
      参数：
           voice_path: 发送语音文件的本地路径
           kwargs:  可选择发送对象，tousers(用户), todept(部门), totags(标签用户)可同时填入,默认为发送全部人
    
      例：
           app.send_voice(r"G:\caht\语音.amr", touser="ZhuRen|user1")
           app.send_voice(r"G:\caht\语音.amr", todept="1|2")
           app.send_voice(r"G:\caht\语音.amr", totags="A")
           
      tips:
      		默认为touser=@all, 发送全体用户，注意指定接收对象
      		接收的多个用户用 | 拼接



#### <span id="send_video">send_video</span>

      发送视频消息，仅支持MP4格式的视频消息，大小5B~10M
      
      参数：
           video_path: 发送视频文件的本地路径
           kwargs:  可选择发送对象，tousers(用户), todept(部门), totags(标签用户)可同时填入,默认为发送全部人
    
      例：
           app.send_video(r"G:\caht\视频.mp4", touser="ZhuRen|user1")
           app.send_video(r"G:\caht\视频.MP4", todept="1|2")
           app.send_video(r"G:\caht\视频.mp4", totags="A")
           
      tips:
      		默认为touser=@all, 发送全体用户，注意指定接收对象
      		接收的多个用户用 | 拼接

![send_video](https://p.qpic.cn/pic_wework/3478722865/9d9b75910515dfd9064947d1d95e8dd7892670895ddfc0f3/0)



#### <span id="send_file">send_file</span>

      发送文件消息, 大小5B~10M
      
      参数：
           file_path: 发送文件的本地路径
           kwargs:  可选择发送对象，tousers(用户), todept(部门), totags(标签用户)可同时填入,默认为发送全部人
    
      例：
           app.send_file(r"G:\caht\富婆联系表.xlsx", touser="ZhuRen|user1")
           app.send_file(r"G:\caht\富婆联系表.xlsx", todept="1|2")
           app.send_file(r"G:\caht\富婆联系表.xlsx", totags="A")
           
      tips:
      		默认为touser=@all, 发送全体用户，注意指定接收对象
      		接收的多个用户用 | 拼接

![send_file](http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/filemsg.jpeg)



#### <span id="send_textcard">send_textcard</span>

      发送文字卡片消息，点击卡片后跳转到设定的链接
      
      参数：
           card_title: 标题，不超过128个字节，超过会自动截断
           desc: 描述，不超过512个字节，超过会自动截断
           link: 点击后跳转的链接。最长2048字节，请确保包含了协议头(http/https)
           btn: 按钮文字。 默认为“详情”， 不超过4个文字，超过自动截断.
           kwargs: 可选择发送对象，tousers(用户), todept(部门), totags(标签用户)可同时填入,默认为发送全部人
       
      例：
           app.send_textcard("富婆任务通知", "2021年10月24日\n您关注的富婆发布了最新的任务.","https://www.RichWoman.com/task/1",touser="ZhuRen")
           
           app.send_textcard("富婆任务通知", "2021年10月24日\n您关注的富婆发布了最新的任务.","https://www.RichWoman.com/task/1",todept="1|2")
           
           app.send_textcard("富婆任务通知", "2021年10月24日\n您关注的富婆发布了最新的任务.","https://www.RichWoman.com/task/1",totags="A")
      
      tips:
      		默认为touser=@all, 发送全体用户，注意指定接收对象
      		接收的多个用户用 | 拼接

![send_textcard](http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/cardmsg.jpeg)



#### <span id="send_graphic">send_graphic</span>

```
  发送图文卡片消息，点击卡片后跳转到设定的链接
  
  参数：
       cardtitle: 标题，不超过128个字节，超过会自动截断
       desc: 描述，不超过512个字节，超过会自动截断
       link: 点击后跳转的链接。最长2048字节，请确保包含了协议头(http/https)
       image_link: 卡片中显示图片的url.如何获取参考(upload_iamge)
       kwargs: 可选择发送对象，tousers(用户), todept(部门), totags(标签用户)可同时填入,默认为发送全部人
       
  例：
       app.send_graphic("富婆动态通知", "您关注的富婆发布了最新的照片.", "https://www.RichWoman.com/dynamic/1/", "https://www.RichWoman.com/dynamic/1/photos/fp.jpg", touser="ZhuRen|user1")
       app.send_graphic("富婆动态通知", "您关注的富婆发布了最新的照片.", "https://www.RichWoman.com/dynamic/1/", "https://www.RichWoman.com/dynamic/1/photos/fp.jpg", todeot="1|2")
       app.send_graphic("富婆动态通知", "您关注的富婆发布了最新的照片.", "https://www.RichWoman.com/dynamic/1/", "https://www.RichWoman.com/dynamic/1/photos/fp.jpg", totags="A")
   
   tips:
  		默认为touser=@all, 发送全体用户，注意指定接收对象
  		接收的多个用户用 | 拼接
```

![send_graphic](https://p.qpic.cn/pic_wework/3478722865/7a7c92760b2bd396e3b856a660f43c8b7db11271bddb3f34/0)



#### <span id="upload_image">upload_image</span>

      上传图片，返回图片链接，永久有效，主要用于图文消息卡片imag_link参数
      图片大小：图片文件大小应在 5B ~ 2MB 之间
      
      参数：
           image_path: 发送图片的本地路径
           enable: 是否开启记录上传图片返回的url,会在当前文件夹下创建一个imagesList.txt。 置为False不持久化.默认True
      
      例：
           image_url = app.upload_image(r"C:\\photo\boy.jpg")
           print(image_url)
           
      tips:
      		多次上传同一图片会返回不同的地址且永久保存，希望大家还是只上传一次记录返回的url备用。
      		默认为touser=@all, 发送全体用户，注意指定接收对象
      		接收的多个用户用 | 拼接



#### <span id="get_user_id">get_user_id</span>   

      通过部门id获取部门下的员工信息
    
    参数：
           departmentid: 部门id.根部门默认为 1
           fetch_child: 是否递归子部门下的员工信息，默认为0，不递归
      
      例：
           get_userid(1)
           
      tips:
      		该方法只输出不进行返回.
      		默认为touser=@all, 发送全体用户，注意指定接收对象
      		接收的多个用户用 | 拼接





