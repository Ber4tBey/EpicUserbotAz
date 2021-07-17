""" UserBot başlangıç noktası """
import importlib
from importlib import import_module
from sqlite3 import connect
import os
import requests
from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.tl.functions.channels import GetMessagesRequest
from . import BRAIN_CHECKER, LOGS, bot, PLUGIN_CHANNEL_ID, CMD_HELP, LANGUAGE, EPİC_VERSION, PATTERNS
from .modules import ALL_MODULES
import userbot.modules.sql_helper.mesaj_sql as MSJ_SQL
import userbot.modules.sql_helper.galeri_sql as GALERI_SQL
from pySmartDL import SmartDL
from telethon.tl import functions

from random import choice
import chromedriver_autoinstaller
from json import loads, JSONDecodeError
import re
import userbot.cmdhelp

ALIVE_MSG = [
    "`Userbotunuz işləyir və sizə bir şey demək istəyir .. mən sizi sevirəm` **{epicsahip}** ❤️",
    "🎆 `Narahat olma! Mən səni tək qoymaram.` **{epicsahip}**, `EpicUserbot işləyir.`",
    "`⛈️ Əlimdən gələni etməyə hazıram`, **{epicsahip}**",
    "✨ `EpicUserBot sahibinin sifarişi ilə hazırdır...`",
    "`Ən qabaqcıl istifadəçi tərəfindən düzəldilmiş mesajı hazırda oxumalısınız` **{epicsahip}**.",
    "`Mənə zəng etdiniz ❓ Buradayam Narahat olma`"
]

DIZCILIK_STR = [
    "Etiketi darıxıram ...",
    "Oğurladım və getdi, yaxşılaş🤭",
    "Yaşasın dızcılık...",
    "Bu stikeri öz paketimə dəvət edirəm...",
    "Bunu asmaq lazımdır...",
    "Hey bu çox gözəl bir stiker! \ NMən dərhal hirslənirəm ..",
    "Çıkartmanı dızlıyorum\nhahaha.",
    "Hey oraya bax. (☉｡☉)!→\nmen bunu dızlarken...",
    "Qızılgüllər qırmızı bənövşələr mavidir, bu stikeri paketimə yapışdırıb sərinləşərəm ...",
    "Etiket həbs olunur ...",
    "Cənab jester bu stikeri sızlayır ... ",
    "Niyə bu gözəl etiket mənim paketimdə olmasın?🤭",
]

AFKSTR = [
    "Mən indi tələsirəm, sonra mesaj yaza bilərsiniz? Onsuz da yenə gələcəm.",
    "Zəng etdiyiniz şəxs hazırda telefona cavab verə bilmir. Tondan sonra mesajınızı öz tarifinizdə buraxa bilərsiniz. Mesaj haqqı 49 sentdir. \ n`biiiiiiiiiiiiiiiiiiiiiiiiiiiiiip`!",
    "Bir neçə dəqiqəyə qayıdacağam. Ancaq gəlməsəm ... daha gözləməyin.",
    "Mən hazırda burada deyiləm, amma yəqin ki, başqa bir yerdəyəm.",
    "Qızılgüllər qırmızı \nVolletlər mavi \nMənə bir mesaj verin \nVə sizinlə görüşəcəyəm.",
    "Bəzən həyatda ən yaxşı şeyləri gözləməyə dəyər ... \n Geri dönəcəyəm.",
    "Mən dərhal qayıdacağam, amma qayıtmasam, daha sonra qayıdacağam.",
    "Hələ başa düşməmisinizsə, \ nMən burada deyiləm.",
    "Salam, uzaq mesajıma xoş gəldiniz, bu gün sizi necə görməməzlikdən gələ bilərəm?",
    "7 dənizdən və 7 ölkədən, \n7 su və 7 qitədən, \n7 dağ və 7 təpədən, \n7 düzənlik və 7 kurqandan, \n7 hovuz və 7 göldən, \n7 bulaq və 7 çəmənlikdən, \n7 şəhərdən və 7-dən uzağam. məhəllələr, \n n7 məhəllə və 7 ev ... \n \nM mesajların belə mənə çatmadığı yer!",
    "Mən hazırda klaviaturadan uzağam, ancaq ekranda kifayət qədər yüksək səslə qışqırırsansa, səni eşidirəm.",
    "Aşağıdakı istiqamətdə irəliləyirəm \ n ---->",
    "Bu istiqamətdə irəliləyir\n<----",
    "Xahiş edirəm bir mesaj buraxın və mənə özümü indiki olduğumdan daha vacib hiss etdim.",
    "Sahibim burada deyil, mənə yazmağı dayandır.",
    "Burada olsaydım \n sənə harada olduğumu deyərdim. \n \nAmma bu mən deyiləm, qayıdandan sonra məni boğ ...",
    "Uzaqdayam! \nə vaxt qayıdacağımı bilmirəm! \nÜmid edirəm bir neçə dəqiqədən sonra!",
    "Mənim sahibim hazırda əlçatan deyil. Adınızı, nömrənizi və ünvanınızı versəniz, onu ona ötürə bilərəm ki, qayıdandan sonra.",
    "Bağışlayın, sahibim burada deyil. \nGələnə qədər mənimlə danışa bilərsiniz. \nMənim sahibim daha sonra sizinlə əlaqə saxlayacaq.",
    "Güman edirəm ki, bir mesaj gözləyirdiniz!",
    "Həyat çox qısadır, ediləcək çox şey var ... \nBundan birini edirəm ...",
    "Mən indi burda deyiləm .... \namma mən olsam ... \n \nböyük olmazdımı?",
    "Məni xatırladığınıza görə sevinirəm, amma hazırda klaviatura mənim üçün çox uzaqdır",
    "Bəlkə yaxşıyam, bəlkə pisəm, bilmirsən amma AFK olduğumu görə bilərsən"
]


KICKME_MSG = [
    "güle güle gedirəm 👋🏻",
    "Mən səssizcə gedirəm 🥴",
    "Səndən xəbərsiz ayrılsam, bir gün qrupda olmadığımı başa düşəcəksən .. Bu səbəbdən bu mesajı tərk edirəm I'm",
    "Mən indi buranı tərk etməliyəm🤭"
]


UNAPPROVED_MSG = ("`Hey olduğun yerdə qal! 👨‍💻 Mən epikəm. Narahat olma!\n\n`"
                  "`Sahibim sənə mesaj göndərməyimə icazə vermədi ki, sahibim səni təsdiqləyənə qədər bu mesajı alasan .. `"
                  "`Xahiş edirəm sahibimin aktiv olmasını gözləyin, ümumiyyətlə PM-ləri təsdiqləyir.\n\n`"
                  "`Bildiyim qədəri ilə PM-yə dəli insanlara icazə vermir.`")

DB = connect("learning-data-root.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()


INVALID_PH = '\nXATA: Girilən telefon nömrəsi etibarsızdır' \
             '\n  İpucu: Ölkə kodunu istifadə edərək nömrənizi daxil edin' \
             '\n   Telefon nömrənizi yenidən yoxlayın'

for i in ALL_ROWS:
    BRAIN_CHECKER.append(i[0])
connect("learning-data-root.check").close()
BRAIN_CHECKER = BRAIN_CHECKER[0]

def extractCommands(file):
    FileRead = open(file, 'r').read()
    
    if '/' in file:
        file = file.split('/')[-1]

    Pattern = re.findall(r"@register\(.*pattern=(r|)\"(.*)\".*\)", FileRead)
    Komutlar = []

    if re.search(r'CmdHelp\(.*\)', FileRead):
        pass
    else:
        dosyaAdi = file.replace('.py', '')
        CmdHelp = userbot.cmdhelp.CmdHelp(dosyaAdi, False)

        # Komutları Alıyoruz #
        for Command in Pattern:
            Command = Command[1]
            if Command == '' or len(Command) <= 1:
                continue
            Komut = re.findall("(^.*[a-zA-Z0-9şğüöçı]\w)", Command)
            if (len(Komut) >= 1) and (not Komut[0] == ''):
                Komut = Komut[0]
                if Komut[0] == '^':
                    KomutStr = Komut[1:]
                    if KomutStr[0] == '.':
                        KomutStr = KomutStr[1:]
                    Komutlar.append(KomutStr)
                else:
                    if Command[0] == '^':
                        KomutStr = Command[1:]
                        if KomutStr[0] == '.':
                            KomutStr = KomutStr[1:]
                        else:
                            KomutStr = Command
                        Komutlar.append(KomutStr)

            # EPİCPY
            Epicpy = re.search('\"\"\"EPİCPY(.*)\"\"\"', FileRead, re.DOTALL)
            if not Epicpy == None:
                Epicpy = Epicpy.group(0)
                for Satir in Epicpy.splitlines():
                    if (not '"""' in Satir) and (':' in Satir):
                        Satir = Satir.split(':')
                        Isim = Satir[0]
                        Deger = Satir[1][1:]
                                
                        if Isim == 'INFO':
                            CmdHelp.add_info(Deger)
                        elif Isim == 'WARN':
                            CmdHelp.add_warning(Deger)
                        else:
                            CmdHelp.set_file_info(Isim, Deger)
            for Komut in Komutlar:
                # if re.search('\[(\w*)\]', Komut):
                    # Komut = re.sub('(?<=\[.)[A-Za-z0-9_]*\]', '', Komut).replace('[', '')
                CmdHelp.add_command(Komut, None, 'Bu plagin xaricdən yüklənir. Heç bir izahat təyin olunmayıb.')
            CmdHelp.add()

try:
    bot.start()
    idim = bot.get_me().id
    epicbl = requests.get('https://raw.githubusercontent.com/ErdemBey0/datas/master/blacklist.json').json()
    if idim in epicbl:
        bot.send_message("me", f"`❌ Epic administratorları sizə bot qadağan etdilər! Bot bağlanır ...`")
        LOGS.error("Epic adminləri sizə bot qadağan etdilər! Bot bağlanır ...")
        bot.disconnect()
    # ChromeDriver'ı Ayarlayalım #
    try:
        chromedriver_autoinstaller.install()
    except:
        pass
    
    # Galeri için değerler
    GALERI = {}

    # PLUGIN MESAJLARI AYARLIYORUZ
    PLUGIN_MESAJLAR = {}
    ORJ_PLUGIN_MESAJLAR = {"alive": f"{str(choice(ALIVE_MSG))}", "afk": f"`{str(choice(AFKSTR))}`", "kickme": f"`{str(choice(KICKME_MSG))}`", "pm": str(UNAPPROVED_MSG), "dızcı": str(choice(DIZCILIK_STR)), "ban": "🌀 {mention}`, Banlandı!!`", "mute": "🌀 {mention}`, sessize alındı!`", "approve": "`Merhaba` {mention}`, artık bana mesaj gönderebilirsin!`", "disapprove": "{mention}`, artık bana mesaj gönderemezsin!`", "block": "{mention}`, bunu bana mecbur bıraktın! Seni engelledim!`"}


    PLUGIN_MESAJLAR_TURLER = ["alive", "afk", "kickme", "pm", "dızcı", "ban", "mute", "approve", "disapprove", "block",]
    for mesaj in PLUGIN_MESAJLAR_TURLER:
        dmsj = MSJ_SQL.getir_mesaj(mesaj)
        if dmsj == False:
            PLUGIN_MESAJLAR[mesaj] = ORJ_PLUGIN_MESAJLAR[mesaj]
        else:
            if dmsj.startswith("MEDYA_"):
                medya = int(dmsj.split("MEDYA_")[1])
                medya = bot.get_messages(PLUGIN_CHANNEL_ID, ids=medya)

                PLUGIN_MESAJLAR[mesaj] = medya
            else:
                PLUGIN_MESAJLAR[mesaj] = dmsj
    if not PLUGIN_CHANNEL_ID == None:
        LOGS.info("🔄Plugins yüklənir ..")
        try:
            KanalId = bot.get_entity(PLUGIN_CHANNEL_ID)
        except:
            KanalId = "me"

        for plugin in bot.iter_messages(KanalId, filter=InputMessagesFilterDocument):
            if plugin.file.name and (len(plugin.file.name.split('.')) > 1) \
                and plugin.file.name.split('.')[-1] == 'py':
                Split = plugin.file.name.split('.')

                if not os.path.exists("./userbot/modules/" + plugin.file.name):
                    dosya = bot.download_media(plugin, "./userbot/modules/")
                else:
                    LOGS.info("Bu Plugin Onsuz quraşdırılıb " + plugin.file.name)
                    extractCommands('./userbot/modules/' + plugin.file.name)
                    dosya = plugin.file.name
                    continue 
                
                try:
                    spec = importlib.util.spec_from_file_location("userbot.modules." + Split[0], dosya)
                    mod = importlib.util.module_from_spec(spec)

                    spec.loader.exec_module(mod)
                except Exception as e:
                    LOGS.info(f"`[×] Yükləmə alınmadı! Plugin Yanlış !! \ n \ nXəta: {e}`")

                    try:
                        plugin.delete()
                    except:
                        pass

                    if os.path.exists("./userbot/modules/" + plugin.file.name):
                        os.remove("./userbot/modules/" + plugin.file.name)
                    continue
                extractCommands('./userbot/modules/' + plugin.file.name)
    else:
        bot.send_message("me", f"`Lütfən, plaginləri qalıcı etmək üçün PLUGIN_CHANNEL_ID ayarlayın.`")
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

async def FotoDegistir (foto):
    FOTOURL = GALERI_SQL.TUM_GALERI[foto].foto
    r = requests.get(FOTOURL)

    with open(str(foto) + ".jpg", 'wb') as f:
        f.write(r.content)    
    file = await bot.upload_file(str(foto) + ".jpg")
    try:
        await bot(functions.photos.UploadProfilePhotoRequest(
            file
        ))
        return True
    except:
        return False

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

os.system("clear")

LOGS.info("+===========================================================+")
LOGS.info("|                     ✨Epic Userbot✨                       |")
LOGS.info("+==============+==============+==============+==============+")
LOGS.info("|                                                            |")
LOGS.info("Botunuz işləyir! Hər hansı bir söhbətə .alive yazaraq test edin."
          " Yardıma ehtiyacınız varsa, t.me/HydraSupport ünvanındakı Dəstək qrupumuza gəlin")
LOGS.info(f"Bot versiyanız: Epic {EPİC_VERSION}")

"""
if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
"""
bot.run_until_disconnected()
