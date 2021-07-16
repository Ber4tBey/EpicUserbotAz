# GNU LICENCE / EpicUserBot - ErdemBey - Midy

import codecs
import heroku3
import asyncio
import aiohttp
import math
import os
import ssl
import requests

from userbot import (
    HEROKU_APPNAME,
    HEROKU_APIKEY,
    BOTLOG,
    ASISTAN,
    MYID,
    BOTLOG_CHATID
)

from userbot.events import register
from userbot.cmdhelp import CmdHelp
from telethon.errors.rpcerrorlist import PeerIdInvalidError # Botlog grubundan çıktıysa

heroku_api = "https://api.heroku.com"
if HEROKU_APPNAME is not None and HEROKU_APIKEY is not None:
    Heroku = heroku3.from_key(HEROKU_APIKEY)
    app = Heroku.app(HEROKU_APPNAME)
    heroku_var = app.config()
else:
    app = None




@register(outgoing=True, pattern=r'^.set var (\w*) ([\s\S]*)')
async def set_var(var):
    await var.edit("`🔄 Məlumatlar Herokuya Yazılır...`")
    variable = var.pattern_match.group(1)
    value = var.pattern_match.group(2)
    fix = False
    if variable in heroku_var:
        try:
            if BOTLOG:
                await var.client.send_message(
                    BOTLOG_CHATID, "#SETCONFIGVAR\n\n"
                    "**ConfigVar Dəyişikliyi**:\n"
                    f"`{variable}` = `{value}`"
                )
            await var.edit("`Veriler Yazıldı!`")
        except PeerIdInvalidError:
             fix = True
             await var.edit("😒 Botlog qrupundan çıxmısan.. Sənin üçün düzəldirəm..")
    else:
        try:
            if BOTLOG:
                await var.client.send_message(
                    BOTLOG_CHATID, "#ADDCONFIGVAR\n\n"
                    "**Yeni ConfigVar Əlavə Edildi**:\n"
                    f"`{variable}` = `{value}`"
                )
            await var.edit("`Veriler Yazıldı!`")
        except PeerIdInvalidError:
            fix = True
            await var.edit("😒 Botlog qrupundan çıxmısan.. Sənin üçün düzəldirəm..")
    if fix:
        heroku_var["BOTLOG"] = "False"
    else:
        heroku_var[variable] = value


@register(incoming=True, from_users=ASISTAN, pattern="^.setvar (\w*) ([\s\S]*)")
async def asistansetvar(ups):
    """ Sadece bilgileri değiştirebilir kodlardan görüldüğü üzere bilgileri göremez. """
    if ups.is_reply:
        reply = await ups.get_reply_message()
        reply_user = await ups.client.get_entity(reply.from_id)
        ren = reply_user.id
        if ren == MYID:
            usp = await ups.reply("`⚙️ Asistan'dan alınan veriler herokuya yazılıyor...`")
            dg = ups.text.replace(".setvar ","")
            dgs = dg.split(":")
            variable = dgs[0]
            value = dgs[1]
            heroku_var[variable] = value
            if variable in heroku_var:
                if BOTLOG:
                    await ups.client.send_message(
                        BOTLOG_CHATID, "#SETCONFIGVAR\n\n"
                        "**Asistan tərəfindən ConfigVar Dəyişikliyi**:\n"
                        f"`{variable}` = `{value}`"
                    )
            else:
                if BOTLOG:
                    await ups.client.send_message(
                        BOTLOG_CHATID, "#ADDCONFIGVAR\n\n"
                        "**Yeni ConfigVar Eklendi**:\n"
                        f"`{variable}` = `{value}`"
                    )
            await usp.edit("`⚙️ Asistandan alınan məlumatlar herokuya yazıldı!`")
        else:
            return
    else:
        return


"""Hesabınızdakı dynosuna bakmanızı yarayan userbot modulu"""


@register(outgoing=True, pattern=r"^.dyno(?: |$)")
async def dyno_usage(dyno):
    """Bu qisimdə bot istifadə edilmiş dynonu əldə etməyə çalışır"""
    await dyno.edit("`🔄 Lütfen Bekleyiniz...`")
    useragent = ('Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/80.0.3987.149 Mobile Safari/537.36'
                 )
    u_id = Heroku.account().id
    headers = {
     'User-Agent': useragent,
     'Authorization': f'Bearer {HEROKU_APIKEY}',
     'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
    }
    path = "/accounts/" + u_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("`Error: something bad happened`\n\n"
                               f">.`{r.reason}`\n")
    result = r.json()
    quota = result['account_quota']
    quota_used = result['quota_used']

    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)

    """ - Current - """
    App = result['apps']
    try:
        App[0]['quota_used']
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]['quota_used'] / 60
        AppPercentage = math.floor(App[0]['quota_used'] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)

    await asyncio.sleep(1.5)

    return await dyno.edit("**✨ Qalan Dyno**:\n\n"
                           f" 👉🏻 `İstifadə Edilən Dyno Saatı`  **({HEROKU_APPNAME})**:\n"
                           f"     ⌛  `{AppHours}` **saat**  `{AppMinutes}` **dəqiqə**  "
                           f"**|**  [`{AppPercentage}` **%**]"
                           "\n"
                           " 👉🏻 `Bu ay üçün qalan dyno saatı`:\n"
                           f"     ⌛  `{hours}` **saat**  `{minutes}` **dəqiqə**  "
                           f"**|**  [`{percentage}` **%**]"
                           )

@register(outgoing=True, pattern=r"^\.herokulog")
async def _(dyno):
    try:
        Heroku = heroku3.from_key(HEROKU_APIKEY)
        app = Heroku.app(HEROKU_APPNAME)
    except BaseException:
        return await dyno.reply(
            "`Litfen gözləyin ,Heroku VARS'da Heroku API Key ve Heroku APP name'in düzgün olduğundan emin olun.`"
        )
    await dyno.edit("`🔄 Log gətirilir....`")
    with open("logs.txt", "w") as log:
        log.write(app.get_log())
    fd = codecs.open("logs.txt", "r", encoding="utf-8")
    data = fd.read()
    key = (requests.post("https://nekobin.com/api/documents",
                         json={"content": data}) .json() .get("result") .get("key"))
    url = f"https://nekobin.com/raw/{key}"
    await dyno.edit(f"`Heroku log'u :`\n\n: [S  İ  R  İ]({url})")
    return os.remove("logs.txt")


CmdHelp('heroku').add_command(
'dyno', None, 'Dyno saati hakkında bilgi verir..'
    ).add_command(
        'set var', None, 'set var <Yeni Var adı> <değer> Botunuza yeni ConfigVar eklenir.'
    ).add_command(
        'get var', None, 'Güvenlik Nedeni İle İptal Edilmiştir.'
    ).add_command(
        'del var', None, 'del var <Var adı> Seçdiğiniz ConfigVarı siler sildikten sonra botunuza .restart atın.'
    ).add_command(
        'log', None, 'Heroku logunuza bakın'
    ).add_info(
        '**Botlog grubundan çıktıysanız sizin yerinize düzeltmesi için** `.set var BOTLOG False` **yazın.. ✨ Thx to @erdembey**'
    ).add()
