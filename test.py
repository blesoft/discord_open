import discord
from discord.ext import commands
# import asyncio
import boss

TOKEN = '*******'
bot = commands.Bot(command_prefix='.')
CHANNEL_ID = boss.CHANNEL_ID

# 設定したbossのデータをとってくる
### bossの基本データ
boss_date_1 = boss.boss_date_formal1
boss_date_2 = boss.boss_date_formal2
boss_date_3 = boss.boss_date_formal3
boss_date_4 = boss.boss_date_formal4
boss_date = boss_date_1
### bossのアイコン
icon1 = boss.boss_icon[0]
icon2 = boss.boss_icon[1]
icon3 = boss.boss_icon[2]
icon4 = boss.boss_icon[3]
icon5 = boss.boss_icon[4]
### 段階数と周数の対応
first = boss.first
second = boss.second
third = boss.third
### botの名前
bot_name = boss.bot_name

# 現在の周回数をカウントする
count = 1

# now と next それぞれの関数の呼ばれた数をカウントする
n_count =[0,0]

# now と next それぞれの直前のメッセージのidを保存する
pre_message_id = [0,0]

# 予約表のlist[何周目][予約メンバー]    
presev_date1 = [[boss.boss_name[0]]for i in range(boss.lap + 1)] # 1体目
presev_date2 = [[boss.boss_name[1]]for i in range(boss.lap + 1)] # 2体目
presev_date3 = [[boss.boss_name[2]]for i in range(boss.lap + 1)] # 3体目
presev_date4 = [[boss.boss_name[3]]for i in range(boss.lap + 1)] # 4体目
presev_date5 = [[boss.boss_name[4]]for i in range(boss.lap + 1)] # 5体目


# 起動時イベント
@bot.event
async def on_ready():
    print('ログインしました')

#.init 予約機能開始 or データ初期化
@bot.command()
async def init(ctx,*args):
    # channelの確認
    channel = ctx.channel.id
    if channel == CHANNEL_ID:
        # 引数の数が違う場合にエラー処理
        if len(args) != 0:
            embed = discord.Embed(title='エラー',description='コマンドに誤りがあります.\n(例:予約機能を開始したいor予約表にリセットをかけたい) .init',color=0xff0000)
            await ctx.send(embed=embed)
        else:
            await initEvent(ctx,count)
    else:
        await msgError(ctx)

#.now 現在の予約表を表示
@bot.command() 
async def now(ctx,*args):
    # channelの確認
    channel = ctx.channel.id
    if channel == CHANNEL_ID:
        # 引数の数が違う場合にエラー処理
        if len(args) != 0:
            embed = discord.Embed(title='エラー',description='コマンドに誤りがあります.\n(例:現在の周を確認したい時) .now',color=0xff0000)
            await ctx.send(embed=embed)
        else:
            await nowEvent(ctx,count)
    else:
        await msgError(ctx)

#.next 次周の予約表を表示
@bot.command()
async def next(ctx,*args):
    # channelの確認
    channel = ctx.channel.id
    if channel == CHANNEL_ID:
        # 引数の数が違う場合にエラー処理
        if len(args) != 0:
            embed = discord.Embed(title='エラー',description='コマンドに誤りがあります.\n(例:次周の予約を入れたいor次周の予約を確認したい時) .next',color=0xff0000)
            await ctx.send(embed=embed)
        else:
            await nextEvent(ctx,count)
    else:
        await msgError(ctx)

#.finish 予約表の更新
@bot.command()
async def finish(ctx,*args):
    # channelの確認
    channel = ctx.channel.id
    if channel == CHANNEL_ID:
        # 引数の数が違う場合にエラー処理
        if len(args) != 0:
            embed = discord.Embed(title='エラー',description='コマンドに誤りがあります.\n(例:現在の周が終わって周が更新された時) .finish',color=0xff0000)
            await ctx.send(embed=embed)
        else:
            await finishEvent(ctx,count)
    else:
        await msgError(ctx)

#.set {数字}　指定した周数の予約表のセット
@bot.command()
async def set(ctx,*args):
    # channelの確認
    channel = ctx.channel.id
    if channel == CHANNEL_ID:
        # 引数の数が違う場合にエラー処理
        if len(args) != 1:
            embed = discord.Embed(title='エラー',description='コマンドに誤りがあります.\n__.set {数字}__で入力してください.\n(例:18周でセットしたい場合) .set 18',color=0xff0000)
            await ctx.send(embed=embed)
        # 引数の値が数字でない場合にエラー処理
        elif args[0].isdecimal() == False:
            embed = discord.Embed(title='エラー',description='コマンドに誤りがあります.\n__.set {数字}__で入力してください.\n(例:18周でセットしたい場合) .set 18',color=0xff0000)
            await ctx.send(embed=embed)
        else:
            number = int(args[0])
            await setEvent(ctx,number)
    else:
        await msgError(ctx)

#.help ヘルプ
@bot.command()
async def h(ctx):
    await helpCommand(ctx)

#.totsu 
@bot.command() 
async def check(ctx,*args):
    # 引数の数が違う場合にエラー
    if len(args) == 2:
        month = int(args[0])
        day = int(args[1])
        await totsucheck(ctx,month,day)
    # 引数の値が数字でない場合にエラー処理
    elif args[0].isdecimal() == False:
        embed = discord.Embed(title='エラー',description='コマンドに誤りがあります.\n__.check {月} {日}__で入力してください.\n(例:5/28でセットしたい場合) .check 5 28',color=0xff0000)
        await ctx.send(embed=embed)
    elif args[1].isdecimal() == False:
        embed = discord.Embed(title='エラー',description='コマンドに誤りがあります.\n__.check {月} {日}__で入力してください.\n(例:5/28でセットしたい場合) .check 5 28',color=0xff0000)
        await ctx.send(embed=embed)
    else :
        embed = discord.Embed(title='エラー',description='コマンドに誤りがあります.\n__.check {月} {日}__で入力してください.\n(例:5/28でセットしたい場合) .check 5 28',color=0xff0000)
        await ctx.send(embed=embed)

###関数###
# init 関数
async def initEvent(ctx,count):
    if count == 1:
        embed = discord.Embed(title='≪二二二二二二┣ o(・∀・ )お覇断剣!!!',description='起動します',color=0x4169e1)
        await ctx.send(embed=embed)
        await nowEvent(ctx,count)
    else:
        embed = discord.Embed(title='全ての予約表を初期化します',description='本当に初期化してもよろしいですか?\n.yes で初期化されます',color=0xff0000)
        await ctx.send(embed=embed)
        @bot.command()
        async def yes(ctx):
            await clear_presev()
            await setEvent(ctx,1)
# now 関数
async def nowEvent(ctx,count):
    embed = discord.Embed(title='第'+str(count)+'周の予約表\n≪二二二二二二┣ o(・∀・ )お覇断剣!!!',description='現在の予約表になります',color=0x4169e1)
    i = 1
    await presev(embed,count,ctx,i)
# next 関数
async def nextEvent(ctx,count):
    # 周回上限数を超えていないかのチェック
    if count > boss.lap:
        embed = discord.Embed(title='エラー',description='入力値が設定した上限周回数を超えています',color=0xff0000)
        await ctx.send(embed=embed)
    else:
        count_next = count + 1
        embed = discord.Embed(title='第'+str(count_next)+'周の予約表\n≪二二二二二二┣ o(・∀・ )お覇断剣!!!',description='次周の予約表になります',color=0x4169e1)
        i = 0
        await presev(embed,count_next,ctx,i)
# finish 関数
async def finishEvent(ctx,count):
    # 周回上限数を超えていないかチェック
    if count > boss.lap:
        embed = discord.Embed(title='エラー',description='入力値が設定した上限周回数を超えています',color=0xff0000)
        await ctx.send(embed=embed)
    else:
        # nextが呼ばれていたかの確認
        if n_count[0] != 0:
            # 呼ばれた回数を0にリセットする
            n_count[0] = 0
            # 前の next メッセージ を消す
            channel = bot.get_channel(CHANNEL_ID)
            msg = await channel.fetch_message(pre_message_id[0])
            await msg.delete()
        number = count + 1
        # 周カウントを1つ増やす
        await numCount(0)
        embed = discord.Embed(title='Conglaturations!',description='次周の予約表に移ります',color=0x4169e1)
        await ctx.send(embed=embed)
        await nowEvent(ctx,number)
# set 関数
async def setEvent(ctx,number):
    i = int(number)
    # 周回上限数を超えていないかチェック
    if i > boss.lap:
        embed = discord.Embed(title='エラー',description='入力値が設定した上限周回数を超えています',color=0xff0000)
        await ctx.send(embed=embed)
    # 0以下になっていないかチェック
    elif i < 1:
        embed = discord.Embed(title='エラー',description='入力値が0以下です.',color=0xff0000)
        await ctx.send(embed=embed)
    else:
        # next が呼ばれていたかの確認
        if n_count[0] != 0:
            # 呼ばれた回数を0にリセットする
            n_count[0] = 0
            # 前の next メッセージ を消す
            channel = bot.get_channel(CHANNEL_ID)
            msg = await channel.fetch_message(pre_message_id[0])
            await msg.delete()
        # 周カウントを指定した数にセットする
        await numCount(i)
        embed = discord.Embed(title='予約表セット'+str(number),description='現在の予約表を'+str(number)+'に更新します',color=0x4169e1)
        await nowEvent(ctx,number)
# help 関数
async def helpCommand(ctx):
    embed = discord.Embed(title='コマンド一覧',description='以下コマンド一覧になります\n**************',color=0xffd900)
    embed.add_field(name='__.init__',value='予約機能の開始,または予約表の初期化',inline=False)
    embed.add_field(name='__.now__',value='現在の予約表を表示',inline=False)
    embed.add_field(name='__.next__',value='次周の予約表を表示',inline=False)
    embed.add_field(name='__.finish__',value='周を更新する',inline=False)
    embed.add_field(name='__.set {数字}__',value='指定した周を現在の周に更新する\n**************',inline=False)
    embed.add_field(name='__注意事項(コマンド)__',value='・全てのコマンドは半角で打ち込んでください.\n・上記のコマンドはバグを起こさないように指定されたチャンネルでしか使用できません.ご了承ください\n・上記のセットコマンドにおいて set と {数字} の間に必ず半角スペースを入れてください.\n・わかりづらい,やりにくい,直して欲しいなどありましたらお気軽にお申し付けください.善処します.\n**************\n**************',inline=False)
    embed.add_field(name='__予約表 使い方__',value='・対応したボスの絵文字リアクション(スタンプ)を押すと,ユーザー名で予約が追加されます.\n・追加された予約を消す場合には対応した絵文字リアクションをもう一度押してください\n**************',inline=False)
    embed.add_field(name='__注意事項(予約表)__',value='予約表は自動で投稿を削除する機能をつけているので手動で投稿を削除する必要はありません.\nむしろバグの原因になってしまう恐れがあるので,削除はお控えください.\n改善できるまでおまちください.ﾍﾟｺﾘｰﾇ',inline=False)
    await ctx.send(embed=embed)
# totsu 関数    
async def totsucheck(ctx,month:int,day:int):
    embed = discord.Embed(title=str(month)+'月'+str(day)+'日の3凸確認表だよ〜',description='***',color=0x4169e1)
    embed.add_field(name='下の絵文字リアクションを押してね',value='1️⃣ 1凸完了\n2️⃣  2凸完了\n3️⃣  3凸完了',inline=False)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('1️⃣')
    await msg.add_reaction('2️⃣')
    await msg.add_reaction('3️⃣')
    # メッセージのピン留め
    await msg.pin()

# エラー処理
async def msgError(ctx):
    embed = discord.Embed(title='エラー',description='申し訳ございません.こちらのチャンネルではそのコマンドの使用が許可されていません.',color=0xff0000)
    await ctx.send(embed=embed)

# 予約表の表示及びリアクション待機
async def presev(embed,num:int,ctx,i:int):
    # now next それぞれの予約表が2回以上よび出されたとき
    if n_count[i] != 0:
        channel = bot.get_channel(CHANNEL_ID)
        msg = await channel.fetch_message(pre_message_id[i])
        await msg.delete()
    # now と　next の呼ばれた数をカウントする
    await nCount(i)
    # bossのデータを更新する
    await boss_date_check(num) 
    embed.add_field(name=boss_date[0][0],value='****** 物防:' + str(boss_date[1][0]) + '\n****** 魔防:' + str(boss_date[2][0]) + await review(presev_date1[num]),inline=False)
    embed.add_field(name=boss_date[0][1],value='****** 物防:' + str(boss_date[1][1]) + '\n****** 魔防:' + str(boss_date[2][1]) + await review(presev_date2[num]),inline=False)
    embed.add_field(name=boss_date[0][2],value='****** 物防:' + str(boss_date[1][2]) + '\n****** 魔防:' + str(boss_date[2][2]) + await review(presev_date3[num]),inline=False)
    embed.add_field(name=boss_date[0][3],value='****** 物防:' + str(boss_date[1][3]) + '\n****** 魔防:' + str(boss_date[2][3]) + await review(presev_date4[num]),inline=False)
    embed.add_field(name=boss_date[0][4],value='****** 物防:' + str(boss_date[1][4]) + '\n****** 魔防:' + str(boss_date[2][4]) + await review(presev_date5[num]),inline=False)
    msg = await ctx.send(embed=embed)
    # リアクションの追加
    await msg.add_reaction(icon1)
    await msg.add_reaction(icon2)
    await msg.add_reaction(icon3)
    await msg.add_reaction(icon4)
    await msg.add_reaction(icon5)
    # メッセージのidを取得
    msg_id = msg.id
    # メッセージのidを保存する
    await message_memory(msg_id,i)
    # 現在の周のみピン留めする
    if i == 1:
        await msg.pin()
    # リアクション待機
    while 1:
        reaction, user = await bot.wait_for('reaction_add',check=check,timeout=None)
        message_id = reaction.message.id
        if user.name != bot_name: # botは無視する
            if msg_id == message_id: # リアクションのあったメッセージが自分のIDであるときのみ反応する
                if str(reaction.emoji) == icon1:
                    # presev_date1[num].append(user.name)
                    # 予約リストに追加 or 削除
                    await add_or_rem(presev_date1[num],user.name)
                    await edit_msg(msg,num,i,ctx)
                if str(reaction.emoji) == icon2:
                    # presev_date2[num].append(user.name)
                    # 予約リストに追加 or 削除
                    await add_or_rem(presev_date2[num],user.name)
                    await edit_msg(msg,num,i,ctx)
                if str(reaction.emoji) == icon3:
                    # presev_date3[num].append(user.name)
                    # 予約リストに追加 or 削除
                    await add_or_rem(presev_date3[num],user.name)
                    await edit_msg(msg,num,i,ctx)
                if str(reaction.emoji) == icon4:
                    # presev_date4[num].append(user.name)
                    # 予約リストに追加 or 削除
                    await add_or_rem(presev_date4[num],user.name)                
                    await edit_msg(msg,num,i,ctx)
                if str(reaction.emoji) == icon5:
                    # presev_date5[num].append(user.name)
                    # 予約リストに追加 or 削除
                    await add_or_rem(presev_date5[num],user.name)
                    await edit_msg(msg,num,i,ctx)
        reaction2, user2 = await bot.wait_for('reaction_remove',check=check,timeout=None)
        message_id = reaction2.message.id
        if user2.name != bot_name: # botは無視する
            if msg_id == message_id: # リアクションのあったメッセージが自分のIDであるときのみ反応する
                if str(reaction2.emoji) == icon1:
                    # presev_date1[num].append(user.name)
                    # 予約リストに追加 or 削除
                    await add_or_rem(presev_date1[num],user2.name)
                    await edit_msg(msg,num,i,ctx)
                if str(reaction2.emoji) == icon2:
                    # presev_date2[num].append(user.name)
                    # 予約リストに追加 or 削除
                    await add_or_rem(presev_date2[num],user2.name)
                    await edit_msg(msg,num,i,ctx)
                if str(reaction2.emoji) == icon3:
                    # presev_date3[num].append(user.name)
                    # 予約リストに追加 or 削除
                    await add_or_rem(presev_date3[num],user2.name)
                    await edit_msg(msg,num,i,ctx)
                if str(reaction2.emoji) == icon4:
                    # presev_date4[num].append(user.name)
                    # 予約リストに追加 or 削除
                    await add_or_rem(presev_date4[num],user2.name)                
                    await edit_msg(msg,num,i,ctx)
                if str(reaction2.emoji) == icon5:
                    # presev_date5[num].append(user.name)
                    # 予約リストに追加 or 削除
                    await add_or_rem(presev_date5[num],user2.name)
                    await edit_msg(msg,num,i,ctx)

# メッセージを編集
async def edit_msg(msg,num,i,ctx):
    if i == 0:
        embed = discord.Embed(title='第'+str(num)+'周の予約表\n≪二二二二二二┣ o(・∀・ )お覇断剣!!!',description='次周の予約表になります',color=0x4169e1)
    if i == 1:
        embed = discord.Embed(title='第'+str(num)+'周の予約表\n≪二二二二二二┣ o(・∀・ )お覇断剣!!!',description='現在の予約表になります',color=0x4169e1)
    # bossのデータを更新する
    await boss_date_check(num)    
    embed.add_field(name=boss_date[0][0],value='****** 物防:' + str(boss_date[1][0]) + '\n****** 魔防:' + str(boss_date[2][0]) + await review(presev_date1[num]),inline=False)
    embed.add_field(name=boss_date[0][1],value='****** 物防:' + str(boss_date[1][1]) + '\n****** 魔防:' + str(boss_date[2][1]) + await review(presev_date2[num]),inline=False)
    embed.add_field(name=boss_date[0][2],value='****** 物防:' + str(boss_date[1][2]) + '\n****** 魔防:' + str(boss_date[2][2]) + await review(presev_date3[num]),inline=False)
    embed.add_field(name=boss_date[0][3],value='****** 物防:' + str(boss_date[1][3]) + '\n****** 魔防:' + str(boss_date[2][3]) + await review(presev_date4[num]),inline=False)
    embed.add_field(name=boss_date[0][4],value='****** 物防:' + str(boss_date[1][4]) + '\n****** 魔防:' + str(boss_date[2][4]) + await review(presev_date5[num]),inline=False)
    await msg.edit(embed=embed)

# 周数をカウント
async def numCount(i:int):
    global count
    if i == 0:
        count += 1
    else :
        count = i

# now と next でそれぞれメッセージのIDを記憶
async def message_memory(message_id,i):
    global pre_message_id
    # if i == 0:
    #     pre_message_id[0] = message_id # next
    # if i == 1:
    #     pre_message_id[1] = message_id # now
    pre_message_id[i] = message_id


# now と next の関数の呼ばれた数をカウント
async def nCount(i):
    global n_count
    # if i == 0:
    #     n_count[0] += 1 # next
    # if i == 1:
    #     n_count[1] += 1 # now
    n_count[i] += 1

# 予約表を初期化する
async def clear_presev():
    global presev_date1
    global presev_date2
    global presev_date3
    global presev_date4
    global presev_date5
    presev_date1.clear
    presev_date2.clear
    presev_date3.clear
    presev_date4.clear
    presev_date5.clear   
    presev_date1 = [[boss.boss_name[0]]for i in range(boss.lap + 1)]  # 1体目
    presev_date2 = [[boss.boss_name[1]]for i in range(boss.lap + 1)] # 2体目
    presev_date3 = [[boss.boss_name[2]]for i in range(boss.lap + 1)] # 3体目
    presev_date4 = [[boss.boss_name[3]]for i in range(boss.lap + 1)] # 4体目
    presev_date5 = [[boss.boss_name[4]]for i in range(boss.lap + 1)] # 5体目

# 周数に応じたbossデータを表示
async def boss_date_check(i):
    global boss_date
    if i <= first:
        boss_date = boss_date_1
    elif i <= second:
        boss_date = boss_date_2
    elif i <= third:
        boss_date = boss_date_3
    else:
        boss_date = boss_date_4

# リアクションチェック
async def check(reaction,user):
    emoji = str(reaction,emoji)
    if user.bot == True:    #botは無視
        pass
    else:
        return emoji == icon1 or emoji == icon2 or emoji == icon3 or emoji == icon4 or emoji == icon5

# 予約の表示
async def review(date):
    name = '\n******予約　'
    if len(date) == 1:
        return name + str(0)
    else :
        name = name + '__'
        for i in range(len(date)):
            if i == 1:
                name = name + date[i] + '__'
            elif i > 1:
                name = name + '\n            　__' + date[i] + '__'
    return name

# 予約の追加/削除
async def add_or_rem(date,uesr_name):
    check_count = 0
    for i in date:
        if i == uesr_name:
            date.remove(uesr_name)
            check_count = 1
    if check_count == 0:
        date.append(uesr_name)

bot.run(TOKEN)