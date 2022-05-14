import PhotosFromMessageGetter
import PhrasesGenerator
import logging
import time
import MyFileWorker


class MessagesHandler:
    """
    Methods:
        reply_to_text(message)
        reply_to_photo(message)
        reply_to_document(message)
        reply_to_start_command(message)

    """

    def __init__(self, bot, with_data_worker, with_problems_worker, temporary_values_keeper):
        operator_data_list = MyFileWorker.load_data_of_operator()
        self.operator_id = operator_data_list["chat_id"]
        self.operator_mail = operator_data_list["email"]
        self.operator_mail_password = operator_data_list["password"]
        self.with_data_worker = with_data_worker
        self.with_problems_worker = with_problems_worker
        self.temporary_values_keeper = temporary_values_keeper
        self.bot = bot

    def reply_to_text(self, message):
        """
            This method will be called if the bot receives a 'text' type as a message.
            Processes the content of the user's message.
        """
        self.temporary_values_keeper.add_id(str(message.chat.id))
        if self.temporary_values_keeper.temp_values[str(message.chat.id)]['isGetUserDataPerforming'] or \
                self.temporary_values_keeper.temp_values[str(message.chat.id)]["isGetMessageMethodPerforming"] or \
                self.temporary_values_keeper.temp_values[str(message.chat.id)]["isAnswerMethodPerforming"]:
            return
        while True:
            if not self.temporary_values_keeper.temp_values["isDoneProcessPerforming"]:
                self.temporary_values_keeper.temp_values[str(message.chat.id)]["isAnswerMethodPerforming"] = True
                break
            time.sleep(0.1)
        print(f" ' {message.text} ' by {message.from_user.first_name} {message.chat.id}")

        self.with_problems_worker.update_problems_of_users()

        # If operator details are not specified.
        if self.operator_id == "":
            print("Введите данные оператора в приложении")
        # If a message is received from an operator.
        elif str(message.chat.id) == self.operator_id:
            self.bot.send_message(str(message.chat.id), PhrasesGenerator.get_info_text_for_operator())
        else:
            # If user data has already been received
            if self.with_data_worker.data_of_users.get(
                    str(message.chat.id)) is not None \
                    and self.with_data_worker.data_of_users.get(str(message.chat.id)).get("phonenumber") is not None:

                self.with_data_worker.update_data_of_users()
                self.bot.send_message(str(message.chat.id),
                                      PhrasesGenerator.get_hello_text_with_data(str(message.chat.id)))
                self.with_problems_worker.get_new_problem(message)
            else:
                self.bot.send_message(str(message.chat.id), PhrasesGenerator.get_hello_text_without_data())
                self.with_data_worker.get_new_user(message, self.with_problems_worker.add_new_user,
                                                   self.with_problems_worker.get_new_problem)

        self.temporary_values_keeper.temp_values[str(message.chat.id)]["isAnswerMethodPerforming"] = False
        self.temporary_values_keeper.temp_values[str(message.chat.id)]["last_message"] = time.time()

    def reply_to_photo(self, message):
        """
            This method will be called if the bot receives a 'photo' type as a message.
            Processes the content of the user's message.
        """
        self.temporary_values_keeper.add_id(str(message.chat.id))
        if self.temporary_values_keeper.temp_values[str(message.chat.id)]['isGetUserDataPerforming']:
            return
        # If a method for processing a message or receiving a problem for this user is already running, then
        # the process is queued
        while True:
            if self.temporary_values_keeper.temp_values[str(message.chat.id)]["isGetMessageMethodPerforming"] == False and \
                    self.temporary_values_keeper.temp_values[str(message.chat.id)]["isAnswerMethodPerforming"] == False \
                    and self.temporary_values_keeper.temp_values["isDoneProcessPerforming"] == False:
                self.temporary_values_keeper.temp_values[str(message.chat.id)]["isAnswerMethodPerforming"] = True
                break
            time.sleep(0.1)

        print(f"Photo by {message.from_user.first_name} {message.chat.id}")
        logging.info(f"Photo by {message.from_user.first_name} {message.chat.id}")
        # If this photo belongs to a post with a group of photos that we have already replied to.
        if str(message.media_group_id) in self.temporary_values_keeper.temp_values['list_of_photos_ids']:
            print("Отбрасываем фото, которое принадлежит к сообщению с группой фотографий, на которое мы уже ответили")
            self.temporary_values_keeper.temp_values[str(message.chat.id)]["isAnswerMethodPerforming"] = False
            self.temporary_values_keeper.temp_values[str(message.chat.id)]["last_message"] = time.time()
            return

        if self.operator_id == "":  # If operator details are not specified.
            print("Введите данные оператора в приложении")

        elif str(message.chat.id) == self.operator_id:  # If a message is received from an operator.
            self.bot.send_message(str(message.chat.id), PhrasesGenerator.get_info_text_for_operator())

        elif self.with_data_worker.data_of_users.get(
                str(message.chat.id)) is not None \
                and self.with_data_worker.data_of_users.get(str(message.chat.id)).get("phonenumber") is not None:
            if message.media_group_id is not None:  # If a group of photos was sent.
                source_dict = self.with_problems_worker.get_photos_list_with_mediagroupid(str(message.media_group_id))
                if source_dict is None:  # If no photos of this group have been added to the problems.

                    self.temporary_values_keeper.temp_values['list_of_photos_ids'].append(str(message.media_group_id))
                    if time.time() - self.temporary_values_keeper.temp_values[str(message.chat.id)]["last_message"] > 1:
                        self.with_problems_worker.update_problems_of_users()
                        self.bot.send_message(str(message.chat.id),
                                         PhrasesGenerator.get_hello_text_with_data(
                                             str(message.chat.id)))
                        self.with_problems_worker.get_new_problem(message)
                else:  # Otherwise, there is already a problem with the photos of this media group and we add photos there.
                    photo_dict = PhotosFromMessageGetter.get_photo_from_message(self.bot, message)
                    self.with_problems_worker.update_problems_of_users()
                    dict_with_new_photos = self.with_problems_worker.problems_of_users[str(message.chat.id)][
                        source_dict['date_key']].copy()
                    dict_with_new_photos["photos"].append(photo_dict)
                    self.with_problems_worker.change_problem_dict(str(message.chat.id), dict_with_new_photos,
                                                                  source_dict['date_key'])

            else:  # Otherwise, this is a single photo.
                if time.time() - self.temporary_values_keeper.temp_values[str(message.chat.id)]["last_message"] > 1:
                    self.with_problems_worker.update_problems_of_users()
                    self.bot.send_message(str(message.chat.id),
                                     PhrasesGenerator.get_hello_text_with_data(str(message.chat.id)))
                    self.with_problems_worker.get_new_problem(message)

        else:  # If user data has not yet been received.
            self.temporary_values_keeper.temp_values['list_of_photos_ids'].append(str(message.media_group_id))
            self.bot.send_message(str(message.chat.id), PhrasesGenerator.get_hello_text_without_data())
            self.with_data_worker.get_new_user(message, self.with_problems_worker.add_new_user,
                                               self.with_problems_worker.get_new_problem)
        self.temporary_values_keeper.temp_values[str(message.chat.id)]["isAnswerMethodPerforming"] = False
        self.temporary_values_keeper.temp_values[str(message.chat.id)]["last_message"] = time.time()

    def reply_to_document(self, message):
        """
            This method will be called if the bot receives a "document" type as a message.
            Processes the content of the user's message.
        """
        # If no initial values have been set yet.
        self.temporary_values_keeper.add_id(str(message.chat.id))

        if self.temporary_values_keeper.temp_values[str(message.chat.id)]['isGetUserDataPerforming']:
            return

        # If a method for processing a message or receiving a problem for this user is already running, then
        # the process is queued.
        while True:
            if self.temporary_values_keeper.temp_values[str(message.chat.id)]["isGetMessageMethodPerforming"] == False and \
                    self.temporary_values_keeper.temp_values[str(message.chat.id)]["isAnswerMethodPerforming"] == False \
                    and self.temporary_values_keeper.temp_values["isDoneProcessPerforming"] == False:
                self.temporary_values_keeper.temp_values[str(message.chat.id)]["isAnswerMethodPerforming"] = True
                break
            print("Процесс попал в очередь:")
            print(self.temporary_values_keeper.temp_values)
            time.sleep(0.1)

        print(f"File by {message.from_user.first_name} {message.chat.id}")
        logging.info(f"File by {message.from_user.first_name} {message.chat.id}")

        # If this photo belongs to a post with a group of photos that we have already replied to.
        if str(message.media_group_id) in self.temporary_values_keeper.temp_values['list_of_photos_ids']:
            print("Отбрасываем фото, которое принадлежит к сообщению с группой фотографий, на которое мы уже ответили")
            self.temporary_values_keeper.temp_values[str(message.chat.id)]["isAnswerMethodPerforming"] = False
            self.temporary_values_keeper.temp_values[str(message.chat.id)]["last_message"] = time.time()
            return

        if self.operator_id == "":  # If operator details are not specified.
            print("Введите данные оператора в приложении")

        elif str(message.chat.id) == self.operator_id:  # If a message is received from an operator.
            self.bot.send_message(str(message.chat.id), PhrasesGenerator.get_info_text_for_operator())

        # If user data has already been received.
        elif self.with_data_worker.data_of_users.get(str(message.chat.id)) is not None \
                and self.with_data_worker.data_of_users.get(str(message.chat.id)).get("phonenumber") is not None:

            if message.media_group_id is not None:  # If a group of photos was sent.
                source_dict = self.with_problems_worker.get_photos_list_with_mediagroupid(str(message.media_group_id))

                if source_dict is None:  # If no photos of this group have been added to problems yet.

                    last_problem_key = self.with_problems_worker.get_last_appeal_key(message)

                    # If the telegram split the photo and text with it into 2 messages.
                    if last_problem_key is not None and (int(time.time()) - self.with_problems_worker.problems_of_users[
                        str(message.chat.id)][last_problem_key]['date'] <= 5) \
                            and (len(
                        self.with_problems_worker.problems_of_users[str(message.chat.id)][last_problem_key][
                            'photos']) == 0):

                        photo_dict = PhotosFromMessageGetter.get_photo_from_message(self.bot, message)
                        self.with_problems_worker.update_problems_of_users()
                        dict_with_new_photos = self.with_problems_worker.problems_of_users[str(message.chat.id)][
                            last_problem_key].copy()
                        dict_with_new_photos["photos"].append(photo_dict)
                        self.with_problems_worker.change_problem_dict(str(message.chat.id), dict_with_new_photos,
                                                                      last_problem_key)

                    else:  # Otherwise, this message is the first photo from the media group we are responding to.
                        self.temporary_values_keeper.temp_values['list_of_photos_ids'].append(str(message.media_group_id))
                        if time.time() - self.temporary_values_keeper.temp_values[str(message.chat.id)]["last_message"] > 1:
                            self.bot.send_message(str(message.chat.id),
                                             PhrasesGenerator.get_hello_text_with_data(
                                                 str(message.chat.id)))
                            self.with_problems_worker.get_new_problem(message)

                else:  # Otherwise, there is already a problem with the photos of this media group and we add photos there.
                    photo_dict = PhotosFromMessageGetter.get_photo_from_message(self.bot, message)
                    self.with_data_worker.update_data_of_users()
                    dict_with_new_photos = self.with_problems_worker.problems_of_users[str(message.chat.id)][
                        source_dict['date_key']].copy()
                    dict_with_new_photos["photos"].append(photo_dict)
                    self.with_problems_worker.change_problem_dict(str(message.chat.id), dict_with_new_photos,
                                                                  source_dict['date_key'])

            else:  # Otherwise, this is a single photo.
                if time.time() - self.temporary_values_keeper.temp_values[str(message.chat.id)]["last_message"] > 1:
                    self.with_problems_worker.update_problems_of_users()
                    self.bot.send_message(str(message.chat.id),
                                     PhrasesGenerator.get_hello_text_with_data(str(message.chat.id)))
                    self.with_problems_worker.get_new_problem(message)

        else:  # If user data has not yet been received.
            self.temporary_values_keeper.temp_values['list_of_photos_ids'].append(str(message.media_group_id))
            if time.time() - self.temporary_values_keeper.temp_values[str(message.chat.id)]["last_message"] > 1:
                self.bot.send_message(str(message.chat.id), PhrasesGenerator.get_hello_text_without_data())
                self.with_data_worker.get_new_user(message, self.with_problems_worker.add_new_user,
                                                   self.with_problems_worker.get_new_problem)

        self.temporary_values_keeper.temp_values[str(message.chat.id)]["isAnswerMethodPerforming"] = False
        self.temporary_values_keeper.temp_values[str(message.chat.id)]["last_message"] = time.time()

    def reply_to_start_command(self, message):
        """
            This method should be called when the user enters the 'start' command.
            Processes the content of the user's message.

        """
        print(f"start/ command by {message.chat.id}")
        logging.info(f"start/ command by {message.chat.id}")

        self.with_problems_worker.update_problems_of_users()

        self.temporary_values_keeper.add_id(str(message.chat.id))

        if self.operator_id == "":  # If operator details are not specified.
            print("Введите данные оператора в приложении")

        elif str(message.chat.id) == self.operator_id:  # If a message is received from an operator.
            self.bot.send_message(str(message.chat.id), PhrasesGenerator.get_info_text_for_operator())

        # If user data has not yet been received.
        elif self.with_data_worker.data_of_users.get(str(message.chat.id)) is None \
                or self.with_data_worker.data_of_users.get(str(message.chat.id)).get("phonenumber") is None:

            if time.time() - self.temporary_values_keeper.temp_values[str(message.chat.id)]["last_message"] > 1:
                self.bot.send_message(str(message.chat.id), PhrasesGenerator.get_hello_text_without_data())
                self.with_data_worker.get_new_user(message, self.with_problems_worker.add_new_user,
                                                   self.with_problems_worker.get_new_problem)

        else:  # Otherwise, user data is received.
            if time.time() - self.temporary_values_keeper.temp_values[str(message.chat.id)]["last_message"] > 1:
                self.bot.send_message(str(message.chat.id),
                                 PhrasesGenerator.get_hello_text_with_data(str(message.chat.id)))
                self.with_problems_worker.get_new_problem(message)

        self.temporary_values_keeper.temp_values[str(message.chat.id)]["last_message"] = time.time()

