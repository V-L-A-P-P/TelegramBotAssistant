import MyFileWorker
import DataWithBackupDumper
import logging
import constants

logging.basicConfig(
    format='%(asctime)s: %(message)s',
    level=logging.INFO,
    filename='sample.log')
PERSONAL_DATA_ITEMS = constants.PERSONAL_DATA_ITEMS


class WithDataWorker:
    """
    Methods:
        get_new_user(message)
        change_user_dict(chat_id, user_dict)
        delete_user(chat_id)
        update_personal_users_data(self)
        process_new_user(message)
        get_firstname(message, new_user_dict)
        get_lastname(self, message, new_user_dict)
        get_subdivision(message, new_user_dict)
        get_email(message, new_user_dict)
        get_phone_number(message, new_user_dict)
        finish_process_new_user(message, new_user_dict)
    """

    def __init__(self, bot, temporary_values_keeper):
        self.personal_users_data = MyFileWorker.load_personal_users_data()  # Stores all personal data of users
        self.bot = bot
        self.temporary_values_keeper = temporary_values_keeper

    def get_new_user(self, message, add_user_to_problems_f, user_get_f=None):
        """
            Entering the chain of obtaining user data.
            (user_get_f - refers to get_new_problem method)
        """
        self.temporary_values_keeper.temp_values[str(message.chat.id)]['isGetUserDataPerforming'] = True
        self.temporary_values_keeper.temp_values['isGetUserDataPerforming'] = True
        self.process_new_user(message, add_user_to_problems_f, user_get_f)

    def change_user_dict(self, chat_id, user_dict):
        """Overwrites the changed data in the user's dictionary."""
        while True:
            self.personal_users_data[chat_id] = user_dict
            DataWithBackupDumper.dump_personal_users_data(self.personal_users_data)
            self.update_personal_users_data()
            if chat_id in self.personal_users_data:
                break
            time.sleep(0.1)

    def delete_user(self, chat_id):
        """Removes a user's dictionary from the database."""
        print("hah")
        while chat_id in self.personal_users_data:
            print("some")
            self.personal_users_data.pop(chat_id)
            DataWithBackupDumper.dump_personal_users_data(self.personal_users_data)
            self.update_personal_users_data()

    def update_personal_users_data(self):
        """Loads data from a json file into self.personal_users_data"""
        self.personal_users_data = MyFileWorker.load_personal_users_data()

    def process_new_user(self, message, add_user_to_problems_f, user_get_f=None):
        new_user_dict = {"deleted": False}
        self.bot.register_next_step_handler(self.bot.send_message(str(message.chat.id), "?????????????? ???????? ??????: "), self.get_firstname,
                                       new_user_dict, add_user_to_problems_f, user_get_f)
        print("???????? ??????")

    def get_firstname(self, message, new_user_dict, add_user_to_problems_f, user_get_f=None):
        if message.content_type != 'text':
            self.bot.register_next_step_handler(
                self.bot.send_message(str(message.chat.id), "??????????????, ????????????????????, ?????? ?? ?????????????????? ??????????????: "),
                self.get_firstname, new_user_dict, add_user_to_problems_f, user_get_f)
        else:
            print('??????:')
            print(message.text)

            new_user_dict[PERSONAL_DATA_ITEMS[0]] = message.text
            # time.sleep(1)
            self.bot.register_next_step_handler(
                self.bot.send_message(str(message.chat.id), "?????????????? ???????? ??????????????: "),
                self.get_lastname, new_user_dict, add_user_to_problems_f, user_get_f)

    def get_lastname(self, message, new_user_dict, add_user_to_problems_f, user_get_f=None):

        if message.content_type != 'text':
            print('???????????? ???? ??????????')
            self.bot.register_next_step_handler(
                self.bot.send_message(str(message.chat.id), "??????????????, ????????????????????, ?????????????? ?? ?????????????????? ??????????????: "),
                self.get_lastname, new_user_dict, add_user_to_problems_f, user_get_f)
        else:
            print('??????????????:')
            print(message.text)

            new_user_dict[PERSONAL_DATA_ITEMS[1]] = message.text
            self.bot.register_next_step_handler(
                self.bot.send_message(str(message.chat.id), "?????????????? ???????? ??????????????????????????:"), self.get_subdivision,
                new_user_dict, add_user_to_problems_f, user_get_f)

    def get_subdivision(self, message, new_user_dict, add_user_to_problems_f, user_get_f=None):
        if message.content_type != 'text':
            print('???????????? ???? ??????????')
            self.bot.register_next_step_handler(
                self.bot.send_message(str(message.chat.id),
                                 "??????????????, ????????????????????, ?????????????????????????? ?? ?????????????????? ??????????????:"),
                self.get_subdivision, new_user_dict, add_user_to_problems_f, user_get_f)
        else:

            print('??????????????????????????:')
            print(message.text)

            new_user_dict[PERSONAL_DATA_ITEMS[2]] = message.text
            self.bot.register_next_step_handler(
                self.bot.send_message(str(message.chat.id), "?????????????? ?????? ?????????? ?????????????????????? ??????????:"), self.get_email,
                new_user_dict, add_user_to_problems_f, user_get_f)

    def get_email(self, message, new_user_dict, add_user_to_problems_f, user_get_f=None):
        if message.content_type != 'text':
            print('???????????? ???? ??????????')
            self.bot.register_next_step_handler(self.bot.send_message(str(message.chat.id),
                                                            "??????????????, ????????????????????, ?????????? ?????????????????????? ?????????? "
                                                            "?? ?????????????????? ??????????????:"),
                                           self.get_email, new_user_dict, add_user_to_problems_f, user_get_f)
        elif '@' not in message.text or '.' not in message.text:
            self.bot.register_next_step_handler(self.bot.send_message(str(message.chat.id),
                                                            "??????????????, ????????????????????, ?????????? ?????????????????????? ?????????? "
                                                            "?? ???????????????????? ??????????????:"),
                                           self.get_email, new_user_dict, add_user_to_problems_f, user_get_f)
        else:

            print('??????????:')
            print(message.text)

            new_user_dict[PERSONAL_DATA_ITEMS[3]] = message.text
            self.bot.register_next_step_handler(
                self.bot.send_message(str(message.chat.id), "?????????????? ?????? ???????????????????? ?????????? ?????? ????????????????: "),
                self.get_phone_number, new_user_dict, add_user_to_problems_f, user_get_f)

    def get_phone_number(self, message, new_user_dict, add_user_to_problems_f, user_get_f=None):
        if message.content_type != 'text':
            self.bot.register_next_step_handler(self.bot.send_message(str(message.chat.id),
                                                            "??????????????, ????????????????????, ???????????????????? ?????????? ?? "
                                                            "?????????????????? ??????????????: "),
                                           self.get_phone_number, new_user_dict, add_user_to_problems_f, user_get_f)
        else:
            print('??????????:')
            print(message.text)
            new_user_dict[PERSONAL_DATA_ITEMS[4]] = message.text

            self.finish_process_new_user(message, new_user_dict, add_user_to_problems_f, user_get_f)

    def finish_process_new_user(self, message, new_user_dict, add_user_to_problems_f, user_get_f=None):
        print(f"User's personal data received ({str(message.chat.id)}):\n{str(new_user_dict)}")
        logging.info(f"User's personal data received ({str(message.chat.id)}):\n{str(new_user_dict)}")
        self.temporary_values_keeper.temp_values[str(message.chat.id)]['isGetUserDataPerforming'] = False
        self.temporary_values_keeper.temp_values['isGetUserDataPerforming'] = False
        self.change_user_dict(str(message.chat.id), new_user_dict)
        add_user_to_problems_f(str(message.chat.id))
        if user_get_f is not None:
            user_get_f(message)