import myFileWorker
import logging

logging.basicConfig(
    format='%(asctime)s: %(message)s',
    level=logging.INFO,
    filename='sample.log')


class DataWithBackupDumper:
    """Dump data into a json file and overwrites its backup."""

    @staticmethod
    def dump_data_of_users(data_of_users):
        myFileWorker.dump_data_of_users(data_of_users)
        myFileWorker.dump_data_of_users_backup(data_of_users)

    @staticmethod
    def dump_problems_of_users(problems_of_users):
        myFileWorker.dump_problems_of_users(problems_of_users)
        myFileWorker.dump_problems_of_users_backup(problems_of_users)

    @staticmethod
    def dump_counter_of_orders(counter_of_orders):
        myFileWorker.dump_counter_of_orders(counter_of_orders)
        myFileWorker.dump_counter_of_orders_backup(counter_of_orders)

    @staticmethod
    def dump_image(downloaded_file, name):
        myFileWorker.dump_image(downloaded_file, name)
