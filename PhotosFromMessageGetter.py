import DataWithBackupDumper


def get_photo_from_message(bot, message):
    """Retrieves and returns photos from a message."""
    if message.content_type == 'photo':
        photo_id = message.photo[len(message.photo) - 1].file_id
        name = photo_id + ".jpg"
        photo_file = bot.get_file(photo_id)
        downloaded_file = bot.download_file(photo_file.file_path)
        DataWithBackupDumper.dump_image(downloaded_file, name)
        return {"name": name, "media_group_id": str(message.media_group_id)}
    elif message.content_type == 'document':
        photo_id = message.document.file_id
        name = photo_id + ".jpg"
        photo_file = bot.get_file(photo_id)
        downloaded_file = bot.download_file(photo_file.file_path)
        DataWithBackupDumper.dump_image(downloaded_file, name)
        return {"name": name, "media_group_id": str(message.media_group_id)}
    else:
        return {}