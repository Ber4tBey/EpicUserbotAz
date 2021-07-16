# Erdem Bey / 

from telethon import events
import asyncio
from userbot.events import register

@register(outgoing=True, pattern="^.yay ?(.*)")
async def yay(event):
    mesaj = event.pattern_match.group(1)
    if len(mesaj) < 1:
        await event.edit("`Bir şeyi yaymaq üçün bir mesaj verməlisiniz. Nümunə: ``.yay merhaba dünya`")
        return

    if event.is_private:
        await event.edit("`Bu əmr sadəcə qruplarda işləyir.`")
        return

    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await event.edit("`Ciddisən? Admin olmadığın bir qrupda mesaj göndərməyinə icazə verməyəcəyəm!`")
        return

    await event.edit("`Bütün istifadəçilərə mesajınız göndərilir...`")
    all_participants = await event.client.get_participants(event.chat_id, aggressive=True)
    a = 0

    for user in all_participants:
        a += 1
        uid = user.id
        if user.username:
            link = "@" + user.username
        else:
            link = "[" + user.first_name + "](" + str(user.id) + ")"
        try:
            await event.client.send_message(uid, mesaj + "\n\n@EpicUserBot ilə göndərildi.")
            son = f"**Son mesaj göndərilən istifadəçi:** {link}"
        except:
            son = f"**Son mesaj göndərilən istifadəçi:** **Göndərilmədi!**"
    
        await event.edit(f"`Bütün istifadəçilərə mesajınız göndərilir...`\n{son}\n\n**Status:** `{a}/{len(all_participants)}`")
        await asyncio.sleep(0.5)

    await event.edit("`Bütün istifadəçilərə mesajınız göndərildi!`\n\nby @EpicUserBot 😙")
