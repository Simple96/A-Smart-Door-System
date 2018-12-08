import itchat

@itchat.msg_register(itchat.content.TEXT)
def get_msg(msg):
    global status_flag
    if msg.text == 'no':
        status_flag = 0
        itchat.logout()
    if msg.text == 'yes':
        status_flag = 3
        itchat.logout()
    print msg.text

itchat.login.getQR(picDic = './qr.png')
#itchat.auto_login(hotReload = True)#, enableCmdQR = True
#itchat.getQR(picDic = './QR.png')
#itchat.login(picDir = './qr.png')
itchat.send('Hello', toUserName = 'filehelper')
itchat.send_image('./fog.png',toUserName = 'filehelper')
itchat.start_receiving()
itchat.run()