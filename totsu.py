import discord
from discord.ext import commands

TOKEN = 'NzA5MDMwMTYxMTgxMzExMjI2.XrpvvQ.WvIHPgJYXzHKAJk4Q3sXoV-0cIA'
bot = commands.Bot(command_prefix='.')

# 凸確認リスト
totsu_list = [[0]for i in range(3)]

# 起動時イベント
@bot.event
async def on_ready():
    print('ログインしました')

@bot.command() 
async def check(ctx,month:int,day:int):
    await totsucheck(ctx,month,day)

async def totsuList(i:int,user_id):
    global totsu_list
    check_count = 0
    for j in totsu_list[i]:
        if j == user_id:
            totsu_list[i].remove(user_id)
            check_count = 1
    if check_count == 0:
        totsu_list[i].append(user_id)
    
async def editMsg(msg,month:int,day:int):
    embed = discord.Embed(title=str(month)+'月'+str(day)+'日の3凸確認表だよ〜',description='***',color=0x4169e1)
    first_num = len(totsu_list[0]) - 1
    second_num = len(totsu_list[1]) - 1
    third_num = len(totsu_list[2]) - 1
    embed.add_field(name='下の絵文字リアクションを押してね',value='1️⃣  1凸完了 '+str(first_num)+'人\n2️⃣  2凸完了 '+str(second_num)+'人\n3️⃣  3凸完了 '+str(third_num)+'人',inline=False)
    await msg.edit(embed=embed)

async def totsucheck(ctx,month:int,day:int):
    embed = discord.Embed(title=str(month)+'月'+str(day)+'日の3凸確認表だよ〜',description='***',color=0x4169e1)
    embed.add_field(name='下の絵文字リアクションを押してね',value='1️⃣ 1凸完了\n2️⃣  2凸完了\n3️⃣  3凸完了',inline=False)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('1️⃣')
    await msg.add_reaction('2️⃣')
    await msg.add_reaction('3️⃣')
    # メッセージのIDを保存する
    msg_id = msg.id
    # メッセージのピン留め
    await msg.pin()
    # リアクション待機
    def check(reaction, user):
        emoji = str(reaction.emoji)
        if user.bot == True:
            pass
        else:
            return emoji == '1️⃣' or emoji == '2️⃣' or emoji == '3️⃣'
    
    while 1:
        reaction, user = await bot.wait_for('reaction_add',check=check,timeout=None)
        message_id = reaction.message.id
        if msg_id == message_id:
            if str(reaction.emoji) == '1️⃣':
                # 1凸完了者の記録
                await totsuList(0,user.id)
                await editMsg(msg,month,day)
            if str(reaction.emoji) == '2️⃣':
                # 2凸完了者の記録
                await totsuList(1,user.id)
                await editMsg(msg,month,day)
            if str(reaction.emoji) == '3️⃣':
                # 3凸完了者の記録
                await totsuList(2,user.id)
                await editMsg(msg,month,day)


bot.run(TOKEN)
