import os
import json
import traceback
import logging

logging.basicConfig(
    format='%(asctime)s: %(message)s',
    level=logging.INFO,
    filename='sample.log')


class MyFileWorker:
    @staticmethod
    def load_data_of_users():
        while True:
            try:
                if os.path.exists('data_of_users.json'):

                    if os.path.getsize("data_of_users.json") == 0:
                        d = MyFileWorker.load_data_of_users_backup()
                        MyFileWorker.dump_data_of_users(d)
                        return d
                    else:
                        with open("data_of_users.json", "r") as read_file:
                            d = json.load(read_file)
                        return d
                else:
                    MyFileWorker.dump_data_of_users({})
                    return {}


            except PermissionError as _ex:

                pass


            except ValueError as _ex:

                d = MyFileWorker.load_data_of_users_backup()
                MyFileWorker.dump_data_of_users(d)
                return d

    @staticmethod
    def load_data_of_users_backup():
        while True:
            try:
                if os.path.exists('data_of_users_backup.json'):

                    if os.path.getsize("data_of_users_backup.json") == 0:
                        d = MyFileWorker.load_data_of_users()
                        MyFileWorker.dump_data_of_users_backup(d)
                        return d
                    else:
                        with open("data_of_users_backup.json", "r") as read_file:
                            d = json.load(read_file)
                        return d
                else:
                    MyFileWorker.dump_data_of_users_backup({})
                    return {}
            except PermissionError as _ex:

                pass


            except ValueError as _ex:
                d = MyFileWorker.load_data_of_users()
                MyFileWorker.dump_data_of_users_backup(d)
                return d

    @staticmethod
    def load_problems_of_users():
        while True:
            try:
                if os.path.exists('problems_of_users.json'):
                    if os.path.getsize("problems_of_users.json") == 0:
                        print("дата удалилась")
                        up = MyFileWorker.load_problems_of_users_backup()
                        MyFileWorker.dump_problems_of_users(up)
                        return up
                    else:
                        with open("problems_of_users.json", "r") as read_file:
                            up = json.load(read_file)
                        return up
                else:
                    MyFileWorker.dump_problems_of_users({})
                    return {}

            except PermissionError as _ex:
                pass

            except ValueError as _ex:
                print(_ex)
                up = MyFileWorker.load_problems_of_users_backup()
                MyFileWorker.dump_problems_of_users(up)
                return up

    @staticmethod
    def load_problems_of_users_backup():
        while True:
            try:
                if os.path.exists('problems_of_users_backup.json'):
                    if os.path.getsize("problems_of_users_backup.json") == 0:
                        up = MyFileWorker.load_problems_of_users()
                        MyFileWorker.dump_problems_of_users_backup(up)
                        return up
                    else:
                        with open("problems_of_users_backup.json", "r") as read_file:
                            up = json.load(read_file)
                        return up
                else:
                    MyFileWorker.dump_problems_of_users_backup({})
                    return {}


            except PermissionError as _ex:

                pass


            except ValueError as _ex:
                up = MyFileWorker.load_problems_of_users()
                MyFileWorker.dump_problems_of_users_backup(up)
                return up

    @staticmethod
    def load_data_of_operator():
        while True:
            try:
                if os.path.exists('data_of_operator.json'):
                    with open("data_of_operator.json", "r") as read_file:
                        up = json.load(read_file)
                    return up
                else:
                    return {"email": "", "password": "", "chat_id": ""}

            except:
                pass

    @staticmethod
    def load_image(file_name):
        src = 'Images/' + file_name
        while True:
            try:
                if os.path.exists(src):
                    with open(src, "rb") as read_file:
                        img = read_file.read()
                    return img
                else:
                    return None

            except:
                pass

    @staticmethod
    def load_counter_of_orders():
        while True:
            try:
                if os.path.exists('counter_of_orders.json'):

                    if os.path.getsize("counter_of_orders.json") == 0:
                        print("counter_of_orders was deleted")
                        up = MyFileWorker.load_counter_of_orders_backup()
                        MyFileWorker.dump_counter_of_orders(up)
                        return up
                    else:
                        with open("counter_of_orders.json", "r") as read_file:
                            up = json.load(read_file)
                        return up
                else:
                    MyFileWorker.dump_counter_of_orders(0)
                    return 0


            except PermissionError as _ex:

                pass



            except ValueError as _ex:

                up = MyFileWorker.load_counter_of_orders_backup()
                MyFileWorker.dump_counter_of_orders(up)
                return up

    @staticmethod
    def load_counter_of_orders_backup():
        while True:
            try:
                if os.path.exists('counter_of_orders_backup.json'):
                    if os.path.getsize("counter_of_orders_backup.json") == 0:
                        up = MyFileWorker.load_counter_of_orders()
                        MyFileWorker.dump_counter_of_orders_backup(up)
                        return up
                    else:
                        with open("counter_of_orders_backup.json", "r") as read_file:
                            up = json.load(read_file)
                        return up
                else:
                    MyFileWorker.dump_counter_of_orders_backup(0)
                    return 0


            except PermissionError as _ex:

                pass




            except ValueError as _ex:
                up = MyFileWorker.load_counter_of_orders()
                MyFileWorker.dump_counter_of_orders_backup(up)
                return up

    @staticmethod
    def load_bot_token():
        while True:
            try:
                if os.path.exists('bot_token.json'):
                    with open("bot_token.json", "r") as read_file:
                        bt = json.load(read_file)
                    return bt
                else:
                    MyFileWorker.dump_bot_token(0)
                    return 0

            except PermissionError as _ex:
                pass

    @staticmethod
    def dump_bot_token(bt):
        while True:
            try:
                with open("bot_token.json", "w") as write_file:
                    json.dump(bt, write_file)
                return
            except:
                pass

    @staticmethod
    def dump_counter_of_orders(d):
        while True:
            try:
                with open("counter_of_orders.json", "w") as write_file:
                    json.dump(d, write_file)
                return
            except:
                pass

    @staticmethod
    def dump_counter_of_orders_backup(d):
        while True:
            try:
                with open("counter_of_orders_backup.json", "w") as write_file:
                    json.dump(d, write_file)
                return
            except:
                pass

    @staticmethod
    def dump_data_of_users(d):
        while True:
            try:
                with open("data_of_users.json", "w") as write_file:
                    json.dump(d, write_file)
                return
            except:
                pass

    @staticmethod
    def dump_problems_of_users(up):
        while True:
            try:
                with open("problems_of_users.json", "w") as write_file:
                    json.dump(up, write_file)
                return
            except:
                pass

    @staticmethod
    def dump_data_of_users_backup(d):
        while True:
            try:
                with open("data_of_users_backup.json", "w") as write_file:
                    json.dump(d, write_file)
                return
            except:
                pass

    @staticmethod
    def dump_problems_of_users_backup(up):
        while True:
            try:
                with open("problems_of_users_backup.json", "w") as write_file:
                    json.dump(up, write_file)
                return
            except:
                pass

    @staticmethod
    def dump_data_of_operator(d):
        while True:
            try:

                with open("data_of_operator.json", "w") as write_file:
                    json.dump(d, write_file)
                return
            except:
                pass

    @staticmethod
    def dump_image(img, name):
        src = 'Images/' + name
        if not os.path.exists("Images"):
            os.mkdir("Images")
        while True:
            try:
                with open(src, 'wb') as write_file:
                    write_file.write(img)
                return
            except:
                pass

    @staticmethod
    def load_data_items_const():
        try:
            with open("DATA_ITEMS.json", 'r') as read_file:
                return json.load(read_file)
        except:
            pass
