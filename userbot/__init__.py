# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Thanks github.com/spechide for creating inline bot support.
# EpicUserBot - Erdem By - ByMisakiMey
""" UserBot hazırlanışı. """

import os
import time
import heroku3
from re import compile
from .utils.pip_install import install_pip
from sys import version_info
from logging import basicConfig, getLogger, INFO, DEBUG
from distutils.util import strtobool as sb
from pylast import LastFMNetwork, md5
from pySmartDL import SmartDL
from sqlite3 import connect
from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from dotenv import load_dotenv
from requests import get
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.sync import TelegramClient, custom
from telethon.sessions import StringSession
from telethon.events import callbackquery, InlineQuery, NewMessage
from math import ceil


load_dotenv("config.env")

# Bot günlükleri kurulumu:
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

ASYNC_POOL = []

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        level=DEBUG,
        format="[%(asctime)s - %(levelname)s] - @EpicUserBot : %(message)s",
        datefmt='%d-%b-%y %H:%M:%S')
else:
    basicConfig(
        level=INFO,
        format="[%(asctime)s - %(levelname)s] - @EpicUserBot : %(message)s",
        datefmt='%d-%b-%y %H:%M:%S')
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 6:
    LOGS.info("Ən azı python 3.6 versiyanız olmalıdır."
              "Birdən çox xüsusiyyət bundan asılıdır. Bot bağlanır.")
    quit(1)

# Yapılandırmanın önceden kullanılan değişkeni kullanarak düzenlenip düzenlenmediğini kontrol edin.
# Temel olarak, yapılandırma dosyası için kontrol.
CONFIG_CHECK = os.environ.get(
    "___________Lütfən_______O_____XƏTT_____SHILLING__________", None)

if CONFIG_CHECK:
    LOGS.info(
        "Xahiş edirəm config.env faylından ilk hashtagda göstərilən sətri silin"
    )
    quit(1)

# Bot'un dili
LANGUAGE = os.environ.get("LANGUAGE", "DEFAULT").upper()

if not LANGUAGE in ["EN", "TR", "AZ", "UZ", "DEFAULT"]:
    LOGS.info("Siz naməlum bir dil yazmısınız. Buna görə DEFAULT istifadə olunur.")
    LANGUAGE = "DEFAULT"
    
# Epic versiyon
EPİC_VERSION = "v3.1"

# Telegram API KEY ve HASH
API_KEY = os.environ.get("API_KEY", None)
API_HASH = os.environ.get("API_HASH", None)
#Grouo Call 

async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call))
    return xx.call

#Sudoİd
try:
    SUDO_ID = set(int(x) for x in os.environ.get("SUDO_ID", "").split())
except ValueError:
    raise Exception("Bir istifadəçi kodu göstərməlisiniz.")

SILINEN_PLUGIN = {}
# UserBot Session String
STRING_SESSION = os.environ.get("STRING_SESSION", None)

# Kanal / Grup ID yapılandırmasını günlüğe kaydetme.
BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", None))

# UserBot günlükleme özelliği.
BOTLOG = sb(os.environ.get("BOTLOG", "False"))
LOGSPAMMER = sb(os.environ.get("LOGSPAMMER", "False"))

# Hey! Bu bir bot. Endişelenme ;)
PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN", "False"))

# Güncelleyici için Heroku hesap bilgileri.
HEROKU_MEMEZ = sb(os.environ.get("HEROKU_MEMEZ", "False"))
HEROKU_APPNAME = os.environ.get("HEROKU_APPNAME", None)
HEROKU_APIKEY = os.environ.get("HEROKU_APIKEY", None)

EZZEC = False
Heroku = None
app = None

if HEROKU_APPNAME is not None and HEROKU_APIKEY is not None:
    if EZZEC == True:
        pass
    else:
        EZZEC = True
        Heroku = heroku3.from_key(HEROKU_APIKEY)
        app = Heroku.app(HEROKU_APPNAME)
        heroku_var = app.config()
        heroku_var["UPSTREAM_REPO_URL"] = "https://github.com/ErdemBey0/EpicUserBot.git"
else:
    app = None


try:
    import randomstuff
except ModuleNotFoundError:
    install_pip("randomstuff.py")
    import randomstuff

#Chatbot için Client -- ByMisakiMey
RANDOM_STUFF_API_KEY = os.environ.get("RANDOM_STUFF_API_KEY", None)
if RANDOM_STUFF_API_KEY:
    try:
        rs_client = randomstuff.AsyncClient(api_key=RANDOM_STUFF_API_KEY, version="4")
    except:
        print('Invalid RANDOM_STUFF_API_KEY')
        rs_client = None
else:
    rs_client = None
AI_LANG = os.environ.get("AI_LANG", 'en')


# Güncelleyici için özel (fork) repo linki.
UPSTREAM_REPO_URL = "https://github.com/erdembey0/EpicUserBot.git"

# Afk mesajların iletilmesi
AFKILETME = sb(os.environ.get("AFKILETME", "True"))

# SQL Veritabanı
DB_URI = os.environ.get("DATABASE_URL", "sqlite:///epic.db")

# OCR API key
OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", None)

# remove.bg API key
REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)

# AUTO PP
AUTO_PP = os.environ.get("AUTO_PP", None)

# Warn modül
WARN_LIMIT = int(os.environ.get("WARN_LIMIT", 3))
WARN_MODE = os.environ.get("WARN_MODE", "gmute")

if not WARN_MODE in ["gmute", "gban"]:
    WARN_MODE = "gmute"

# Galeri
GALERI_SURE = int(os.environ.get("GALERI_SURE", 60))

# Chrome sürücüsü ve Google Chrome dosyaları
CHROME_DRIVER = os.environ.get("CHROME_DRIVER", None)
GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN", None)

#Time
WORKTIME = time.time()

PLUGINID = os.environ.get("PLUGIN_CHANNEL_ID", None)
# Plugin İçin
if not PLUGINID:
    PLUGIN_CHANNEL_ID = "me"
else:
    PLUGIN_CHANNEL_ID = int(PLUGINID)

# OpenWeatherMap API Key
OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)
WEATHER_DEFCITY = os.environ.get("WEATHER_DEFCITY", None)

# Anti Spambot
ANTI_SPAMBOT = sb(os.environ.get("ANTI_SPAMBOT", "False"))
ANTI_SPAMBOT_SHOUT = sb(os.environ.get("ANTI_SPAMBOT_SHOUT", "True"))

# Youtube API key
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", None)

# Saat & Tarih - Ülke ve Saat Dilimi
COUNTRY = str(os.environ.get("COUNTRY", ""))
TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))

# Sevgili :)
SEVGILI = os.environ.get("SEVGILI",None)

# Temiz Karşılama
CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME", "True"))

# Last.fm Modülü
BIO_PREFIX = os.environ.get("BIO_PREFIX", "@EpicUserBot | ")
DEFAULT_BIO = os.environ.get("DEFAULT_BIO", None)

LASTFM_API = os.environ.get("LASTFM_API", None)
LASTFM_SECRET = os.environ.get("LASTFM_SECRET", None)
LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME", None)
LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD", None)
LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)
if LASTFM_API and LASTFM_SECRET and LASTFM_USERNAME and LASTFM_PASS:
    lastfm = LastFMNetwork(api_key=LASTFM_API,
                           api_secret=LASTFM_SECRET,
                           username=LASTFM_USERNAME,
                           password_hash=LASTFM_PASS)
else:
    lastfm = None

# Google Drive Modülü
G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
G_DRIVE_AUTH_TOKEN_DATA = os.environ.get("G_DRIVE_AUTH_TOKEN_DATA", None)
GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", None)
TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY",
                                         "./downloads")

#Revert yani Klondan Sonra hesabın eski haline dönmesi
DEFAULT_NAME = os.environ.get("DEFAULT_NAME", None)

# Bazı pluginler için doğrulama
USERBOT_ = True

# Inline yardımın çalışması için
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
BOT_USERNAME = os.environ.get("BOT_USERNAME", None)

# Genius modülünün çalışması için buradan değeri alın https://genius.com/developers her ikisi de aynı değerlere sahiptir
GENIUS = os.environ.get("GENIUS", None)

CMD_HELP = {}
CMD_HELP_BOT = {}

PM_AUTO_BAN_LIMIT = int(os.environ.get("PM_AUTO_BAN_LIMIT", 4))

SPOTIFY_DC = os.environ.get("SPOTIFY_DC", None)
SPOTIFY_KEY = os.environ.get("SPOTIFY_KEY", None)

PAKET_ISMI = os.environ.get("PAKET_ISMI", "| 🌃 @EpicUserBot paket |")

# Userbotu kapatmak için gruplar
BLACKLIST_CHAT = os.environ.get("BLACKLIST_CHAT", None)

if not BLACKLIST_CHAT: #Eğer ayarlanmamışsa Epic Support grubu eklenir.
    BLACKLIST_CHAT = [-1001197341555,-1001168760410]

# Otomatik Katılma ve güncellemeler
OTOMATIK_KATILMA = sb(os.environ.get("OTOMATIK_KATILMA", "True"))
AUTO_UPDATE =  sb(os.environ.get("AUTO_UPDATE", "True"))


# Özel Pattern'ler
PATTERNS = os.environ.get("PATTERNS", ".;!,")
WHITELIST = get('https://raw.githubusercontent.com/ErdemBey0/datas/master/whitelist.json').json()

# Bot versiyon kontrolü
forceVer = []
if os.path.exists("force-surum.check"):
    os.remove("force-surum.check")
else:
    LOGS.info("force-surum.check faylı yoxdur, gətirilir ...")

URL = 'https://raw.githubusercontent.com/ErdemBey0/datas/master/force-surum.check' 
with open('force-surum.check', 'wb') as load:
    load.write(get(URL).content)

DB = connect("force-surum.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM SURUM1""")
ALL_ROWS = CURSOR.fetchall()

for i in ALL_ROWS:
    forceVer.append(i[0])
connect("force-surum.check").close() 

# CloudMail.ru ve MEGA.nz ayarlama
if not os.path.exists('bin'):
    os.mkdir('bin')

binaries = {
    "https://raw.githubusercontent.com/yshalsager/megadown/master/megadown":
    "bin/megadown",
    "https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py":
    "bin/cmrudl"
}

for binary, path in binaries.items():
    downloader = SmartDL(binary, path, progress_bar=False)
    downloader.start()
    os.chmod(path, 0o755)

from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
loop = None
# 'bot' değişkeni
if STRING_SESSION:
    # pylint: devre dışı=geçersiz ad
    bot = TelegramClient(
    StringSession(STRING_SESSION),
    API_KEY,
    API_HASH,
    loop=loop,
    connection=ConnectionTcpAbridged,
    auto_reconnect=True,
    connection_retries=None,
)
else:
    # pylint: devre dışı=geçersiz ad
    bot = TelegramClient("userbot", API_KEY, API_HASH)

ASISTAN = 1899959408 # Bot yardımcısı

if os.path.exists("learning-data-root.check"):
    os.remove("learning-data-root.check")
else:
    LOGS.info("Braincheck faylı yoxdur, gətirilir ...")

URL = 'https://raw.githubusercontent.com/ErdemBey0/datas/master/learning-data-root.check'
with open('learning-data-root.check', 'wb') as load:
    load.write(get(URL).content)
    
# async def get_call(event):
    # mm = await event.client(getchat(event.chat_id))
   # xx = await event.client(getvc(mm.full_chat.call))
   # return xx.call

async def check_botlog_chatid():
    if not BOTLOG_CHATID and LOGSPAMMER:
        LOGS.info(
            "Xüsusi səhv jurnalının işləməsi üçün BOTLOG_CHATID dəyişənini konfiqurasiyadan təyin etməlisiniz.")
        quit(1)

    elif not BOTLOG_CHATID and BOTLOG:
        LOGS.info(
            "Qeyd etmə xüsusiyyətinin işləməsi üçün BOTLOG_CHATID dəyişənini konfiqurasiyadan təyin etməlisiniz.")
        quit(1)

    elif not BOTLOG or not LOGSPAMMER:
        return

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.info(
            "Hesabınızın BOTLOG_CHATID qrupuna mesaj göndərmək icazəsi yoxdur."
            "Qrup kimliyini düzgün yazdığınızı yoxlayın.")
        quit(1)
        
if not BOT_TOKEN == None:
    tgbot = TelegramClient(
        "TG_BOT_TOKEN",
        api_id=API_KEY,
        api_hash=API_HASH
    ).start(bot_token=BOT_TOKEN)
else:
    tgbot = None

def butonlastir(sayfa, moduller):
    Satir = 5
    Kolon = 2
    
    moduller = sorted([modul for modul in moduller if not modul.startswith("_")])
    pairs = list(map(list, zip(moduller[::2], moduller[1::2])))
    if len(moduller) % 2 == 1:
        pairs.append([moduller[-1]])
    max_pages = ceil(len(pairs) / Satir)
    pairs = [pairs[i:i + Satir] for i in range(0, len(pairs), Satir)]
    butonlar = []
    for pairs in pairs[sayfa]:
        butonlar.append([
            custom.Button.inline("🔸 " + pair, data=f"bilgi[{sayfa}]({pair})") for pair in pairs
        ])

    butonlar.append([custom.Button.inline("◀️ Geri", data=f"sayfa({(max_pages - 1) if sayfa == 0 else (sayfa - 1)})"), custom.Button.inline("İleri ▶️", data=f"sayfa({0 if sayfa == (max_pages - 1) else sayfa + 1})")])
    return [max_pages, butonlar]

with bot:


    try:
        bot(LeaveChannelRequest("@SiriSupport"))
        bot(LeaveChannelRequest("@SiriOT"))
        bot(LeaveChannelRequest("@Siriaddon"))
        bot(JoinChannelRequest("@EpicUserBot"))
        bot(JoinChannelRequest("@HydraDestek"))
        if OTOMATIK_KATILMA:
            bot(JoinChannelRequest("@HydraDev"))
            bot(JoinChannelRequest("@EpicPlugin"))
    except:
        pass

    moduller = CMD_HELP

    me = bot.get_me()
    uid = me.id

    try:
        @tgbot.on(NewMessage(pattern='/start'))
        async def start_bot_handler(event):
            if not event.message.from_id == uid:
                await event.reply(f'`Salam, mən  @EpicUserBot`am! Sahibimə kömək etmək üçün buradayam (`@ @ me.username}`), ona görə sizə kömək edə bilmərəm: / Ancaq bir dastan da aça bilərsiniz; Kanalı yoxlayın `@EpicUserBot')
            else:
                await event.reply(f'`Tengri save Turks! Epic working... `')

        @tgbot.on(InlineQuery)  # pylint:disable=E0602
        async def inline_handler(event):
            builder = event.builder
            result = None
            query = event.text
            if event.query.user_id == uid and query == "@EpicUserBot":
                rev_text = query[::-1]
                veriler = (butonlastir(0, sorted(CMD_HELP)))
                result = await builder.article(
                    f"Xahiş edirəm yalnız .help əmri ilə istifadə edin",
                    text=f"** Ən Qabaqcıl İstifadəçi Botu! ** [Epik] (https://t.me/EpicUserBot) __İşləmə ...__ \ n \ n ** Qurulmuş Modulların Sayı: ** `{len (CMD_HELP)}" \ n * * Səhifə: ** 1 / {məlumat [0]}",
                    buttons=veriler[1],
                    link_preview=False
                )
            elif query.startswith("http"):
                parca = query.split(" ")
                result = builder.article(
                    "Fayl yükləndi",
                    text=f"**Fayl uğurla başa çatıb {parca[2]} sayta yükləndi!**\n\nYükləmə vaxtı: {parca[1][:3]} saniye\n[‏‏‎ ‎]({parca[0]})",
                    buttons=[
                        [custom.Button.url('URL', parca[0])]
                    ],
                    link_preview=True
                )
            else:
                result = builder.article(
                    "@EpicUserBot",
                    text="""@EpicUserBot istifadə edin!
Hesabınızı botlara çevirə və istifadə edə bilərsiniz. Bütün quraşdırma detalları aşağıda GitHub-da izah olunur.""",
                    buttons=[
                        [custom.Button.url("Kanala qoşulun", "https://t.me/EpicUserBot"), custom.Button.url(
                            "Qrupa qoşulun", "https://t.me/HydraDestek")],
                        [custom.Button.url(
                            "GitHub", "https://github.com/ErdemBey0/EpicUserBot")]
                    ],
                    link_preview=False
                )
            await event.answer([result] if result else None)

        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"sayfa\((.+?)\)")))
        async def sayfa(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌ Hey! Yazılarımı düzəltməyə çalışmayın! Özünüzə @EpicUserBot yaradın.", cache_time=0, alert=True)
            sayfa = int(event.data_match.group(1).decode("UTF-8"))
            veriler = butonlastir(sayfa, CMD_HELP)
            await event.edit(
                f"** Ən Qabaqcıl İstifadəçi Botu! ** [Epik] (https://t.me/EpicUserBot) __İşləmə ...__ \ n \ n ** Qurulmuş Modulların Sayı: ** `{len (CMD_HELP)}" \ n * * Səhifə: ** 1 / {məlumat [0]}",
                buttons=veriler[1],
                link_preview=False
            )
        
        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"bilgi\[(\d*)\]\((.*)\)")))
        async def bilgi(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌ Hey! Yazılarımı düzəltməyə çalışmayın! Özünüzə @EpicUserBot yaradın.", cache_time=0, alert=True)

            sayfa = int(event.data_match.group(1).decode("UTF-8"))
            komut = event.data_match.group(2).decode("UTF-8")
            try:
                butonlar = [custom.Button.inline("🔹 " + cmd[0], data=f"komut[{komut}[{sayfa}]]({cmd[0]})") for cmd in CMD_HELP_BOT[komut]['commands'].items()]
            except KeyError:
                return await event.answer("❌Bu modul üçün heç bir şərh yazılmamışdır..", cache_time=0, alert=True)

            butonlar = [butonlar[i:i + 2] for i in range(0, len(butonlar), 2)]
            butonlar.append([custom.Button.inline("◀️ Geri", data=f"sayfa({sayfa})")])
            await event.edit(
                f"**📗 Fayl:** `{komut}`\n**🔢 qomut Sayısı:** `{len(CMD_HELP_BOT[komut]['commands'])}`",
                buttons=butonlar,
                link_preview=False
            )
        
        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"komut\[(.*)\[(\d*)\]\]\((.*)\)")))
        async def komut(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌ Hey! Yazılarımı düzəltməyə çalışmayın! Özünüzə @EpicUserBot yaradın.", cache_time=0, alert=True)

            cmd = event.data_match.group(1).decode("UTF-8")
            sayfa = int(event.data_match.group(2).decode("UTF-8"))
            komut = event.data_match.group(3).decode("UTF-8")

            result = f"**📗 Fayl:** `{cmd}`\n"
            if CMD_HELP_BOT[cmd]['info']['info'] == '':
                if not CMD_HELP_BOT[cmd]['info']['warning'] == '':
                    result += f"**⬇️ Official:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n"
                    result += f"**⚠️ Xəbərdarlıq:** {CMD_HELP_BOT[cmd]['info']['warning']}\n\n"
                else:
                    result += f"**⬇️ Official:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n\n"
            else:
                result += f"**⬇️ Official:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n"
                if not CMD_HELP_BOT[cmd]['info']['warning'] == '':
                    result += f"**⚠️ Xəbərdarlıq:** {CMD_HELP_BOT[cmd]['info']['warning']}\n"
                result += f"**ℹ️ Info:** {CMD_HELP_BOT[cmd]['info']['info']}\n\n"

            command = CMD_HELP_BOT[cmd]['commands'][komut]
            if command['params'] is None:
                result += f"**🛠 əmr:** `{PATTERNS[:1]}{command['command']}`\n"
            else:
                result += f"**🛠 əmr:** `{PATTERNS[:1]}{command['command']} {command['params']}`\n"
                
            if command['example'] is None:
                result += f"**💬 İzahat:** `{command['usage']}`\n\n"
            else:
                result += f"**💬 İzahat:** `{command['usage']}`\n"
                result += f"**⌨️ Misal:** `{PATTERNS[:1]}{command['example']}`\n\n"

            await event.edit(
                result,
                buttons=[custom.Button.inline("◀️ Geri", data=f"bilgi[{sayfa}]({cmd})")],
                link_preview=False
            )
    except Exception as e:
        print(e)
        LOGS.info(
            "Satır daxilində dəstək botunuzda deaktivdir."
            "Aktivləşdirmək üçün bir bot işarəsi təyin edin və botunuzda satır içi rejimini aktivləşdirin."
            "Bunun xaricində başqa bir problem olduğunu düşünürsənsə, t.me/HydraSupport ilə bizimlə əlaqə qur."
        )

    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except:
        LOGS.info(
            "BOTLOG_CHATID mühit dəyişəni etibarlı bir şəxs deyil."
            "Ətraf mühit dəyişənlərini / config.env faylını yoxlayın."
        )
        quit(1)


# Küresel Değişkenler
SON_GORULME = 0
COUNT_MSG = 0
USERS = {}
MYID = uid
ForceVer = int(forceVer[0])
BRAIN_CHECKER = []
COUNT_PM = {}
LASTMSG = {}
FUP = True
ENABLE_KILLME = True
ISAFK = False
AFKREASON = None
ZALG_LIST = [[
    "̖",
    " ̗",
    " ̘",
    " ̙",
    " ̜",
    " ̝",
    " ̞",
    " ̟",
    " ̠",
    " ̤",
    " ̥",
    " ̦",
    " ̩",
    " ̪",
    " ̫",
    " ̬",
    " ̭",
    " ̮",
    " ̯",
    " ̰",
    " ̱",
    " ̲",
    " ̳",
    " ̹",
    " ̺",
    " ̻",
    " ̼",
    " ͅ",
    " ͇",
    " ͈",
    " ͉",
    " ͍",
    " ͎",
    " ͓",
    " ͔",
    " ͕",
    " ͖",
    " ͙",
    " ͚",
    " ",
],
    [
    " ̍", " ̎", " ̄", " ̅", " ̿", " ̑", " ̆", " ̐", " ͒", " ͗",
    " ͑", " ̇", " ̈", " ̊", " ͂", " ̓", " ̈́", " ͊", " ͋", " ͌",
    " ̃", " ̂", " ̌", " ͐", " ́", " ̋", " ̏", " ̽", " ̉", " ͣ",
    " ͤ", " ͥ", " ͦ", " ͧ", " ͨ", " ͩ", " ͪ", " ͫ", " ͬ", " ͭ",
    " ͮ", " ͯ", " ̾", " ͛", " ͆", " ̚"
],
    [
    " ̕",
    " ̛",
    " ̀",
    " ́",
    " ͘",
    " ̡",
    " ̢",
    " ̧",
    " ̨",
    " ̴",
    " ̵",
    " ̶",
    " ͜",
    " ͝",
    " ͞",
    " ͟",
    " ͠",
    " ͢",
    " ̸",
    " ̷",
    " ͡",
]]