import os

FOLDERS_LIST = ['Images']
JSON_FILES_IN_FOLDERS = {'Images' : []}
PROJECT_NAME = "TelegramBotAssistant"


class PathesKeeper:
    def __init__(self):
        self.pathes_dict = {}
        self.project_path = self.get_project_path()
        self.update_pathes()

    def update_pathes(self):
        new_path = os.sep.join(map(str, self.project_path))
        for folder_name in FOLDERS_LIST:
            self.pathes_dict[folder_name] = new_path + os.sep + folder_name

    def get_file_path(self, file_name : str):
        pass#  HEEEEEEEERE


    def get_project_path(self) -> list:
        path_list = os.getcwd().split(os.sep)
        while self_path_list[len(self_path_list) - 1] != PROJECT_NAME:
            path_list.pop(len(self_path_list) - 1)
        return path_list