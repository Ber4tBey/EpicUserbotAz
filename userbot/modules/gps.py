from geopy.geocoders import Nominatim
from telethon.tl import types

from userbot.events import register
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern=r"^.gps (.*)")
async def gps(event):
    if event.fwd_from:
        return
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    input_str = event.pattern_match.group(1)

    if not input_str:
        return await event.edit("`Epic-ə bir bölgənin adını verməlisən!`")

    await event.edit("**Axtarıram...**")

    geolocator = Nominatim(user_agent="erdembey")
    geoloc = geolocator.geocode(input_str)
    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await event.reply(
            input_str,
            file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon)),
            reply_to=reply_to_id,
        )
        await event.delete()
    else:
        await event.edit("`Bağışlayın, belə bir bölgəni tapa bilmədim :(`")

Help = CmdHelp('gps')
Help.add_command('gps <yer>',  None, 'Qeyd etdiyiniz bölgənin konumunu atar.').add()
