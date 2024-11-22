from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    PushMessageRequest,
    BroadcastRequest,
    MulticastRequest,
    QuickReply,
    QuickReplyItem,
    TextMessage,
    Emoji,
    VideoMessage,
    AudioMessage,
    LocationMessage,
    StickerMessage,
    ImageMessage,
    TemplateMessage,
    ConfirmTemplate,
    ButtonsTemplate,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    MessageAction,
    URIAction,
    PostbackAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction
)
from linebot.v3.webhooks import (
    MessageEvent,
    FollowEvent,
    PostbackEvent,
    TextMessageContent
)
import os
app = Flask(__name__)

configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

#加入好友事件
@line_handler.add(FollowEvent)
def handle_follow(event):
    print(f'Got {event.type} event')

#訊息事件
@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

    if text == 'EEC錯誤':
            message_icon = request.url_root + 'static/message.png'
            message_icon = message_icon.replace("http", "https")            
            quickReply = QuickReply(
                items=[
                        QuickReplyItem(
                        action=MessageAction(
                            label="49408",
                            text="閘道器系統錯誤，請洽資訊人員處理"
                        )
                        # image_url=message_icon
                    ),
                        QuickReplyItem(
                        action=MessageAction(
                            label="49409",
                            text="封裝之CDA未符合公告之Schema"
                        )
                        # image_url=message_icon
                    ),
                         QuickReplyItem(
                        action=MessageAction(
                            label="49410",
                            text="封裝之CDA欄位缺少"
                        )
                        # image_url=message_icon
                    ),
                        QuickReplyItem(
                        action=MessageAction(
                            label="49411",
                            text="封裝之CDA無機構數位章"
                        )
                        # image_url=message_icon
                    ),
                        QuickReplyItem(
                        action=MessageAction(
                            label="49413",
                            text="缺少部分或所有影像，請先傳送影像後再傳送電子病歷影像報告"
                        )
                        # image_url=message_icon
                    )
                ]
             )

            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    #messages=[TextMessage(text=event.message.text)]
                        messages=[TextMessage(
                        text='請選擇錯誤代碼',
                        quick_reply=quickReply
                    )]
                )
            )
    elif text == '許願':
            url = 'https://generateimageapi20241121151339.azurewebsites.net/images/cae1f0b7-aba7-453d-9207-f8bcb8b9d2fd.png'
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(original_content_url=url, preview_image_url=url)
                    ]
                )
            )

if __name__ == "__main__":
    app.run()