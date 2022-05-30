import MyFileWorker
import logging

logging.basicConfig(
    format='%(asctime)s: %(message)s',
    level=logging.INFO,
    filename='sample.log')


def dump_personal_users_data(personal_users_data):
    MyFileWorker.dump_personal_users_data(personal_users_data)
    MyFileWorker.dump_personal_users_data_backup(personal_users_data)


def dump_problems_of_users(problems_of_users):
    MyFileWorker.dump_problems_of_users(problems_of_users)
    MyFileWorker.dump_problems_of_users_backup(problems_of_users)


def dump_counter_of_orders(counter_of_orders):
    MyFileWorker.dump_counter_of_orders(counter_of_orders)
    MyFileWorker.dump_counter_of_orders_backup(counter_of_orders)


def dump_image(downloaded_file, name):
    MyFileWorker.dump_image(downloaded_file, name)
