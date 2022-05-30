import logging
import PhrasesGenerator
import ToOperatorByEmailSender
import ToOperatorByTelegramSender
import MyFileWorker
import time
import constants

logging.basicConfig(
    format='%(asctime)s: %(message)s',
    level=logging.INFO,
    filename='sample.log')

OPERATOR_DATA = MyFileWorker.load_data_of_operator()
NEXT_REMINDER = constants.NEXT_REMINDER



class BackgroundProcessPerformer:
    def __init__(self, bot, with_data_worker, with_problems_worker, temporary_values_keeper):
        self.with_data_worker = with_data_worker
        self.with_problems_worker = with_problems_worker
        self.operator_data_list = OPERATOR_DATA
        self.operator_id = self.operator_data_list["chat_id"]
        self.next_reminder = NEXT_REMINDER
        self.temporary_values_keeper = temporary_values_keeper
        self.bot = bot

    def do_background_process(self):
        """
          The method runs constantly in the background.
          It happens in it:
              Sending notifications to the operator about outstanding tasks.
              Sending new problems to the operator.
              tracking changes in task status.
        """
        print("Запуск фонового процесса")

        while True:
            time.sleep(1)
            if not self.temporary_values_keeper.temp_values['isGetMessageMethodPerforming']:
                self.with_problems_worker.update_problems_of_users()
                self.with_data_worker.update_personal_users_data()

                # If operator details are not specified.
                if self.operator_id == "":

                    print("Введите данные оператора в приложении")
                else:

                    for chat_id in list(self.with_problems_worker.problems_of_users):

                        if self.with_data_worker.personal_users_data[chat_id]['deleted']:
                            print(f"The operator deleted the user {chat_id} from the database")
                            logging.info(f"The operator deleted the user {chat_id} from the database")
                            self.with_data_worker.delete_user(chat_id)
                            self.with_problems_worker.delete_user_problems(chat_id)

                        elif (chat_id in self.temporary_values_keeper.temp_values) == False or (
                                self.temporary_values_keeper.temp_values[chat_id]["isGetMessageMethodPerforming"] == False and
                                self.temporary_values_keeper.temp_values[chat_id]["isAnswerMethodPerforming"] == False):

                            self.temporary_values_keeper.temp_values["isBGprocessPerforming"] = True

                            for date_key in self.with_problems_worker.problems_of_users[chat_id].copy():
                                print(self.with_problems_worker.problems_of_users[chat_id][date_key][
                                          "howPointsToSendToOperator"])

                                # If it's time to send notification to operator about new problem.
                                if self.with_problems_worker.problems_of_users[chat_id][date_key][
                                    'howPointsToSendToOperator'] == 0:
                                    text = PhrasesGenerator.get_new_problem_text_for_operator(chat_id,
                                                                                              date_key)
                                    ToOperatorByTelegramSender.send_to_operator(self.bot, text, self.operator_data_list,
                                                                                photos=
                                                                                self.with_problems_worker.problems_of_users[
                                                                                    chat_id][date_key]['photos'])
                                    ToOperatorByEmailSender.send_to_operator(text, self.operator_data_list,
                                                                             photos=
                                                                             self.with_problems_worker.problems_of_users[
                                                                                 chat_id][
                                                                                 date_key][
                                                                                 'photos'])

                                    new_problems_dict = self.with_problems_worker.problems_of_users[chat_id][
                                        date_key].copy()
                                    new_problems_dict['howPointsToSendToOperator'] = -1
                                    self.with_problems_worker.change_problem_dict(chat_id, new_problems_dict, date_key)

                                # If the message has already been sent.
                                elif self.with_problems_worker.problems_of_users[chat_id][date_key][
                                    'howPointsToSendToOperator'] == -1:
                                    pass
                                # Otherwise, the message must be sent later.
                                else:
                                    new_problems_dict = self.with_problems_worker.problems_of_users[chat_id][
                                        date_key].copy()
                                    new_problems_dict['howPointsToSendToOperator'] -= 1
                                    self.with_problems_worker.change_problem_dict(chat_id, new_problems_dict, date_key)

                                # If the problem is marked as unresolved.
                                if not self.with_problems_worker.problems_of_users[chat_id][date_key]["issolved"]:
                                    # If it's time for a reminder.
                                    if int(time.time()) > \
                                            self.with_problems_worker.problems_of_users[chat_id][date_key][
                                                "next_reminder"]:
                                        print("Отправляем напоминание")

                                        text = PhrasesGenerator.get_reminder_text(chat_id, date_key)
                                        ToOperatorByTelegramSender.send_to_operator(self.bot, text, self.operator_data_list,
                                                                                    photos=
                                                                                    self.with_problems_worker.problems_of_users[
                                                                                        chat_id][date_key]['photos'])
                                        ToOperatorByEmailSender.send_to_operator(text,
                                                                                 self.operator_data_list,
                                                                                 photos=
                                                                                 self.with_problems_worker.problems_of_users[
                                                                                     chat_id][
                                                                                     date_key][
                                                                                     'photos'])
                                        new_problem_dict = self.with_problems_worker.problems_of_users[chat_id][
                                            date_key].copy()
                                        new_problem_dict["next_reminder"] = int(time.time()) + self.next_reminder
                                        self.with_problems_worker.change_problem_dict(chat_id, new_problem_dict,
                                                                                      date_key)
                            self.temporary_values_keeper.temp_values["isBGprocessPerforming"] = False
