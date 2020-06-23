import subprocess
import paho.mqtt.client as mqtt
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

import line_info # LINEのアクセストークンの文字列

# LINEでメッセージ送信
def send_line_msg(msg):
    line_bot_api = LineBotApi(line_info.LINE_CHANNEL_ACCESS_TOKEN)
    line_bot_api.broadcast(TextSendMessage(text=msg))

# ブローカーに接続できたときの処理
def on_connect(client, userdata, flag, rc):
    #接続できたことを表示
    print('[mqtt_aircon_control.py] Connected with result code' + str(rc))
    #subscribeするトピックを表示
    client.subscribe('my_home/remote_control')

def on_disconnect(client, userdata, flags, rc):
    if rc != 0:
        print('[mqtt_aircon_control.py] Unexpected disconnection')

# メッセージが届いたときの処理
def on_message(client, userdata, msg):

    # メッセージ受け取り
    get_msg = msg.payload.decode('utf-8')

    # 信号送信処理
    if get_msg == 'on':
        subprocess.run(['python3', 'irrp.py', '-p', '-g17', '-f', 'codes', 'AC:on'])
        send_line_msg('エアコンon!')

    elif get_msg == 'off':
        subprocess.run(['python3', 'irrp.py', '-p', '-g17', '-f', 'codes', 'AC:off'])
        send_line_msg('エアコンoff')



#MQTTの接続設定
client = mqtt.Client()               # クラスのインスタンスを作成
client.on_connect = on_connect       # 接続時のコールバック関数を登録
client.on_disconnect = on_disconnect # 切断時のコールバック関数を登録
client.on_message = on_message       # メッセージ到着時のコールバック

client.username_pw_set("token:token_gFFITlJy7ptJtulK")
client.tls_set("/home/pi/develop/pi_remote_control/mqtt.beebotte.com.pem")
client.connect("mqtt.beebotte.com", 8883, 60)

send_line_msg('システム起動!')

client.loop_forever()
