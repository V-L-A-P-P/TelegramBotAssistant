import logging
import MyFileWorker
import telebot

logging.basicConfig(
    format='%(asctime)s: %(message)s',
    level=logging.INFO,
    filename='sample.log')


def send_to_operator(bot, text, operator_data, photos):
    """Sends a message to the operator via telegram."""
    try:
        if photos is None:
            bot.send_message(operator_data["chat_id"], text)
        else:
            if len(photos) == 1:
                photo_id = (photos[0]['name'].split('.'))[0]
                photo_file = bot.get_file(photo_id)
                downloaded_file = bot.download_file(photo_file.file_path)
                bot.send_photo(operator_data["chat_id"], downloaded_file, text)
            elif len(photos) == 0:
                bot.send_message(operator_data["chat_id"], text)
            else:
                media = []
                k = 0
                for photo in photos:
                    img = MyFileWorker.load_image(photo['name'])
                    if k == 0:
                        media.append(telebot.types.InputMediaPhoto(img, caption=text))
                    else:
                        media.append(telebot.types.InputMediaPhoto(open('Images/' + photo['name'], 'rb')))
                    k = 1
                bot.send_media_group(operator_data["chat_id"], media)
        print("Сообщение оператору через телеграмм успешно доставлено")

    except Exception as _ex:
        print(f"Exception in sending to the operator via telegram:\n{_ex}")
        logging.exception(f"Exception in sending to the operator via telegram:\n{_ex}")