import MyFileWorker
import DataWithBackupDumper
import logging
from datetime import datetime
import time
import PhrasesGenerator
import PhotosFromMessageGetter

NEXT_REMINDER = 720


class WithProblemsWorker:
    """
    Methods:
        update_problems_of_users()
        delete_user_problems(chat_id)
        change_problem_dict(chat_id, new_problem_dict, date_key)
        add_new_user(chat_id)
        add_new_problem(chat_id, new_problem_dict)
        get_problem_source_with_number(number)
        mark_problem_completed(message, number)
        get_new_problem(message)
        process_new_problem(message)
        start_get_photos(message, new_problem_dict)
        finish_process_new_problem(message, new_problem_dict)
        get_photos_list_with_mediagroupid(media_group_id)
        get_last_appeal_key(message)
    """

    def __init__(self, bot, temporary_values_keeper):
        self.problems_of_users = MyFileWorker.load_problems_of_users()
        self.next_reminder = NEXT_REMINDER
        self.temporary_values_keeper = temporary_values_keeper
        self.bot = bot

    def update_problems_of_users(self):
        """Loads problems from a json file into self.problems_of_users"""
        self.problems_of_users = MyFileWorker.load_problems_of_users()

    def delete_user_problems(self, chat_id):
        """Removes a user's problems from the database."""
        while chat_id in self.problems_of_users:
            print('tryd')
            self.problems_of_users.pop(chat_id)
            DataWithBackupDumper.dump_problems_of_users(self.problems_of_users)
            self.update_problems_of_users()

    def change_problem_dict(self, chat_id, new_problem_dict, date_key):
        """Overwrites the changed problems data in the problem dictionary."""
        while True:
            self.problems_of_users[chat_id][date_key] = new_problem_dict
            DataWithBackupDumper.dump_problems_of_users(self.problems_of_users)
            self.update_problems_of_users()
            if date_key in self.problems_of_users[chat_id]:
                break
            time.sleep(0.1)

    def add_new_user(self, chat_id):
        """Adds new user to problems_of_users."""
        while True:
            self.problems_of_users[chat_id] = {}
            DataWithBackupDumper.dump_problems_of_users(self.problems_of_users)
            self.update_problems_of_users()
            if chat_id in self.problems_of_users:
                break
            time.sleep(0.1)

    def add_new_problem(self, chat_id, new_problem_dict):
        """Adds a new problem dictionary to problems_of_users."""
        while True:
            date_key = datetime.today().strftime("%d.%m.%y %H:%M:%S")
            self.problems_of_users[chat_id][date_key] = new_problem_dict
            DataWithBackupDumper.dump_problems_of_users(self.problems_of_users)
            self.update_problems_of_users()
            if date_key in self.problems_of_users[chat_id]:
                break
            time.sleep(0.1)

    def get_problem_source_with_number(self, number):
        """Returns the path to the problem at a specific number"""
        self.update_problems_of_users()
        source_dict = None
        for chat_id in self.problems_of_users:
            for date_key in self.problems_of_users[chat_id]:
                if number == self.problems_of_users[chat_id][date_key]['number']:
                    source_dict = {"chat_id": chat_id, "date_key": date_key}
        return source_dict

    def mark_problem_completed(self, message, number):
        """Marks as solved a problem with a number."""
        source = self.get_problem_source_with_number(number)

        if source is not None:
            if not self.problems_of_users[source["chat_id"]][source["date_key"]]["issolved"]:
                new_problem_dict = self.problems_of_users[source["chat_id"]][source["date_key"]].copy()
                new_problem_dict["issolved"] = True
                self.change_problem_dict(source["chat_id"], new_problem_dict, source["date_key"])
                text = f"Заявка с номером {number} от {source['chat_id']} отмечена решённой"
                self.bot.send_message(str(message.chat.id), text)
                print(text)
                logging.info(text)
            else:
                self.bot.send_message(str(message.chat.id),
                                      "Заявка с номером " + str(number) + " уже была отмечена решённой.")

        else:
            self.bot.send_message(str(message.chat.id), "Такого номера заявки не существует.")
        self.temporary_values_keeper.temp_values["isDoneProcessPerforming"] = False

    def get_new_problem(self, message):
        """Entering the chain of receiving problem data from the user."""
        self.update_problems_of_users()
        self.bot.register_next_step_handler(
            self.bot.send_photo(str(message.chat.id), PhrasesGenerator.get_text_with_input_suggestion()[1],
                                PhrasesGenerator.get_text_with_input_suggestion()[0]),
            self.process_new_problem)

    def process_new_problem(self, message):
        """Processes the text of the problem (Possibly with photos) received from the user."""
        self.temporary_values_keeper.temp_values[str(message.chat.id)]["isGetMessageMethodPerforming"] = True
        if str(message.chat.id) in self.problems_of_users:
            print("Обрабатываем проблему, которую прислал пользователь")
            # If a type to be processed is received.
            if message.content_type == 'text' or message.content_type == 'photo' or message.content_type == 'document':
                new_problem_dict = {'issolved': False, "next_reminder": int(time.time() + self.next_reminder),
                                    "date": int(time.time())}

                if message.content_type == 'text':
                    mes_text = message.text
                else:
                    mes_text = message.caption

                if mes_text is not None:
                    new_problem_dict["text"] = mes_text
                else:
                    new_problem_dict["text"] = "Отсутствует"

                new_problem_dict["number"] = MyFileWorker.load_counter_of_orders()
                DataWithBackupDumper.dump_counter_of_orders(new_problem_dict["number"] + 1)
                self.start_get_photos(message, new_problem_dict)
            else:
                print(f"User {str(message.chat.id)} sent a message of an unprocessed type ({str(message.content_type)}) as a request ")
                logging.info(f"User {str(message.chat.id)} sent a message of an unprocessed type ({str(message.content_type)}) as a request ")
        else:
            self.bot.send_message(str(message.chat.id), PhrasesGenerator.get_text_about_deleted_data())
        self.temporary_values_keeper.temp_values[str(message.chat.id)]["isGetMessageMethodPerforming"] = False

    def start_get_photos(self, message, new_problem_dict):
        """Adds photos from the received message to the case, if any."""
        if message.content_type == 'photo' or message.content_type == 'document':
            photo_dict = PhotosFromMessageGetter.get_photo_from_message(self.bot, message)
            new_problem_dict['photos'] = [photo_dict]

        else:
            new_problem_dict["photos"] = []

        new_problem_dict['howPointsToSendToOperator'] = 3
        self.finish_process_new_problem(message, new_problem_dict)

    def finish_process_new_problem(self, message, new_problem_dict):
        self.add_new_problem(str(message.chat.id), new_problem_dict)

        self.bot.send_message(str(message.chat.id),
                              PhrasesGenerator.get_final_text_of_appeal(new_problem_dict["number"]))
        print(f"Problem added as number {new_problem_dict['number']} by user {message.chat.id}\n {new_problem_dict}")
        logging.info(
            f"Problem added as number {new_problem_dict['number']} by user {message.chat.id}\n {new_problem_dict}")

    def get_photos_list_with_mediagroupid(self, media_group_id):
        """Returns a list with a photo by media_group_id."""
        self.update_problems_of_users()
        source_dict = None
        for chat_id in self.problems_of_users:
            for date_key in self.problems_of_users[chat_id]:
                if 'photos' in self.problems_of_users[chat_id][date_key]:
                    for photo in self.problems_of_users[chat_id][date_key]['photos']:
                        if photo['media_group_id'] == media_group_id:
                            source_dict = {"chat_id": chat_id, "date_key": date_key}
                            return source_dict
        return source_dict

    def get_last_appeal_key(self, message):
        """Returns the key of the last problem added by the user."""
        self.update_problems_of_users()
        max_date = 0
        result = None
        for date_key in self.problems_of_users[str(message.chat.id)]:
            if self.problems_of_users[str(message.chat.id)][date_key]['date'] >= max_date:
                max_date = self.problems_of_users[str(message.chat.id)][date_key]['date']
                result = date_key
        return result
