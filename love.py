from .. import loader

@loader.tds
class EchoMod(loader.Module):
    """Эхо модуль."""
    strings = {'name': 'Echo'}

    async def client_ready(self, client, db):
        self.db = db
        self.message_history = {}  # Store message history per chat

    async def echocmd(self, message):
        """Активировать/деактивировать Echo."""
        echos = self.db.get("Echo", "chats", []) 
        chatid = str(message.chat_id)

        if chatid not in echos:
            echos.append(chatid)
            self.db.set("Echo", "chats", echos)

            # Send stored messages if there are any
            if chatid in self.message_history:
                for msg in self.message_history[chatid]:
                    await message.client.send_message(int(chatid), msg)

                # Clear the history after sending
                del self.message_history[chatid]

            return await message.edit("<b>[Echo Mode]</b> Активирован в этом чате!")

        echos.remove(chatid)
        self.db.set("Echo", "chats", echos)
        return await message.edit("<b>[Echo Mode]</b> Деактивирован в этом чате!")

    async def watcher(self, message):
        echos = self.db.get("Echo", "chats", [])
        chatid = str(message.chat_id)

        if chatid not in str(echos): 
            # Store messages before Echo is activated
            if chatid not in self.message_history:
                self.message_history[chatid] = []
            self.message_history[chatid].append(message.text)
            return

        if message.sender_id == (await message.client.get_me()).id: 
            return

        # Отправляем команду /kick вместо повторения сообщения
        await message.client.send_message(int(chatid), "/kick", reply_to=await message.get_reply_message() or message)
