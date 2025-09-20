# Yui 的 Discord BOT
# 版本號 20250314_1

import discord
import requests
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
import os
from discord import app_commands
from discord.ext import commands
from typing import Optional
import math
import asyncio
import re

def timeswifter(hour, minute):
    if minute >= 60:
        hour += int(minute / 60)
        minute = minute % 60
    if hour >= 24:
        hour -= 24
    return [hour, minute]

def numadjuster(num):
    if num < 10:
        result = "0" + str(num)
    else:
        result = str(num)
    return result

scheduler = AsyncIOScheduler()

# Token
token = os.getenv("DISCORD_BOT_TOKEN")
OWNER_ID = 475310606744813580

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='☃︎', intents = intents)

WEB_APP_URL_IE = 'https://script.google.com/macros/s/AKfycbw74p5G4AWwxFbhoqgyez-ska4vm9gu-0u6lKJGdpFSRjzx4OpE_AeQX1mw_H52VujU/exec'
WEB_APP_URL_RTS = 'https://script.google.com/macros/s/AKfycbzhkPkyTt9wcn0ktMDV0GU6Z6Q-JmAEet4i8Gz9YsRAsDc8h2xAQJNqDb-1UtXjsHd0NA/exec'

@bot.event
async def on_ready():
    if not scheduler.running:
        scheduler.start()
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("You do not have the permission to use this command.")
    else:
        await ctx.send(f"An error occurred: {error}")

@bot.tree.command(name = "shutdown", description = "將BOT關機")
@app_commands.default_permissions(administrator=True)
@app_commands.describe()
async def shutdown(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("⛔ 你沒有權限使用這個指令！", ephemeral=True)
        return
    await interaction.response.send_message("Logging out...")
    await bot.close()

@bot.tree.command(name = "income", description = "記帳：收入")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(date="記錄日期（格式：YYYYMMDD 或 MMDD，不填則為今天）", item = "描述這筆收入項目（Ex：Lunch）", letter_i = "這筆收入項目的種類（以字母簡寫）", number_i = "金額")
async def income(interaction: discord.Interaction, date: Optional[str], item: str, letter_i: str, number_i: int):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("⛔ 你沒有權限使用這個指令！", ephemeral=True)
        return
    await interaction.response.defer()

    # 獲取當前年份
    current_year = datetime.today().year
    if date is None:
        date = datetime.today().strftime("%Y-%m-%d")
    else:
        # 如果使用者只填 `MMDD`，則補上當前年份
        if len(date) == 4:
            date = f"{current_year}-{date[0:2]}-{date[2:4]}"
        else:
            date = f"{date[0:4]}-{date[4:6]}-{date[6:8]}"
    try:
        test_date = int(date[0:4])
        test_date = int(date[5:7])
        test_date = int(date[8:9])
        data = {
            'date': date,
            'item': item,
            'ie': "ie",
            'letter_i': letter_i,
            'number_i': number_i,
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(WEB_APP_URL_IE, json=data, headers=headers)
        print("Response Status Code:", response.status_code)
        print("Response Text:", response.text)
        if response.status_code == 200:
            await interaction.followup.send("✅ 收入成功寫入帳本！")
        else:
            await interaction.followup.send("❌ 收入寫入帳本失敗。")
    except:
        await interaction.followup.send("❌ 請輸入正確的日期格式！")

@bot.tree.command(name = "expense", description = "記帳：支出")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(date="記錄日期（格式：YYYYMMDD 或 MMDD，不填則為今天）", item = "描述這筆支出項目（Ex：Lunch）", letter_e = "這筆支出項目的種類（以字母簡寫）", number_e = "金額")
async def expense(interaction: discord.Interaction, date: Optional[str], item: str, letter_e: str, number_e: int):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("⛔ 你沒有權限使用這個指令！", ephemeral=True)
        return
    await interaction.response.defer()

    # 獲取當前年份
    current_year = datetime.today().year
    if date is None:
        date = datetime.today().strftime("%Y-%m-%d")
    else:
        # 如果使用者只填 `MMDD`，則補上當前年份
        if len(date) == 4:
            date = f"{current_year}-{date[0:2]}-{date[2:4]}"
        else:
            date = f"{date[0:4]}-{date[4:6]}-{date[6:8]}"
    try:
        test_date = int(date[0:4])
        test_date = int(date[5:7])
        test_date = int(date[8:9])
        data = {
            'date': date,
            'item': item,
            'ie': "ie",
            'letter_e': letter_e,
            'number_e': number_e
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(WEB_APP_URL_IE, json=data, headers=headers)
        print("Response Status Code:", response.status_code)
        print("Response Text:", response.text)
        if response.status_code == 200:
            await interaction.followup.send("✅ 支出成功寫入帳本！")
        else:
            await interaction.followup.send("❌ 支出寫入帳本失敗。")
    except:
        await interaction.followup.send("❌ 請輸入正確的日期格式！")

@bot.tree.command(name = "income_expense", description = "記帳：收支")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(date="記錄日期（格式：YYYYMMDD 或 MMDD，不填則為今天）", item = "描述這筆收支項目（Ex：Lunch）", letter_i = "收入種類（以字母簡寫）", number_i = "收入金額", letter_e = "支出種類（以字母簡寫）", number_e = "支出金額")
async def income_expense(interaction: discord.Interaction, date: Optional[str], item: str, letter_i: str, number_i: int, letter_e: str, number_e: int):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("⛔ 你沒有權限使用這個指令！", ephemeral=True)
        return
    await interaction.response.defer()
    
    # 獲取當前年份
    current_year = datetime.today().year
    if date is None:
        date = datetime.today().strftime("%Y-%m-%d")
    else:
        # 如果使用者只填 `MMDD`，則補上當前年份
        if len(date) == 4:
            date = f"{current_year}-{date[0:2]}-{date[2:4]}"
        else:
            date = f"{date[0:4]}-{date[4:6]}-{date[6:8]}"
    try:
        test_date = int(date[0:4])
        test_date = int(date[5:7])
        test_date = int(date[8:9])
        data = {
            'date': date,
            'item': item,
            'ie': "ie",
            'letter_i': letter_i,
            'number_i': number_i,
            'letter_e': letter_e,
            'number_e': number_e
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(WEB_APP_URL_IE, json=data, headers=headers)
        print("Response Status Code:", response.status_code)
        print("Response Text:", response.text)
        if response.status_code == 200:
            await interaction.followup.send("✅ 收支成功寫入帳本！")
        else:
            await interaction.followup.send("❌ 收支寫入帳本失敗。")
    except:
        await interaction.followup.send("❌ 請輸入正確的日期格式！")

@bot.tree.command(name = "account_timestamp_w", description = "記錄帳本核對時間戳記")
@app_commands.default_permissions(administrator=True)
@app_commands.describe()
async def account_timestamp_w(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("⛔ 你沒有權限使用這個指令！", ephemeral=True)
        return
    await interaction.response.defer()
    mode = {'mode': 'TS_write'}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(WEB_APP_URL_RTS, json=mode, headers=headers)
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)
    if response.status_code == 200:
        await interaction.followup.send("✅ 時間戳記更新成功！")
    else:
        await interaction.followup.send("❌ 時間戳記更新失敗。")

@bot.tree.command(name = "ms_arc", description = "計算缺的ARC數量以及農到滿所需天數")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(lv = "ARC等級", num = "ARC數量", week = "是否解每週任務")
async def ms_arc(interaction: discord.Interaction, lv: int, num: int, week: bool):
    sum = 0
    result = 0
    if lv > 19 or lv < 1:
        await interaction.response.send_message("Invalid input.")
    else:
        while lv < 20:
            sum += lv * lv + 11
            lv += 1
        sum -= num
        leak = sum
        if leak < 0:
            await interaction.response.send_message("Invalid input.")
        else:
            if week == True:
                result = int(sum / 185) * 7
                sum -= result * 185 / 7 + 45
                if sum <= 0 and sum > -45:
                    result += 1
                elif sum > 0 and sum % 20 == 0:
                    reslut += sum / 20
                elif sum > 0 and sum % 20 != 0:
                    result += int(sum / 20) + 1
                else:
                    result += 0
            else:
                if sum % 20 == 0:
                    result += sum / 20
                else:
                    result += int(sum / 20) + 1
            result = int(result)
            await interaction.response.send_message(f"缺的數量：{leak}，農滿所需天數：{result}")

@bot.tree.command(name = "ms_aut", description = "計算缺的AUT數量以及農到滿所需天數")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(lv = "AUT等級", num = "AUT數量", cernium = "計算的區域是否為賽爾尼溫")
async def ms_aut(interaction: discord.Interaction, lv: int, num: int, cernium: bool):
    sum = 0
    result = 0
    if lv > 10 or lv < 1:
        await interaction.response.send_message("Invalid input.")
    else:
        while lv < 11:
            sum += 9 * lv * lv + 20 * lv
            lv += 1
        sum -= num
        leak = sum
        if leak < 0:
            await interaction.response.send_message("Invalid input.")
        else:
            if cernium == True:
                if sum % 20 == 0:
                    result += sum / 20
                else:
                    result += int(sum / 20) + 1
            else:
                if sum % 10 == 0:
                    result += sum / 10
                else:
                    result += int(sum / 10) + 1
            result = int(result)
            await interaction.response.send_message(f"缺的數量：{leak}，農滿所需天數：{result}")

@bot.tree.command(name = "gta_clubtimer", description = "計算需要去領GTAO夜總會的被動收入的時間")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(last_time = "上次結算時間(格式為hhmm)", times = "已結算次數")
async def gta_clubtimer(interaction: discord.Interaction, last_time: int, times: int):
    if last_time > 2359 or last_time < 1:
        await interaction.response.send_message("Invalid input.")
    if times > 2 or times < 0:
        await interaction.response.send_message("Invalid input.")
    hour = int(last_time / 100)
    minute = int(last_time % 100)
    if minute > 59:
        await interaction.response.send_message("Invalid input.")

    minute += (2 - times) * 48
    nxt1 = timeswifter(hour, minute)
    minute += 48
    nxt2 = timeswifter(hour, minute)
    for i in range(0, 2):
        nxt1[i] = numadjuster(nxt1[i])
        nxt2[i] = numadjuster(nxt2[i])
    await interaction.response.send_message(f"下次領取時間為 {nxt1[0]}:{nxt1[1]} 到 {nxt2[0]}:{nxt2[1]} 之間")

@bot.tree.command(name = "pcr_ot_calc", description = "計算補償刀秒數")
@app_commands.describe(boss_hp = "BOSS剩餘血量", d1 = "隊員1傷害", d2 = "隊員2傷害")
async def pcr_ot_cal(interaction: discord.Interaction, boss_hp: int, d1: int, d2: int):
    await interaction.response.defer()
    def ot_cal(hp, d_first, d_second):
        if hp - d_first - d_second > 0:
            return -1
        current_hp = hp - d_first
        ot_sec = min(90, round(110 - math.floor(float(current_hp) * 90 / float(d_second))))
        return ot_sec
    def ne_dh(hp, d_first, d_second):
        if d_second > d_first:
            tmp = d_second
            d_second = d_first
            d_first = tmp
        ne_d = round(max(0, hp - 21.0 * d_second / 90.0 - d_first))
        return ne_d
    d1d2 = ot_cal(boss_hp, d1, d2)
    d2d1 = ot_cal(boss_hp, d2, d1)
    ned = ne_dh(boss_hp, d2, d1)
    if d1d2 == -1:
        await interaction.followup.send(f"Boss血量：{boss_hp}\n隊員1傷害：{d1}\n隊員2傷害：{d2}\n\n白癡阿這根本收不掉阿==")
    else:
        await interaction.followup.send(f"Boss血量：{boss_hp}\n隊員1傷害：{d1}\n隊員2傷害：{d2}\n\n**隊員1先出**，隊員2可以拿到的補償刀秒數：{d1d2}\n**隊員2先出**，隊員1可以拿到的補償刀秒數：{d2d1}\n想要滿補，還需要再對Boss造成 {ned} 傷害。")

@bot.tree.command(name = "pcr_ot_shift", description = "轉換補償刀軸")
@app_commands.describe(seconds = "補償刀秒數")
async def pcr_ot_shift(interaction: discord.Interaction, seconds: int):
    """ 使用者輸入 /pcr_ot_shift {秒數}，Bot 會等待 30 秒內的訊息並處理 """

    def ot_shift(text, remain_seconds):
        seconds_to_subtract = 90 - remain_seconds
        pattern = r'\b(?:\d{1,2}:\d{2}|\d{3})\b'  # 支援 "1:21" 或 "121" 格式
        adjusted_lines = []  # 存放處理後的行
        should_stop = False  # 當某行被刪除後，所有後續行都不處理

        for line in text.split("\n"):
            if should_stop:
                break  # 停止處理，後續行全部忽略

            match = re.search(pattern, line)
            if not match:
                adjusted_lines.append(line)  # 無時間的行仍然保留
                continue  

            time_str = match.group()

            # 解析時間
            if ":" in time_str:  # 例：1:21
                minutes, seconds = map(int, time_str.split(":"))
                total_seconds = minutes * 60 + seconds
            else:  # 例：120（解析為 1:20）
                minutes = int(time_str[:-2])  # 取前面數字作為分鐘
                seconds = int(time_str[-2:])  # 取後兩位作為秒數
                total_seconds = minutes * 60 + seconds

            # 減去指定秒數
            new_seconds = total_seconds - seconds_to_subtract
            if new_seconds < 1:
                should_stop = True  # 從這一行開始，所有後續行都刪除
                continue  # 這一行也被刪除

            # 格式化新時間
            if new_seconds >= 60:
                new_time = f"{new_seconds // 60}:{new_seconds % 60:02d}"
            else:
                new_time = f"0:{new_seconds:02d}"  # 確保秒數小於 60 時仍有 `0:xx` 格式

            # 替換該行內的時間
            adjusted_line = re.sub(pattern, new_time, line, count=1)
            adjusted_lines.append(adjusted_line)

        return "\n".join(adjusted_lines).strip()

    if not (1 <= seconds <= 90):
        await interaction.response.send_message("請輸入 1~90 之間的秒數！", ephemeral=True)
        return

    await interaction.response.defer()  # 先延遲回應，防止 Discord 3 秒超時
    await interaction.followup.send(f"請在 30 秒內發送想要轉換的軸。（補償刀秒數：{seconds}）")

    def check(msg):
        return msg.author.id == interaction.user.id and msg.channel == interaction.channel

    try:
        user_msg = await bot.wait_for("message", timeout=30.0, check=check)
        adjusted_text = ot_shift(user_msg.content, seconds)
        await interaction.followup.send(f"```{adjusted_text}```")
    except asyncio.TimeoutError:
        await interaction.followup.send("⚠️ 你沒有在 30 秒內回應，取消指令。")

channels = {"公告": "743858605026967622",
            "練角抽角公告": "826496127972671538",
            "測試用": "870962270887374888"}

@bot.tree.command(name="schedule", description="排程傳送訊息到固定頻道")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(
    channel="選擇要傳送訊息的頻道",
    year="年份", month="月份", day="日期",
    hour="小時", minute="分鐘",
    message="要傳送的訊息內容"
)
@app_commands.choices(
    channel=[
        app_commands.Choice(name=name, value=cid)
        for name, cid in channels.items()
    ]
)
async def schedule(
    interaction: discord.Interaction,
    channel: app_commands.Choice[str],
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    message: str
):
    target_channel_id = int(channel.value)
    target_channel = interaction.guild.get_channel(target_channel_id)
    target_time = datetime(year, month, day, hour, minute)
    trigger = DateTrigger(run_date=target_time)

    async def send_message():
        await target_channel.send(message)

    scheduler.add_job(send_message, trigger=trigger)
    await interaction.response.send_message(
        f"✅ 已排程訊息：{target_time.strftime('%Y-%m-%d %H:%M')} 發送至 {target_channel.mention}",
        ephemeral=True
    )

# BOT 開機
bot.run(token)