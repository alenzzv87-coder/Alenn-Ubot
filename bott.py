from telethon import TelegramClient, events, types
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from datetime import datetime, timedelta
from gtts import gTTS
import pytz
import os
import asyncio
import time
import io
import re

# --- BANNER UBOT (SANGAR STYLE) ---
BANNER = """
 ████        ████  ████████   ███████   ████████ 
 ████        ████  █████████ █████████  █████████
 ████        ████  ███   ███ ███   ███     ███   
 ████        ████  ████████  ███   ███     ███   
 ████        ████  █████████ ███   ███     ███   
 ████        ████  ███   ███ ███   ███     ███   
 ██████████  ████  █████████ █████████     ███   
  █████████  ████  ████████   ███████      ███   
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ✠ ALENZZ PREMIUM USERBOT SYSTEM ✠
        ✠ OWNER: @alenzzxiter | VER: 1.2.5 ✠
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# --- DATA KONFIGURASI ---
api_id = 39479371 
api_hash = '53d69c3a785f66b07e31b57f7153071b'
admin_id = 'alenzzxiter' 
channel_username = 'alenzzvip' 
group_link = 'https://t.me/+TdZ6hg77RWliY2E1' 

# --- DATA RUNTIME ---
already_replied = set() 
bot_active = True 
anti_link_active = True # Default On
TIMEZONE = pytz.timezone('Asia/Jakarta')

# --- SISTEM 24 JAM (JAM TUTUP DIHAPUS) ---
def is_istirahat():
    return False # Selalu False agar bot jalan 24 jam penuh

bot = TelegramClient('alenzz_userbot', api_id, api_hash).start()

# --- FITUR TAMBAHAN: HELP LIST ---
@bot.on(events.NewMessage(outgoing=True, pattern=r'^\.list$'))
async def help_list(event):
    help_text = """
╔════════════════════╗
  📊 **ALENZZ USERBOT MENU** 📊
╚════════════════════╝
🚀 **CORE SKILLS:**
• `.bc`      📡 (Reply) Mass Broadcast
• `.ping`    🏓 Check Speed
• `.id`      🆔 Get Chat/User ID
• `.tts`     🗣️ (Reply) Google Voice
• `.on`      🟢 Enable System
• `.off`     🔴 Disable System

🛡️ **SECURITY:**
• `.antilink on/off` 🔗 Anti Link Grup

🛠️ **ADMIN SKILLS:**
• `.ban`     🚫 (Reply) Kick & Ban
• `.unban`   ✅ (Reply) Lift Ban
• `.mute`    🔇 (Reply) Silence
• `.unmute`  🔊 (Reply) Restore

ℹ️ **OTHERS:**
• `.list`    📑 Show this Menu
━━━━━━━━━━━━━━━━━━━━━━
🔥 **VER: 1.2.5** | **@alenzzxiter**
"""
    await event.edit(help_text)

# --- SECURITY SKILLS: ANTI LINK ---

@bot.on(events.NewMessage(outgoing=True, pattern=r'^\.antilink (on|off)$'))
async def set_antilink(event):
    global anti_link_active
    mode = event.pattern_match.group(1)
    if mode == "on":
        anti_link_active = True
        await event.edit("🛡️ **ANTI-LINK SYSTEM**\n━━━━━━━━━━━━━━━━━━━━━━\n✅ **Status:** `ENABLED`\n⚡ **Mode:** `Auto-Clean Active`\n━━━━━━━━━━━━━━━━━━━━━━")
    else:
        anti_link_active = False
        await event.edit("🔓 **ANTI-LINK SYSTEM**\n━━━━━━━━━━━━━━━━━━━━━━\n⚠️ **Status:** `DISABLED`\n⚡ **Mode:** `Free Mode`\n━━━━━━━━━━━━━━━━━━━━━━")

@bot.on(events.NewMessage(incoming=True))
async def anti_link_handler(event):
    if not anti_link_active or not event.is_group:
        return
    
    if re.search(r'(https?://[^\s]+|t\.me/[^\s]+)', event.raw_text):
        sender = await event.get_sender()
        if isinstance(sender, types.User) and sender.username == admin_id:
            return
            
        try:
            await event.delete()
            warn = await event.respond(f"⚔️ **ALENZZ SECURITY** ⚔️\n━━━━━━━━━━━━━━━━━━━━━━\n⚠️ **WARNING:** `NO LINK ALLOWED!`\n👤 **User:** {sender.first_name}\n🚫 **Action:** `Message Deleted`\n━━━━━━━━━━━━━━━━━━━━━━")
            await asyncio.sleep(5)
            await warn.delete()
        except:
            pass

# --- CORE SKILLS ---

@bot.on(events.NewMessage(outgoing=True, pattern=r'^\.on$'))
async def system_on(event):
    global bot_active
    bot_active = True
    await event.edit("◈───────────────◈\n       🟢 **SYSTEM ENABLED**\n◈───────────────◈\n📡 **Status:** `Online`\n🔋 **Power:** `Full Mode`\n◈───────────────◈")

@bot.on(events.NewMessage(outgoing=True, pattern=r'^\.off$'))
async def system_off(event):
    global bot_active
    bot_active = False
    await event.edit("◈───────────────◈\n       🔴 **SYSTEM DISABLED**\n◈───────────────◈\n📡 **Status:** `Offline`\n💤 **Mode:** `Sleep Mode`\n◈───────────────◈")

@bot.on(events.NewMessage(outgoing=True, pattern=r'^\.bc$'))
async def broadcast(event):
    if not bot_active: return
    if not event.is_reply: return await event.edit("❌ **ERROR:** `Mohon reply ke pesan!`")
    reply_msg = await event.get_reply_message()
    await event.edit("📡 **BROADCAST SYSTEM**\n━━━━━━━━━━━━━━━━━━━━━━\n🚀 **Status:** `In Progress...`\n🎯 **Target:** `All Dialogs`\n━━━━━━━━━━━━━━━━━━━━━━")
    count = 0
    async for dialog in bot.iter_dialogs():
        if dialog.is_user or dialog.is_group:
            try:
                await bot.copy_messages(dialog.id, reply_msg)
                count += 1
                await asyncio.sleep(0.3)
            except: continue
    await event.edit(f"✅ **BROADCAST SUCCESS**\n━━━━━━━━━━━━━━━━━━━━━━\n📊 **Total Delivered:** `{count}`\n✨ **Powered by:** `AlenzzVip`\n━━━━━━━━━━━━━━━━━━━━━━")

# --- FITUR PING ---
@bot.on(events.NewMessage(outgoing=True, pattern=r'^\.ping$'))
async def ping(event):
    if not bot_active: return
    start = datetime.now()
    await event.edit("🚀")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(f"🚀 **PONG!!**\n━━━━━━━━━━━━━━━━━━━━━━\n⏱️ **Latency:** `{ms}ms`\n⚙️ **Engine:** `Premium v1.2.5`\n━━━━━━━━━━━━━━━━━━━━━━")

# --- FITUR CEK ID ---
@bot.on(events.NewMessage(outgoing=True, pattern=r'^\.id$'))
async def get_id(event):
    if not bot_active: return
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        target_id = reply_msg.sender_id
        chat_id = event.chat_id
        await event.edit(f"🆔 **ID INFORMATION**\n━━━━━━━━━━━━━━━━━━━━━━\n👤 **User ID:** `{target_id}`\n📍 **Chat ID:** `{chat_id}`\n━━━━━━━━━━━━━━━━━━━━━━")
    else:
        chat_id = event.chat_id
        my_id = event.sender_id
        await event.edit(f"🆔 **ID INFORMATION**\n━━━━━━━━━━━━━━━━━━━━━━\n🙋‍♂️ **My ID:** `{my_id}`\n📍 **Chat ID:** `{chat_id}`\n━━━━━━━━━━━━━━━━━━━━━━")

@bot.on(events.NewMessage(outgoing=True, pattern=r'^\.tts(?: |$)(.*)'))
async def tts_gen(event):
    if not bot_active: return
    text = event.pattern_match.group(1) or (await event.get_reply_message()).raw_text if event.is_reply else None
    if not text: return await event.edit("❌ **ERROR:** `Teks tidak ditemukan!`")
    await event.edit("🎙️ **GENERATING VOICE...**")
    try:
        fp = io.BytesIO()
        gTTS(text, lang='id').write_to_fp(fp)
        fp.seek(0)
        await bot.send_file(event.chat_id, fp, voice_note=True, reply_to=event.reply_to_msg_id)
        await event.delete()
    except Exception as e: await event.edit(f"❌ **FAILED:** `{e}`")

# --- ADMIN SKILLS ---

@bot.on(events.NewMessage(outgoing=True, pattern=r'^\.(ban|unban|mute|unmute)'))
async def admin_tools(event):
    if not bot_active: return
    cmd = event.pattern_match.group(1)
    if not event.is_reply: return await event.edit("❌ **ERROR:** `Reply targetnya!`")
    reply = await event.get_reply_message()
    try:
        if cmd == "ban":
            await bot(EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None, view_messages=True)))
        elif cmd == "unban":
            await bot(EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None, view_messages=False)))
        elif cmd == "mute":
            await bot(EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None, send_messages=True)))
        elif cmd == "unmute":
            await bot(EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None, send_messages=False)))
        await event.edit(f"⚔️ **ADMIN EXECUTION** ⚔️\n━━━━━━━━━━━━━━━━━━━━━━\n✅ **Action:** `{cmd.upper()}`\n👤 **Target:** `{reply.sender_id}`\n🛡️ **Status:** `Success`\n━━━━━━━━━━━━━━━━━━━━━━")
    except Exception as e: await event.edit(f"❌ **FAILED:** `{e}`")

# --- AUTO REPLY PM ---
@bot.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def auto_reply_pm(event):
    if not bot_active or is_istirahat(): return 
    sender = await event.get_sender()
    if isinstance(sender, types.User) and not sender.is_self:
        if sender.id in already_replied: return
        try:
            pesan_pm = (
                f"⚡ **ALENZZ AUTO-RESPONSE** ⚡\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👋 **HELLO {sender.first_name.upper()}!**\n\n"
                f"Owner sedang **OFFLINE / DEVELOPING** 💻.\n"
                f"Pesan Anda telah diterima, mohon tunggu.\n\n"
                f"🚀 **OFFICIAL INFO:**\n"
                f"• Channel: @{channel_username}\n"
                f"• Grup: [Click Here]({group_link})\n\n"
                f"🛡️ *System Secure Powered by AlenzzVip*"
                f"\n━━━━━━━━━━━━━━━━━━━━━━"
            )
            await event.reply(pesan_pm, link_preview=False)
            already_replied.add(sender.id)
        except: pass

# --- START SYSTEM ---
os.system('clear')
print(BANNER)
print(f" [📡] CONNECTION     : ESTABLISHED")
print(f" [🔐] API AUTH       : SUCCESSFUL [ID: {api_id}]")
print(f" [🐙] GITHUB REPO    : https://github.com/alenzzv87-coder/Alenn-Ubot.git")
print(f" [🛠️] BUILD VERSION  : v1.2.5-STABLE")
print(f" [🌍] REGION/TZ      : {TIMEZONE}")
print(f" [🔋] SYSTEM STATUS  : 🟢 OPERATIONAL (24H MODE)")
print(f" [🛡️] ANTI-LINK      : {'ENABLED' if anti_link_active else 'DISABLED'}")
print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f" [!] SYSTEM IS NOW LIVE 24/7. WAITING FOR COMMANDS...")
bot.run_until_disconnected()
