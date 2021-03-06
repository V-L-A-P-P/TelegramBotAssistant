import os
import json
import logging
import PathesKeeper

logging.basicConfig(
    format='%(asctime)s: %(message)s',
    level=logging.INFO,
    filename='sample.log')


def load_personal_users_data():
    while True:
        try:
            if os.path.exists('personal_users_data.json'):

                if os.path.getsize("personal_users_data.json") == 0:
                    d = load_personal_users_data_backup()
                    dump_personal_users_data(d)
                    return d
                else:
                    with open("personal_users_data.json", "r") as read_file:
                        d = json.load(read_file)
                    return d
            else:
                d = load_personal_users_data_backup()
                dump_personal_users_data(d)
                return d
        except PermissionError as _ex:
            pass

        except ValueError as _ex:

            d = load_personal_users_data_backup()
            dump_personal_users_data(d)
            return d


def load_personal_users_data_backup():
    while True:
        try:
            if os.path.exists('personal_users_data_backup.json'):

                if os.path.getsize("personal_users_data_backup.json") == 0:
                    d = load_personal_users_data()
                    dump_personal_users_data_backup(d)
                    return d
                else:
                    with open("personal_users_data_backup.json", "r") as read_file:
                        d = json.load(read_file)
                    return d
            else:
                dump_personal_users_data_backup({})
                return {}
        except PermissionError as _ex:

            pass

        except ValueError as _ex:
            d = load_personal_users_data()
            dump_personal_users_data_backup(d)
            return d


def load_problems_of_users():
    while True:
        try:
            if os.path.exists('problems_of_users.json'):
                if os.path.getsize("problems_of_users.json") == 0:
                    print("???????? ??????????????????")
                    up = load_problems_of_users_backup()
                    dump_problems_of_users(up)
                    return up
                else:
                    with open("problems_of_users.json", "r") as read_file:
                        up = json.load(read_file)
                    return up
            else:
                up = load_problems_of_users_backup()
                dump_problems_of_users(up)
                return up

        except PermissionError as _ex:
            pass

        except ValueError as _ex:
            print(_ex)
            up = load_problems_of_users_backup()
            dump_problems_of_users(up)
            return up


def load_problems_of_users_backup():
    while True:
        try:
            if os.path.exists('problems_of_users_backup.json'):
                if os.path.getsize("problems_of_users_backup.json") == 0:
                    up = load_problems_of_users()
                    dump_problems_of_users_backup(up)
                    return up
                else:
                    with open("problems_of_users_backup.json", "r") as read_file:
                        up = json.load(read_file)
                    return up
            else:
                dump_problems_of_users_backup({})
                return {}

        except PermissionError as _ex:
            pass

        except ValueError as _ex:
            up = load_problems_of_users()
            dump_problems_of_users_backup(up)
            return up


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


def load_counter_of_orders():
    while True:
        try:
            if os.path.exists('counter_of_orders.json'):

                if os.path.getsize("counter_of_orders.json") == 0:
                    print("counter_of_orders was deleted")
                    up = load_counter_of_orders_backup()
                    dump_counter_of_orders(up)
                    return up
                else:
                    with open("counter_of_orders.json", "r") as read_file:
                        up = json.load(read_file)
                    return up
            else:
                count = load_counter_of_orders_backup()
                dump_counter_of_orders(count)
                return count

        except PermissionError as _ex:

            pass

        except ValueError as _ex:

            up = load_counter_of_orders_backup()
            dump_counter_of_orders(up)
            return up


def load_counter_of_orders_backup():
    while True:
        try:
            if os.path.exists('counter_of_orders_backup.json'):
                if os.path.getsize("counter_of_orders_backup.json") == 0:
                    up = load_counter_of_orders()
                    dump_counter_of_orders_backup(up)
                    return up
                else:
                    with open("counter_of_orders_backup.json", "r") as read_file:
                        up = json.load(read_file)
                    return up
            else:
                dump_counter_of_orders_backup(0)
                return 0


        except PermissionError as _ex:

            pass




        except ValueError as _ex:
            up = load_counter_of_orders()
            dump_counter_of_orders_backup(up)
            return up



def dump_counter_of_orders(d):
    while True:
        try:
            with open("counter_of_orders.json", "w") as write_file:
                json.dump(d, write_file)
            return
        except:
            pass


def dump_counter_of_orders_backup(d):
    while True:
        try:
            with open("counter_of_orders_backup.json", "w") as write_file:
                json.dump(d, write_file)
            return
        except:
            pass


def dump_personal_users_data(d):
    while True:
        try:
            with open("personal_users_data.json", "w") as write_file:
                json.dump(d, write_file)
            return
        except:
            pass


def dump_problems_of_users(up):
    while True:
        try:
            with open("problems_of_users.json", "w") as write_file:
                json.dump(up, write_file)
            return
        except:
            pass


def dump_personal_users_data_backup(d):
    while True:
        try:
            with open("personal_users_data_backup.json", "w") as write_file:
                json.dump(d, write_file)
            return
        except:
            pass


def dump_problems_of_users_backup(up):
    while True:
        try:
            with open("problems_of_users_backup.json", "w") as write_file:
                json.dump(up, write_file)
            return
        except:
            pass


def dump_data_of_operator(d):
    while True:
        try:

            with open("data_of_operator.json", "w") as write_file:
                json.dump(d, write_file)
            return
        except:
            pass


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



