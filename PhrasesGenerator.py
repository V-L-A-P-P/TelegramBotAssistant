import MyFileWorker
import logging

logging.basicConfig(
    format='%(asctime)s: %(message)s',
    level=logging.INFO,
    filename='sample.log')
DATA_ITEMS = MyFileWorker.load_data_items_const()


def get_info_text_for_operator():
    text = "Вы определены как оператор\nВы будете уведомлены о новых обращениях."
    return text


def get_new_problem_text_for_operator(chat_id, date_key):
    """Generates and returns text to describe the new problem to the operator."""
    problems_of_users = MyFileWorker.load_problems_of_users()
    data_of_users = MyFileWorker.load_data_of_users()
    if chat_id in data_of_users and chat_id in problems_of_users:
        date_list = date_key.split(' ')
        text = date_list[0] + "\n" + date_list[1] \
               + "\nДобавлено новое обращение:\n" + "\n" \
               + "Номер заявки: " + str(problems_of_users[chat_id][date_key]['number']) \
               + "\nСотрудник :\n" \
               + data_of_users[chat_id]["firstname"] + " " + data_of_users[chat_id]["lastname"] \
               + "\nПодразделение: " + data_of_users[chat_id]["subdivision"] \
               + "\nАдрес почты: " + data_of_users[chat_id]["email"] \
               + "\nТелефон: " + data_of_users[chat_id]["phonenumber"] \
               + "\n\nТекст обращения:\n" \
               + problems_of_users[chat_id][date_key]["text"]
        return text
    else:
        return ""


def get_reminder_text(chat_id, date_key):
    """Generates and returns text to remind the operator of outstanding tasks."""
    problems_of_users = MyFileWorker.load_problems_of_users()
    data_of_users = MyFileWorker.load_data_of_users()
    if chat_id in data_of_users and chat_id in problems_of_users:
        date_list = date_key.split(' ')
        text = "Напоминаем, что до сих пор не решена проблема:  \n" \
               + date_list[0] + '\n' + date_list[1] + '\n' \
               + "Номер заявки: " + str(problems_of_users[chat_id][date_key]['number']) \
               + "\n\nСотрудник :\n" \
               + data_of_users[chat_id]["firstname"] + " " + data_of_users[chat_id]["lastname"] \
               + "\nПодразделение: " + data_of_users[chat_id]["subdivision"] \
               + "\nАдрес почты: " + data_of_users[chat_id]["email"] \
               + "\nТелефон: " + data_of_users[chat_id]["phonenumber"] \
               + "\n\nТекст обращения:\n" \
               + problems_of_users[chat_id][date_key]["text"]
        return text
    else:
        return ""


def get_hello_text_with_data(chat_id):
    """Generates and returns a welcome text if user data has already been received."""
    data_of_users = MyFileWorker.load_data_of_users()
    if chat_id in data_of_users:
        text = "Здравствуйте!\nВаши данные уже указаны:\n" + \
               data_of_users[chat_id][DATA_ITEMS[0]] + "\n" + \
               data_of_users[chat_id][DATA_ITEMS[1]] + "\n" + \
               data_of_users[chat_id][DATA_ITEMS[2]] + "\n" + \
               data_of_users[chat_id][DATA_ITEMS[3]] + "\n" + \
               data_of_users[chat_id][DATA_ITEMS[4]] + "\n"
        return text
    else:
        return ""


def get_hello_text_without_data():
    """Generates and returns a welcome text if user data has not yet been received."""
    text = "Здравствуйте!\nВам нужно указать свои данные: "
    return text


def get_final_text_of_appeal(number):
    """Generates and returns a text about the successful receipt of the problem."""
    text = f"Ваша заявка принята под номером {number}" \
           f" \nЕсли захотите обратиться еще раз, напишите что-нибудь в этот чат."
    return text


def get_text_with_input_suggestion():
    """Generates and returns text asking for a description of the problem."""
    text = "Подробно опишите вашу проблему:"
    photo = MyFileWorker.load_image("photo_instruction.jpg")
    return text, photo


def get_text_about_deleted_data():
    """Generates and returns a data reset notification text."""
    text = "Ваши данные были сброшены\n Чтобы зарегистрироваться, введите любое сообщение:"
    return text
