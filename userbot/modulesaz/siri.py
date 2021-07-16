from telethon import events 
import time 
import asyncio 
from userbot.events import register

@register(outgoing=True,pattern="^.[Ss]iri")

async def komut(event):
        await event.edit("**Alışkanlık İşte**\n __Botumuzun İsmi Değişti Unuttun mu Siri Yazmak Yerine__ `.epic` __Yazmalısın.__\n \n**Gerekli Açıklama:** t.me/EpicUserBot/65 \n UserBot Kanalı: @EpicUserBot\nPlugin Kanalı: @EpicPlugin")
