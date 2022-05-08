class TemporaryValuesKeeper:
    def __init__(self):
        self.temp_values = {"list_of_photos_ids": [],
                            "isGetMessageMethodPerforming": False,
                            "isGetUserDataPerforming": False,
                            "isBGprocessPerforming": False,
                            "isDoneProcessPerforming": False}

    def add_id(self, chat_id):
        if not (chat_id in self.temp_values):
            self.temp_values[chat_id] = {}
            self.temp_values[chat_id]['isGetUserDataPerforming'] = False
            self.temp_values[chat_id]["isAnswerMethodPerforming"] = False
            self.temp_values[chat_id]["isGetMessageMethodPerforming"] = False
            self.temp_values[chat_id]["last_message"] = 0
