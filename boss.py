
########   botの名前   #######
bot_name = 'prison.test'
#############################

#予約表を使用したいチャンネル情報#
# チャンネルID (int型 18桁)
### URL:https://support.discord.com/hc/ja/articles/206346498-ユーザー-サーバー-メッセージIDはどこで見つけられる- を参考に取得してください
CHANNEL_ID = *********
#############################


######ボスの名前,各種防御力#####
boss_icon = ['🤢','🦅','🐰','🍡','🐃'] # emoji はお好きなもの次のURLからコピぺしてください https://getemoji.com
boss_name = ['🤢  ゴブリングレート','🦅 ワイルドグリフォン','🐰 メガラパーン','🍡 トライロッカー','🐃　ミノタウロス'] 
boss1_deffence = [[200,200],[225,300],[330,360],[330,360]] 
boss2_deffence = [[200,200],[250,250],[470,470],[500,470]]
boss3_deffence = [[250,250],[390,390],[400,500],[300,440]]
boss4_deffence = [['550/50/200','550/200/50'],['800/60/250','800/250/60'],['1000/80/350','1000/350/80'],['1200/120/450','1200/450/120']]
boss5_deffence = [[240,290],[360,300],[445,200],[600,150]]
# 以下サンプルになります
# マルチタゲの敵には,1つの値に 1000/50/100 のように書き込んでください
# boss_name = [':dog: ボス1',':penguin: ボス2',':cat: ボス3',':fish: ボス4',':rabbit: ボス5']
# boss1_deffence = (1体目:)[[1段階目/物防,1段階目/魔防],[2段階目/物防,2段階目/魔防],[3段階目/物防,3段階目/魔防],[4段階目/物防,4段階目/魔防]] 
# boss2_deffence = (2体目:)....
# boss3_deffence = ...
# boss4_deffence = ...
# boss5_deffence = ...
#############################

########## 周回上限数 #########
lap = 50 ### 自分のクランが超えないであろう値に設定してください.あまり大きな数を入力されると,動作が重くなる恐れがあるのでお気をつけください
#############################

#########  段階数　　##########
first = 3   ### 指定した周数まで1段階
second = 10 ### 指定した周数まで2段階
third = 34  ### 指定した周数まで3段階
#############################


###以下特に変更しなくて大丈夫です###
# 1段階目データ
boss_date_formal1 = [boss_name,
                    [boss1_deffence[0][0],boss2_deffence[0][0],boss3_deffence[0][0],boss4_deffence[0][0],boss5_deffence[0][0]],
                    [boss1_deffence[0][1],boss2_deffence[0][1],boss3_deffence[0][1],boss4_deffence[0][1],boss5_deffence[0][1]]]
# 2段階目データ
boss_date_formal2 = [boss_name,
                    [boss1_deffence[1][0],boss2_deffence[1][0],boss3_deffence[1][0],boss4_deffence[1][0],boss5_deffence[1][0]],
                    [boss1_deffence[1][1],boss2_deffence[1][1],boss3_deffence[1][1],boss4_deffence[1][1],boss5_deffence[1][1]]]
# 3段階目データ
boss_date_formal3 = [boss_name,
                    [boss1_deffence[2][0],boss2_deffence[2][0],boss3_deffence[2][0],boss4_deffence[2][0],boss5_deffence[2][0]],
                    [boss1_deffence[2][1],boss2_deffence[2][1],boss3_deffence[2][1],boss4_deffence[2][1],boss5_deffence[2][1]]]
# 4段階目データ
boss_date_formal4 = [boss_name,
                    [boss1_deffence[3][0],boss2_deffence[3][0],boss3_deffence[3][0],boss4_deffence[3][0],boss5_deffence[3][0]],
                    [boss1_deffence[3][1],boss2_deffence[3][1],boss3_deffence[3][1],boss4_deffence[3][1],boss5_deffence[3][1]]]



