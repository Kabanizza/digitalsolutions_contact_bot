import os
import logging
import telebot
from telebot import types

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('BOT_TOKEN', '8660550951:AAFSyV2YAF0WcadEEsbKvvfdQc3xym037H0')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID', '') 

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

user_states = {}

def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("💼 Our Services", callback_data="menu_services"),
        types.InlineKeyboardButton("🌐 View Portfolio", url="https://github.com/your-portfolio"), 
        types.InlineKeyboardButton("📞 Request a Quote", callback_data="menu_contact")
    )
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "<b>Welcome to Kabanizza FlowPlace ✦</b>\n\n"
        "We elevate international brands through high-converting interfaces, "
        "sophisticated automated systems, and seamless custom integrations.\n\n"
        "<i>Please select an option below to proceed:</i>"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu())

@bot.callback_query_handler(func=lambda call: call.data.startswith('menu_'))
def handle_menu_callbacks(call):
    bot.answer_callback_query(call.id) 
    
    if call.data == "menu_services":
        text = (
            "<b>✦ Our Premium Services ✦</b>\n\n"
            "<b>1. Web Development</b>\n"
            "Immaculate, responsive, and blazing-fast architectures built to convert.\n\n"
            "<b>2. Business Automation</b>\n"
            "Bespoke Python engineering to automate complex operational workflows.\n\n"
            "<b>3. Smart Chatbots</b>\n"
            "Sophisticated Telegram integrations for elite customer support and lead capture."
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Return to Main Menu", callback_data="action_back"))
        bot.send_message(call.message.chat.id, text, reply_markup=markup)

    elif call.data == "menu_contact":
        msg = bot.send_message(
            call.message.chat.id, 
            "Let's build something great.\n\nPlease enter your <b>Full Name</b> to initiate the inquiry:"
        )
        bot.register_next_step_handler(msg, process_contact_name)

@bot.callback_query_handler(func=lambda call: call.data == "action_back")
def handle_back_action(call):
    bot.answer_callback_query(call.id)
    welcome_text = (
        "<b>Welcome back to Kabanizza FlowPlace ✦</b>\n\n"
        "<i>Please select an option below:</i>"
    )
    bot.send_message(call.message.chat.id, welcome_text, reply_markup=get_main_menu())

def process_contact_name(message):
    if message.text.startswith('/'):
        send_welcome(message)
        return

    user_states[message.chat.id] = {'name': message.text}
    
    msg = bot.send_message(
        message.chat.id, 
        f"Thank you, {message.text}. Now, please describe your <b>Project Requirements & Goals</b>:"
    )
    bot.register_next_step_handler(msg, process_contact_details)

def process_contact_details(message):
    if message.text.startswith('/'):
        send_welcome(message)
        return

    user_data = user_states.get(message.chat.id, {})
    name = user_data.get('name', 'Unknown')
    project_details = message.text
    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"

    confirmation_text = (
        "<b>✅ Inquiry Transmitted Successfully</b>\n\n"
        "Thank you for reaching out. Our lead engineer will review your requirements "
        "and contact you shortly."
    )
    bot.send_message(message.chat.id, confirmation_text, reply_markup=get_main_menu())

    logger.info(f"NEW INQUIRY | Name: {name} | User: {username} | Details: {project_details}")

    if ADMIN_CHAT_ID:
        try:
            admin_alert = (
                "<b>🚨 New Project Lead</b>\n\n"
                f"<b>Client Name:</b> {name}\n"
                f"<b>Telegram:</b> {username}\n"
                f"<b>Requirements:</b>\n{project_details}"
            )
            bot.send_message(ADMIN_CHAT_ID, admin_alert)
        except Exception as e:
            logger.error(f"Failed to alert admin: {e}")

    if message.chat.id in user_states:
        del user_states[message.chat.id]

if __name__ == '__main__':
    logger.info("Kabanizza FlowPlace Bot Initialization Sequence Started...")
    bot.infinity_polling(skip_pending=True)