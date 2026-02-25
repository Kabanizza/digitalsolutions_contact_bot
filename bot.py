import telebot # type: ignore
from telebot import types


TOKEN = '8660550951:AAFSyV2YAF0WcadEEsbKvvfdQc3xym037H0'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Services 💼')
    btn2 = types.KeyboardButton('Contact Us 📞')
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, 
        "Hello! Welcome to Digital Solutions. How can we help your business today?", 
        reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Services 💼':
        bot.send_message(message.chat.id, 
            "Our Expertise:\n"
            "1. Web Development 🌐\n"
            "2. Business Automation ⚙️\n"
            "3. Smart Chatbots 🤖\n\n"
            "Tap 'Contact Us' to discuss your project!")
            
    elif message.text == 'Contact Us 📞':

        bot.register_next_step_handler(message, process_contact)
        
    else:
        bot.send_message(message.chat.id, "Please use the menu buttons below.")

def process_contact(message):

    request_text = message.text
    bot.send_message(message.chat.id, "Thank you! Your request has been received. We will be in touch soon.")
    print(f"Новая заявка от клиента: {request_text}")


print("Бот успешно запущен! Напиши ему /start в Telegram.")
bot.polling(none_stop=True)