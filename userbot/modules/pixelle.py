# EPİCUSERBOT / ERDEM-BEY

from userbot.events import register
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon import events

@register(outgoing=True, pattern="^.pixelle")
async def pixelator(event):
    if not event.reply_to_msg_id:
        await event.edit("`Xahiş edirəm bir şəkil və ya stiker'ə cavab verin.`")
        return

    reply_message = await event.get_reply_message() 
    
    if not reply_message.media:
        await event.edit("`Xahiş edirəm bir şəkil və ya stiker'ə cavab verin.`")
        return

    chat = "@pixelatorbot"
    if reply_message.sender.bot:
        await event.edit("`Xahiş edirəm real bir istifadəçinin mesajına cavab verin.`")
        return

    await event.edit("`Şəkil pikselləşdirilir...`")
    async with event.client.conversation(chat) as conv:
        try:     
            await event.client.forward_messages(chat, reply_message)
        except YouBlockedUserError:
            await event.reply(f"`Hmm deyəsən` {chat} `əngəlləmisən. Xahiş edirəm bloku aç.`")
            return

        response = await conv.wait_event(events.NewMessage(incoming=True,from_users="@PixelatorBot"))
        await event.client.send_read_acknowledge("@PixelAtorBot")
        if response.text.startswith("Looks"):
            await event.edit("`Bunu pikselləşdirə bilmərəm!`")
        else:
            await event.client.send_message(event.chat_id, "`Şəkil uğurla pikselləşdirildi!`", file=response.message)
            await event.delete()
