# import telepot

# token = "6076591511:AAHuGtWCzufAn2rLba3WzFKleqD8o8VmXl4"
# chat_id = "5955730862"
 
# bot = telepot.Bot(token=token)
# bot.sendMessage(chat_id=chat_id, text="윤수하이")

import telepot

telegram_token = "6076591511:AAHuGtWCzufAn2rLba3WzFKleqD8o8VmXl4"
telegram_chat_id ="5955730862"

bot = telepot.Bot(token=telegram_token)

def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == 'text':
        command = msg['text']
        if command == '/start':
            bot.sendMessage(chat_id=chat_id, text='안녕하세요! DataMate입니다 도시명을 입력해주세요 :)')
        
bot.message_loop(handle_message)

# 프로그램이 종료되지 않도록 유지합니다.
while True:
    pass
