import disnake
from disnake.ext import commands
from disnake import ButtonStyle, Button
import time
from botToken import token, testToken, version
import json
import sqlite3 as sql3
import random
import datetime
import asyncio

intents = disnake.Intents.default()
intents.presences = True
intents.messages = True
intents.reactions = True
intents.voice_states = True

bot = commands.Bot(command_prefix=None, intents=intents)
db = sql3.connect('base.db')
sql = db.cursor()

admin_role = [1160934624789278901, 1160935163597955152, 1160935693737001011, 1160936818087309312, 1183485796741828739]

sql.execute("""CREATE TABLE IF NOT EXISTS user_counts (
    user_id INTEGER PRIMARY KEY, 
    count INTEGER
)
""")

sql.execute("""CREATE TABLE IF NOT EXISTS time_data (
    user_id INTEGER PRIMARY KEY, 
    voice_time INTEGER,
    gift_time INTEGER
)
""")

db.commit()

@bot.slash_command(name='store', description='Магазин сервера')
async def store(ctx):
    embed = disnake.Embed(
        title="Магазин",
        description="**Кастом Роли**\n \nКастом роль (текст) — **20р** или **2500 монет**\nКастом роль (текст + цвет) — **35р** или **4000 монет**\nКастом роль (с матом или 18+ названием) — **100р**\n \n**Крутки**\n \nОбычная крутка — **500 монет**\n \nРедкая крутка — **850 монет**\n \nЭпическая крутка — **1400 монет**\n \nВыберите товар:",
        color=0x6115b3  
    )

    button_row = disnake.ui.ActionRow(
        disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="Обычная крутка", custom_id="buy_loto"),
        disnake.ui.Button(style=disnake.ButtonStyle.green, label="Редкая крутка", custom_id="buy_loto_rare"),
        disnake.ui.Button(style=disnake.ButtonStyle.primary, label="Эпическая крутка", custom_id="buy_loto_epic")
    )

    button_row2 = disnake.ui.ActionRow(
        disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="Кастом роль", custom_id="buy_role")
    )

    await ctx.send(embed=embed, components=[button_row, button_row2])

@bot.slash_command(name='link', description='Ссылки на официальные источники')
async def link(ctx):
    embed = disnake.Embed(
        title="Ссылки",
        description="[Telegram](https://t.me/kenyka)\n \n[Youtube](https://www.youtube.com/channel/UCM6InRH22Xno8nywrZnbhLA)\n \n[GitHub](https://github.com/keeniGitHub)\n \n[DonateAlerts](https://www.donationalerts.com/r/itzkeeni)",
        color=0x6115b3  
    )
    await ctx.send(embed=embed)

@bot.slash_command(name='help', description='Список команд')
async def link(ctx):
    embed = disnake.Embed(
        title="Команды",
        description=f"/help - вы сейчас его читает\n \n/store - магазин сервера\n \n/link - ссылки на официальные источники\n \n/hug - обнять\n \n/kiss - поцеловать\n \n/trax - тра...\n \n/profile - ваш профиль на сервере\n \n*bot version {version}\nby ItzKeeni*",
        color=0x6115b3  
    )
    await ctx.send(embed=embed)

@bot.slash_command(name="hug", description="Обнять пользователя)")
async def hug(ctx, member: disnake.Member):
    await ctx.send(f'{ctx.author.mention} обнял {member.mention} <3')

@bot.slash_command(name="kiss", description="Поцеловать")
async def hug(ctx, member: disnake.Member):
    await ctx.send(f'{ctx.author.mention} Поцеловал {member.mention} ❤')

@bot.slash_command(name="gift", description="Активировать подарок")
async def gift(ctx):    
    await ctx.send("В данный момент активных подарков нету.")

@bot.slash_command(name="gift-status", description="статус активаций команды /gift")
async def status(ctx): 
    with open('var.json', 'r') as file:
        data = json.load(file) 

    member = ctx.author
    role_id = 1160934624789278901
    if role_id in [role.id for role in ctx.author.roles]:
        status = data['activate']
        await ctx.send(f'Осталось активаций: {status}')
    else:
         await ctx.send('У вас нету доступа!')    

@bot.slash_command(name="clear", description="очистить чат")
async def clear(ctx, amount: int):

    if ctx.author.top_role.id in admin_role:
        await ctx.channel.purge(limit=amount)
        await ctx.send("Сообщения успешно удалены!", delete_after=5)
    else:
        await ctx.send("Недостаточно прав!")

@bot.slash_command(name="add_money", description="добавить пользователю монеты")
async def clear(ctx, member: disnake.Member, amount: int):

    if ctx.author.top_role.id in admin_role:
        sql.execute("SELECT count FROM user_counts WHERE user_id=?", (member.id,))
        count = sql.fetchone()[0]

        sql.execute("UPDATE user_counts SET count = ? WHERE user_id = ?", (amount + int(count), member.id))
        db.commit()
        await ctx.send(f"{member} было добавлено {amount} монет!")  
    else:
        await ctx.send("Недостаточно прав!")    

@bot.slash_command(name="del_money", description="убрать пользователю монеты")
async def clear(ctx, member: disnake.Member, amount: int):

    if ctx.author.top_role.id in admin_role:
        sql.execute("SELECT count FROM user_counts WHERE user_id=?", (member.id,))
        count = sql.fetchone()[0]

        sql.execute("UPDATE user_counts SET count = ? WHERE user_id = ?", (int(count) - amount, member.id))
        db.commit()
        await ctx.send(f"{member} было убрано {amount} монет!")  
    else:
        await ctx.send("Недостаточно прав!") 

@bot.slash_command(name="beta_testing_programm", description="Программма бета-тестирования")
async def beta(ctx):
    embed = disnake.Embed(
            title=f"**Программа бета тестирования**",
            description=f"В программе бета тестирования, вы сможете тестировать ранние фишки данного бота на специальном сервере.\n \nТак же, вы будуите получать различные бонусы за это, ввиде монет, значка и прочего.\n \n*Заявки расматриваются в течении 32 часов*",
            color=0x6115b3  
        )
    
    button = disnake.ui.Button(style=disnake.ButtonStyle.gray, label="Подать заявку",  url="")

    view = disnake.ui.View()
    view.add_item(button)

    await ctx.send(embed=embed, view=view)

@bot.listen('on_message')
async def on_message(message):
    user_id = message.author.id
    sql.execute('SELECT count FROM user_counts WHERE user_id=?', (user_id,))
    result = sql.fetchone()

    if message.channel.id == 1183436836215992320 or message.channel.id == 1188844282078048318:
        if result:
            if datetime.datetime.today().isoweekday() in [6, 7]:
                count = result[0] + 5
                sql.execute('UPDATE user_counts SET count=? WHERE user_id=?', (count, user_id))
                db.commit() 
            else:
                count = result[0] + 3
                sql.execute('UPDATE user_counts SET count=? WHERE user_id=?', (count, user_id))
                db.commit()           
        else:
            sql.execute('INSERT INTO user_counts (user_id, count) VALUES (?, 1)', (user_id,))
            db.commit()
    else:
        pass
        
@bot.slash_command(name="profile", description="Ваш профиль на сервере")
async def count(ctx):
    db = sql3.connect('base.db')
    sql = db.cursor()
    user_id = ctx.author.id
    sql.execute('SELECT count FROM user_counts WHERE user_id=?', (user_id,))
    result = sql.fetchone()

    if result:
        count = result[0]
        join_date = ctx.author.joined_at.strftime("%Y-%m-%d")
        badge = " "

        boost = disnake.utils.get(ctx.guild.roles, id=1183858475856580748)
        moderator = disnake.utils.get(ctx.guild.roles, id=1184895535296020631)
        dev = disnake.utils.get(ctx.guild.roles, id=1184879952596828313)
        bughunter = disnake.utils.get(ctx.guild.roles, id=1184871684260503614)
        bughuntergold = disnake.utils.get(ctx.guild.roles, id=1184871797313773680)
        verifed = disnake.utils.get(ctx.guild.roles, id=1184870810511478786)
        itz = disnake.utils.get(ctx.guild.roles, id=1183376165390520350)
        donate = disnake.utils.get(ctx.guild.roles, id=1183675615161884692)
        stars = disnake.utils.get(ctx.guild.roles, id=1188045777386340372)
        betaTester = disnake.utils.get(ctx.guild.roles, id=1188841327840989214)

        if verifed in ctx.author.roles:
            badge += "<:VerifedAccount:1184831405180600502>⠀"
        if boost in ctx.author.roles:
            badge += "<:Boost:1184863793872908338>⠀"
        if moderator in ctx.author.roles:
            badge += "<:Moderation:1184934077892153474>⠀"
        if dev in ctx.author.roles:
            badge += "<:Developer:1184934142249541732>⠀"
        if bughunter in ctx.author.roles:
            badge += "<:Bughunter:1184863662436012084>⠀"
        if bughuntergold in ctx.author.roles:
            badge += "<:BugHunterGold:1184863673618006086>⠀"
        if itz in ctx.author.roles:
            badge += "<:ItzTeamStaff:1184831415318237216>⠀"
        if donate in ctx.author.roles:
            badge += "<:Donate:1184863903147106345>⠀"
        if stars in ctx.author.roles:
            badge += "<:Stars:1187849324235849758>⠀" 
        if betaTester in ctx.author.roles:
            badge += "<:BetaTesters:1188117413586276422>⠀" 

        embed = disnake.Embed(
            title=f"Профиль {ctx.author.display_name}",
            description=f"Ник — **{ctx.author.display_name}**\n \nid — **{ctx.author.id}**\n \nБаланс — **{count}** монет\n \nПрисоеденились к серверу: **{join_date}**\n \nЗначки: {badge}",
            color=0x6115b3  
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send('Произошла ошибка!')

@bot.slash_command(name="user_profile", description="Профиль пользователя на сервере")
async def count(ctx, user: disnake.Member):
    db = sql3.connect('base.db')
    sql = db.cursor()
    user_id = user.id
    sql.execute('SELECT count FROM user_counts WHERE user_id=?', (user_id,))
    result = sql.fetchone()

    if result:
        count = result[0]
        join_date = user.joined_at.strftime("%Y-%m-%d")
        badge = " "

        boost = disnake.utils.get(user.guild.roles, id=1183858475856580748)
        moderator = disnake.utils.get(user.guild.roles, id=1184895535296020631)
        dev = disnake.utils.get(user.guild.roles, id=1184879952596828313)
        bughunter = disnake.utils.get(user.guild.roles, id=1184871684260503614)
        bughuntergold = disnake.utils.get(user.guild.roles, id=1184871797313773680)
        verifed = disnake.utils.get(user.guild.roles, id=1184870810511478786)
        itz = disnake.utils.get(user.guild.roles, id=1183376165390520350)
        donate = disnake.utils.get(user.guild.roles, id=1183675615161884692)
        stars = disnake.utils.get(user.guild.roles, id=1188045777386340372)
        betaTester = disnake.utils.get(user.guild.roles, id=1188841327840989214)

        if verifed in user.roles:
            badge += "<:VerifedAccount:1184831405180600502>⠀"
        if boost in user.roles:
            badge += "<:Boost:1184863793872908338>⠀"
        if moderator in user.roles:
            badge += "<:Moderation:1184934077892153474>⠀"
        if dev in user.roles:
            badge += "<:Developer:1184934142249541732>⠀"
        if bughunter in user.roles:
            badge += "<:Bughunter:1184863662436012084>⠀"
        if bughuntergold in user.roles:
            badge += "<:BugHunterGold:1184863673618006086>⠀"
        if itz in user.roles:
            badge += "<:ItzTeamStaff:1184831415318237216>⠀"
        if donate in user.roles:
            badge += "<:Donate:1184863903147106345>⠀"
        if stars in user.roles:
            badge += "<:Stars:1187849324235849758>⠀" 
        if betaTester in user.roles:
            badge += "<:BetaTesters:1188117413586276422>⠀" 

        embed = disnake.Embed(
            title=f"Профиль {user.display_name}",
            description=f"Ник — **{user.display_name}**\n \nid — **{user.id}**\n \nБаланс — **{count}** монет\n \nПрисоеденились к серверу: **{join_date}**\n \nЗначки: {badge}",
            color=0x6115b3  
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send('Произошла ошибка!')

@bot.event # loto
async def on_button_click(interaction: disnake.MessageInteraction):
    if interaction.component.custom_id == "buy_loto":

        button = disnake.ui.Button(style=disnake.ButtonStyle.grey, label="Купить крутку", custom_id="buy_loto_confirm")

        view = disnake.ui.View()
        view.add_item(button)

        embed = disnake.Embed(
        title="Обычная крутка",
        description=f"Одна крута — **500** монет\n \n**Шансы:**\nКастом роль (текст + цвет) - **4%**\n \n2000 монет - **4%**\n \nКастом роль(текст) - **8%**\n \n1000 монет - **8%**\n \n500монет - **16%**\n \n100 монет - **24%**\n \nНичего - **36%**",
        color=0x6115b3  
    )
        await interaction.send(embed=embed, view=view)

    if interaction.component.custom_id == "buy_loto_rare":

        button = disnake.ui.Button(style=disnake.ButtonStyle.green, label="Купить крутку", custom_id="buy_loto_rare_confirm")

        view = disnake.ui.View()
        view.add_item(button)

        embed = disnake.Embed(
        title="Редкая крутка",
        description=f"Одна крутка — **850** монет\n \n**Шансы:**\nКастом роль (текст + цвет) - **6,25%**\n \nКастом роль (текст) - **9,38%**\n \n3000 монет - **6,25%**\n \n2000 монет - **9,38%**\n \n1500 монет - **12,50%**\n \n1000 монет - **15,63%**\n \n500 монет - **18,75%**\n \nНичего - **25%**",
        color=0x6115b3  
    )
        await interaction.send(embed=embed, view=view)

    if interaction.component.custom_id == "buy_loto_epic":

        button = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Купить крутку", custom_id="buy_loto_epic_confirm")

        view = disnake.ui.View()
        view.add_item(button)

        embed = disnake.Embed(
        title="Эпическая крутка",
        description=f"Одна крутка — **1400** монет\n \n**Шансы:**\nКастом роль (текст + цвет) - **8%**\n \nЗначок <:Stars:1187849324235849758> - **12%**\n \n5000 монет - **6%**\n \n3000 монет - **10%**\n \n2000 монет - **12%**\n \n1500 монет - **14%**\n \n1000 монет - **16%**\n \nНичего - **20%**",
        color=0x6115b3  
    )
        await interaction.send(embed=embed, view=view)

    if interaction.component.custom_id == "buy_loto_confirm":
        db = sql3.connect('base.db')
        sql = db.cursor()
        user_id = interaction.author.id
        sql.execute('SELECT count FROM user_counts WHERE user_id=?', (user_id,))
        result = sql.fetchone()[0]

        if result >= 500:
            sql.execute('SELECT count FROM user_counts WHERE user_id=?', (user_id,))
            result = sql.fetchone()[0]
            sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result - 500, user_id,))
            db.commit()
             
            rand_item = random.randint(1, 25)
            
            if rand_item == 7:
                await interaction.send(f"{interaction.author.name} Вам выпало **Кастом роль (текст + цвет)**!\nЧтобы получить приз создайте тикет в канале <#1183391555860578407>")

            if rand_item == 2 or rand_item == 10:
                await interaction.send(f"{interaction.author.name} Вам выпало **Кастом роль (текст)**!\nЧтобы получить приз создайте тикет в канале <#1183391555860578407>")
            
            if rand_item == 20:
                await interaction.send(f"{interaction.author.name} Вам выпало **2000 монет на баланс**!");
                sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result+1500,user_id,)); 
                db.commit()

            if rand_item == 1 or rand_item == 5:
                await interaction.send(f"{interaction.author.name} Вам выпало **1000 монет на баланс**!");
                sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result+500,user_id,)); 
                db.commit()

            if rand_item == 3 or rand_item == 8 or rand_item == 15 or rand_item == 17:
                await interaction.send(f"{interaction.author.name} Вам выпало **500 монет на баланс**!");
                sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result-0,user_id,)); 
                db.commit()
            
            if rand_item == 21 or rand_item == 22 or rand_item == 23 or rand_item == 24 or rand_item == 25 or rand_item == 14:
                await interaction.send(f"{interaction.author.name} Вам выпало **100 монет на баланс**!");
                sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result-400,user_id,)); 
                db.commit()

            if rand_item == 4 or rand_item == 6 or rand_item == 9 or rand_item == 11 or rand_item == 12 or rand_item == 13 or rand_item == 16 or rand_item == 18 or rand_item == 19:
                await interaction.send(f"{interaction.author.name} К сожелению, вам ничего не выпало(")
        else:
            await interaction.send("Недостаточно монет!")

    if interaction.component.custom_id == "buy_loto_rare_confirm":
        db = sql3.connect('base.db')
        sql = db.cursor()
        user_id = interaction.author.id
        sql.execute('SELECT count FROM user_counts WHERE user_id=?', (user_id,))
        result = sql.fetchone()[0]

        if result >= 850:
            sql.execute('SELECT count FROM user_counts WHERE user_id=?', (user_id,))
            result = sql.fetchone()[0]
            sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result - 850, user_id,))
            db.commit()
             
            rand_item = random.randint(1, 32)
            
            if rand_item == 1 or rand_item == 26:
                await interaction.send(f"{interaction.author.name} Вам выпало **Кастом роль (текст + цвет)**!\nЧтобы получить приз создайте тикет в канале <#1183391555860578407>")

            if rand_item == 2 or rand_item == 3 or rand_item == 27:
                await interaction.send(f"{interaction.author.name} Вам выпало **Кастом роль (текст)**!\nЧтобы получить приз создайте тикет в канале <#1183391555860578407>")
            
            if rand_item == 4 or rand_item == 28:
                await interaction.send(f"{interaction.author.name} Вам выпало **3000 монет на баланс**!");
                sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result+2150,user_id,)); 
                db.commit()

            if rand_item == 5 or rand_item == 6 or rand_item == 29:
                await interaction.send(f"{interaction.author.name} Вам выпало **2000 монет на баланс**!");
                sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result+1150,user_id,)); 
                db.commit()

            if rand_item == 7 or rand_item == 8 or rand_item == 9 or rand_item == 24:
                await interaction.send(f"{interaction.author.name} Вам выпало **1500 монет на баланс**!");
                sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result+650,user_id,)); 
                db.commit()
            
            if rand_item == 10 or rand_item == 11 or rand_item == 12 or rand_item == 13 or rand_item == 25:
                await interaction.send(f"{interaction.author.name} Вам выпало **1000 монет на баланс**!");
                sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result+150,user_id,)); 
                db.commit()

            if rand_item == 14 or rand_item == 15 or rand_item == 16 or rand_item == 17 or rand_item == 18 or rand_item == 30:
                await interaction.send(f"{interaction.author.name} Вам выпало **500 монет на баланс**!");
                sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result-350,user_id,)); 
                db.commit()
            if rand_item == 19 or rand_item == 20 or rand_item == 21 or rand_item == 22 or rand_item == 23 or rand_item == 31 or rand_item == 32:
                await interaction.send(f"{interaction.author.name} К сожелению, вам ничего не выпало(")  
        else:
            await interaction.send("Недостаточно монет!")

    if interaction.component.custom_id == "buy_loto_epic_confirm":
        db = sql3.connect('base.db')
        sql = db.cursor()
        user_id = interaction.author.id
        sql.execute('SELECT count FROM user_counts WHERE user_id=?', (user_id,))
        result = sql.fetchone()[0]

        if result >= 1400:
            sql.execute('SELECT count FROM user_counts WHERE user_id=?', (user_id,))
            result = sql.fetchone()[0]
            sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result - 1400, user_id,))
            db.commit()
             
            rand_item = random.randint(1, 50)
            
            if rand_item == 1 or rand_item == 2 or rand_item == 3 or rand_item == 4:
                await interaction.send(f"{interaction.author.name} Вам выпало **Кастом роль (текст + цвет)**!\nЧтобы получить приз создайте тикет в канале <#1183391555860578407>")
            if rand_item == 10 or rand_item == 11 or rand_item == 12:
                await interaction.send(f"{interaction.author.name} Вам выпало **5000 монет на баланс**!");
                sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result+3600,user_id,)); 
                db.commit()

            if rand_item == 13 or rand_item == 14 or rand_item == 15 or rand_item == 16 or rand_item == 7:
                await interaction.send(f"{interaction.author.name} Вам выпало **3000 монет на баланс**!");
                sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result+1600,user_id,)); 
                db.commit()

            if rand_item == 17 or rand_item == 18 or rand_item == 19 or rand_item == 20 or rand_item == 21 or rand_item == 22:
                await interaction.send(f"{interaction.author.name} Вам выпало **2000 монет на баланс**!");
                sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result+600,user_id,)); 
                db.commit()
            
            if rand_item == 23 or rand_item == 24 or rand_item == 25 or rand_item == 26 or rand_item == 27 or rand_item == 28 or rand_item == 29:
                await interaction.send(f"{interaction.author.name} Вам выпало **1500 монет на баланс**!");
                sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result+100,user_id,)); 
                db.commit()

            if rand_item == 30 or rand_item == 31 or rand_item == 32 or rand_item == 33 or rand_item == 34 or rand_item == 35 or rand_item == 36 or rand_item == 37:
                await interaction.send(f"{interaction.author.name} Вам выпало **1000 монет на баланс**!");
                sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result-400,user_id,)); 
                db.commit()

            if rand_item == 38 or rand_item == 39 or rand_item == 40 or rand_item == 41 or rand_item == 42 or rand_item == 43 or rand_item == 44 or rand_item == 45 or rand_item == 46 or rand_item == 47:
                await interaction.send(f"{interaction.author.name} К сожелению, вам ничего не выпало(")  

            if rand_item == 48 or rand_item == 49 or rand_item == 50 or rand_item == 5 or rand_item == 6 or rand_item == 7:
                await interaction.send(f"{interaction.author.name} Вам выпал эксклюзивный значок <:Stars:1187849324235849758> !") 
                role_id = 1188045777386340372
                role = disnake.utils.get(interaction.guild.roles, id=role_id)
                if role and isinstance(interaction.author, disnake.Member):
                    member = interaction.author
                    await member.add_roles(role)
                else:
                    await interaction.send("Ошибка! role_not_adds")

        else:
            await interaction.send("Недостаточно монет!")

    if interaction.component.custom_id == "buy_role":

        embed = disnake.Embed(
            title = "Кастом роль",
            description="Выберите товар:\n \n*Нельзя делать роли по типу: админ, модератор, кеняка*\n*Если вы хотите купить роль за деньги, создайте тикет в <#1183391555860578407>*",
            color=0x6115b3 
        )

        button_row = disnake.ui.ActionRow(
        disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="Кастом роль (текст)", custom_id="buy_role_1"),
        )

        button_row2 = disnake.ui.ActionRow(
            disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="Кастом роль (текст + цвет)", custom_id="buy_role_2")
        )

        await interaction.send(embed=embed, components=[button_row, button_row2])

    if interaction.component.custom_id == "buy_role_1":
        db = sql3.connect('base.db')
        sql = db.cursor()
        user_id = interaction.author.id
        sql.execute('SELECT count FROM user_counts WHERE user_id=?', (user_id,))
        result = sql.fetchone()[0]

        if result >= 2500:
            sql.execute('SELECT count FROM user_counts WHERE user_id=?', (user_id,))
            result = sql.fetchone()[0]
            sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result - 2500, user_id,))
            db.commit()

            await interaction.send(f"{interaction.author.name} успешно преобрели **Кастом роль (текст)**!\n \nДля получения создайте тикет в канале <#1183391555860578407>")

        else:
            await interaction.send("Недостаточно монет!")

    if interaction.component.custom_id == "buy_role_2":
        db = sql3.connect('base.db')
        sql = db.cursor()
        user_id = interaction.author.id
        sql.execute('SELECT count FROM user_counts WHERE user_id=?', (user_id,))
        result = sql.fetchone()[0]

        if result >= 4000:
            sql.execute('SELECT count FROM user_counts WHERE user_id=?', (user_id,))
            result = sql.fetchone()[0]
            sql.execute(f"UPDATE user_counts SET count = ? WHERE user_id = ?", (result - 4000, user_id,))
            db.commit()

            await interaction.send(f"{interaction.author.name} успешно преобрели **Кастом роль (текст + цвет)**!\n \nДля получения создайте тикет в канале <#1183391555860578407>")
        else:
            await interaction.send("Недостаточно монет!")

@bot.slash_command()
async def check_voice_time(ctx):
    pass

async def add_count_to_user():
    while True:
        await asyncio.sleep(60)  # Wait for 1 minute
        for guild in bot.guilds:
            for member in guild.members:
                if member.voice and member.voice.channel and member.voice.channel.id == 1183486412008456293:
                    continue
                else:
                    sql.execute('SELECT count FROM user_counts WHERE user_id = ?', (member.id,))
                    result = sql.fetchone()
                    if result:
                        if datetime.datetime.today().isoweekday() in [6, 7]:
                            sql.execute('UPDATE user_counts SET count = ? WHERE user_id = ?', (result[0]+5, member.id))
                            db.commit()
                        else:
                            sql.execute('UPDATE user_counts SET count = ? WHERE user_id = ?', (result[0]+3, member.id))
                            db.commit()    
                    else:
                        sql.execute('INSERT INTO user_counts (user_id, count) VALUES (?, ?)', (member.id, 0))
                        db.commit()
        db.commit()

@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name="Яндекс Карты"))
    print(f'Bot is ready, version: {version}')

# @bot.event
# async def on_member_update(before, after):
#     role_id = 1189560625848930334 #1183365301253984328

#     if role_id in [role.id for role in after.roles] and role_id not in [role.id for role in before.roles] and not after.bot:
#         db = sql3.connect('base.db')
#         sql = db.cursor()

#         sql.execute('SELECT count FROM user_counts WHERE user_id = ?', (after.id,))
#         result = sql.fetchone()

#         sql.execute('UPDATE user_counts SET count = ? WHERE user_id = ?', (result[0]+50, after.id))
#         db.commit()

bot.loop.create_task(add_count_to_user())
bot.run(token) 