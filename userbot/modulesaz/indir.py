from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from userbot import bot

@register(outgoing=True, pattern="^.indir ?(.*)")
async def epicnsta(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Yükləmək üçün bir link verin!`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.edit("`Yükləmək üçün bir link verin!`")
        return
    chat = "@SaveAsbot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("`Epic yükləyə bilmədi\n Xahiş edirəm başqa bir link yoxlayın!`")
        return
    asc = await event.edit("`Epic yükləyir biraz səbrli ol...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=523131145)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.edit(" @SaveAsBot `botunun blokunu açın və sonra yenidən yoxlayın!")
            return
        if response.text.startswith("Forward"):
            await event.edit(
                "`Gizlilik ayarlarınızdakı yönləndirmə qismini düzəldin.`"
            )
        elif "Что поддерживается?" in response.text:
            await event.edit(
                "⛔️ `Bu linkin nə olduğu haqqında bir fikrim yoxdur!`"
            )
        else:
            await event.delete()
            await event.client.send_file(
                event.chat_id,
                response.message.media,
                caption=f"@EpicUserBot `ile yükləndi`",
            )
            await event.client.send_read_acknowledge(conv.chat_id)
            

CmdHelp('indir').add_command(
    'indir', None, 'Linkə cavab verin .indir əmri ilə\nİnstagramdan IGTV-Hekayə-Video-Şəkil\nTikToktan Video\nPinterestten Video-Fotoğraf'
).add()
