
import numpy as np
import discord
from discord.ext import commands
import time
import csv
import threading
import matplotlib.pyplot as plt
import os
import math


bot = commands.Bot(command_prefix='+', description='econs')

comlist = ['+lb','+shop','+raid','+roll','+tip','+help','+items','+bjall','+factory','+buy','+pur crypj','+sell crypj','cryptoj','+bal']
shoplist = ['Blue stick','Green gum','Flying witch','Penis snake skin','Ugger gun','Snowman nose']
raidlock = 0
#when tick is activated (t = 0 is at integer hour)
ticker = 0

#https://discordapp.com/developers
testkey = ''
realkey = ''

# em = discord.Embed(title='My Embed Title', description='My Embed Content.', colour=0xDEADBF)
#         em.set_author(name='Someone', icon_url=client.user.default_avatar_url)
#         await client.send_message(message.channel, embed=em)



def writefile():
    global gold
    with open('gold.txt', 'w') as csvfile:
        csvfile.write('%s'%(gold))
        
def writeweapon():
    global weapons
    with open('weapons.txt', 'w') as csvfile:
        csvfile.write('%s'%(weapons))
    
def writejuice():
    global juicefactory
    with open('juicefac.txt', 'w') as csvfile:
        csvfile.write('%s'%(juicefactory))

def writejuiceholding():
    global cryptojuiceholding
    with open('cryptojuiceholding.txt', 'w') as csvfile:
        csvfile.write('%s'%(cryptojuiceholding))


with open('juicefac.txt', 'r') as csvfile:
    juicefactory = eval(csvfile.read())

with open('cryptojuiceholding.txt', 'r') as csvfile:
    cryptojuiceholding = eval(csvfile.read())

with open('gold.txt', 'r') as csvfile:
    gold = eval(csvfile.read())

with open('weapons.txt', 'r') as csvfile:
    weapons = eval(csvfile.read())

with open('cryptojuice.txt', 'r') as csvfile:
    cryptoworth = csv.reader(csvfile, delimiter = '\n')



@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    # for server in bot.servers:
    #     for member in server.members:
    #         print(member)
    # await bot.send_message(discord.Object(id='493834729410527234'),  "{}".format('goldbot online. Running version alpha 0.189'))
    



@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    global gold
    global weapons
    global comlist
    global shoplist
    global juicefactory
    global raidlock
    global cryptojuiceholding
    if message.author == bot.user:
        return


    with open('cryptojuiceholding.txt', 'r') as csvfile:
        cryptojuiceholding = eval(csvfile.read())

    with open('gold.txt', 'r') as csvfile:
        gold = eval(csvfile.read())

    with open('weapons.txt', 'r') as csvfile:
        weapons = eval(csvfile.read())

    with open('juicefac.txt', 'r') as csvfile:
        juicefactory = eval(csvfile.read())

    # if message.content.startswith('+awall'):
    #     for key in gold:
    #         gold[key] += 10

    #     #write to database
    #     writefile()
 
    #     await bot.send_message(message.channel, 'Everyone has been awarded 10 gold')
    #     # await bot.send_message(message.channel, '{}'.format(gold))
    #     # msg = gold['{0.author.mention}'.format(message)]
    #     # await bot.send_message(message.channel, msg)

    if message.content.startswith('+create'):
        if '{0.author.mention}'.format(message) in gold:
            await bot.send_message(message.channel, '{0.author.mention} already created!'.format(message))
        else:
            gold['{0.author.mention}'.format(message)] = 1000
            weapons['{0.author.mention}'.format(message)] = 0
            juicefactory['{0.author.mention}'.format(message)] = [10,0,0,0,0]
            cryptojuiceholding['{0.author.mention}'.format(message)] = 0
            await bot.send_message(message.channel, '{0.author.mention} has been created!'.format(message))
            writefile()
            time.sleep(1)
            writeweapon()
            time.sleep(1)
            writejuice()
            time.sleep(1)
            writejuiceholding()

    if message.content.startswith('+lb'):
        j = 1

        lst = []
        with open('cryptojuice.txt', 'r') as csvfile:
            cryptoworth = csv.reader(csvfile, delimiter = '\n')
            for prices in cryptoworth:
                lst.append(round(float(prices[0]),2))
        for key in gold:
            gold[key] = gold[key]+cryptojuiceholding[key]*lst[-1]+juicefactory[key][1]+juicefactory[key][2]+juicefactory[key][3]+juicefactory[key][4]

        with open('juicefac.txt', 'r') as csvfile:
            juicefactory = eval(csvfile.read())

        for key in sorted(gold, key=gold.get, reverse=True):
            await bot.send_message(message.channel, '{}.{}--->NET WORTH:{}<:juice:496261365212905472>||->{}<:cryptojuice:498252039558791189> earning {}<:juice:496261365212905472>/hour'.format(j,key,round(float(gold[key]),2),int(cryptojuiceholding[key]),juicefactory[key][0]))
            j += 1


    if message.content.startswith('+bal'):
        await bot.send_message(message.channel, '{}--->{}<:juice:496261365212905472>||->{}<:cryptojuice:498252039558791189>'.format(message.author.mention,round(float(gold[message.author.mention]),2),int(cryptojuiceholding[message.author.mention])))



    if message.content.startswith('+roll'):
        if '{0.author.mention}'.format(message) not in gold:
            await bot.send_message(message.channel, 'You must be registered to use this command!')
            return

        for weapon in weapons:
            if float(weapons[weapon]) > 0:
                gold[weapon] += weapons[weapon]
                await bot.send_message(message.channel, '{} earned {}<:juice:496261365212905472> because of <:juice:496261365212905472> gaining item.'.format(weapon,weapons[weapon]))
                writefile()

        ran = np.random.randint(0,10)
        randroll = np.random.randint(0,250)
        if ran < 8:
            names2 = []
            for key in gold:
                names2.append(key)
            randomm2 = np.random.randint(0,len(names2)-1)
            if names2[randomm2] != '{0.author.mention}'.format(message):
                gold[str(names2[randomm2])] += randroll
                await bot.send_message(message.channel, 'You suck! now {} WON {} <:juice:496261365212905472> instead!'.format(names2[randomm2],randroll))
                writefile()
            else:
                gold[str(names2[randomm2+1])] += randroll
                await bot.send_message(message.channel, 'You suck! now {} WON {} <:juice:496261365212905472> instead!'.format(names2[randomm2+1],randroll))
                writefile()

        else:
            gold['{0.author.mention}'.format(message)] += randroll
            await bot.send_message(message.channel, '{} WON {} <:juice:496261365212905472>!'.format(message.author.mention,randroll))
            writefile()


    if message.content.startswith('+mobs'):
        if '{0.author.mention}'.format(message) not in gold:
            await bot.send_message(message.channel, 'You must be registered to use this command!')
            return

        for weapon in weapons:
            if float(weapons[weapon]) > 0:
                gold[weapon] += weapons[weapon]
                await bot.send_message(message.channel, '{} earned {}<:juice:496261365212905472> because of <:juice:496261365212905472> gaining item.'.format(weapon,weapons[weapon]))
                writefile()
        writefile()
        lst = ['Green goblin','Larva','Black mamba','Penis snake','Flying drake','Snowman']
        randomm = np.random.randint(0,len(lst))
        names = []
        for key in gold:
            names.append(key)
        randomm2 = np.random.randint(0,len(names))
        randomlost = np.random.randint(0,500)
        # if int(weapons[names[randomm2]]) > 0:
        #     await bot.send_message(message.channel, '{} appeared! It attacked, but {} had strong weapons so he only lost {} gold'.format(lst[randomm],names[randomm2],int(int(randomlost)*(1-int(weapons[names[randomm2]])))))
        #     gold[str(names[randomm2])] -= int(int(randomlost)*0.10)
        # else:
        await bot.send_message(message.channel, '{} appeared! It attacked and {} lost {} <:juice:496261365212905472>'.format(lst[randomm],names[randomm2],randomlost))
        gold[str(names[randomm2])] -= randomlost
        writefile()

    if message.content.startswith('+shop'):
        if '{0.author.mention}'.format(message) not in gold:
            await bot.send_message(message.channel, 'You must be registered to use this command!')
            return

        await bot.send_message(message.channel,'Here is the shop:\n\
        0.\t Juice stand||Price 500||Earning: 100<:juice:496261365212905472> Hour\n \
        1.\t Small juice shop||Price 1,500||Earning: 480<:juice:496261365212905472> Hour\n \
        2.\t Starjuice||Price 5,000||Earning: 2500<:juice:496261365212905472> Hour\n \
        3.\t Mega juice corporation||Price 50,000||Earning: 33200<:juice:496261365212905472> Hour\n \
        ')

        await bot.send_message(message.channel, 'To buy write +buy <number> <amount>')


    if message.content.startswith('+buy '):
        if '{0.author.mention}'.format(message) not in gold:
            await bot.send_message(message.channel, 'You must be registered to use this command!')
            return

        numbershop = int(message.content[-1])
        message.content = message.content.strip('+buy ')
        numbershop = int(message.content[0])
        mounttobuy = int(message.content[1:])


        if numbershop < 4 and numbershop >= 0:

            if gold['{0.author.mention}'.format(message)] < 500*mounttobuy and numbershop == 0:
                await bot.send_message(message.channel, 'You do not have enough juice!')
            elif numbershop == 0 and gold['{0.author.mention}'.format(message)] > 500*mounttobuy:
                gold['{0.author.mention}'.format(message)] -= 500*mounttobuy
                juicefactory['{0.author.mention}'.format(message)][0] += 100*mounttobuy
                juicefactory['{0.author.mention}'.format(message)][1] += 500*mounttobuy
                await bot.send_message(message.channel, 'You succesfully bought Juice stand!')
                writejuice()
                time.sleep(1)
                writefile()


            if gold['{0.author.mention}'.format(message)] < 1500*mounttobuy and numbershop == 1:
                await bot.send_message(message.channel, 'You do not have enough juice!')
            elif numbershop == 1 and gold['{0.author.mention}'.format(message)] > 1500*mounttobuy:
                gold['{0.author.mention}'.format(message)] -= 1500*mounttobuy
                juicefactory['{0.author.mention}'.format(message)][0] += 480*mounttobuy
                juicefactory['{0.author.mention}'.format(message)][2] += 1500*mounttobuy
                await bot.send_message(message.channel, 'You succesfully bought Small juice shop!')
                writejuice()
                time.sleep(1)
                writefile()


            if gold['{0.author.mention}'.format(message)] < 5000*mounttobuy and numbershop == 2:
                await bot.send_message(message.channel, 'You do not have enough juice!')
            elif numbershop == 2 and gold['{0.author.mention}'.format(message)] > 5000*mounttobuy:
                gold['{0.author.mention}'.format(message)] -= 5000*mounttobuy
                juicefactory['{0.author.mention}'.format(message)][0] += 5000*mounttobuy
                juicefactory['{0.author.mention}'.format(message)][3] += 5000*mounttobuy
                await bot.send_message(message.channel, 'You succesfully bought Starjuice!')
                writejuice()
                time.sleep(1)
                writefile()


            if gold['{0.author.mention}'.format(message)] < 50000*mounttobuy and numbershop == 3:
                await bot.send_message(message.channel, 'You do not have enough juice!')
            elif numbershop == 3 and gold['{0.author.mention}'.format(message)] > 50000*mounttobuy:
                gold['{0.author.mention}'.format(message)] -= 50000*mounttobuy
                juicefactory['{0.author.mention}'.format(message)][0] += 33200*mounttobuy
                juicefactory['{0.author.mention}'.format(message)][4] += 50000*mounttobuy
                await bot.send_message(message.channel, 'You succesfully bought Mega juice corporation!')
                writejuice()
                time.sleep(1)
                writefile()
        else:
            await bot.send_message(message.channel, 'Invalid shop number!')







    if message.content.startswith('+help'):
        await bot.send_message(message.channel, '------------------------------------------')
        await bot.send_message(message.channel, '+roll --> Roll dangerously\n +create --> Create new user\n +mobs --> Make wild monster appear\n +lb --> Leaderboard(NET WORTH)\n +bal --> Your current balance\n +shop --> Buy juicefactories to gain hourly juice!\n +fc --> Earn <:juice:496261365212905472> by answering flashcards!\n+tip <@user> --> Tip other users! \
        \n+items --> Show amount of gain given from items/ action.\n+raid <type>(forest/shadowland) --> Start a raid (Cost: 2000<:juice:496261365212905472>/10000<:juice:496261365212905472>).\
        \n+join --> Join the ongoing raid (Cost: 500 <:juice:496261365212905472>/3000 <:juice:496261365212905472>)\n+bjall --> You are feeling so good that you want to spread some love!! (Cost: 500 <:juice:496261365212905472>)\
        \n+pur crypj <amount>--> Purchase cryptojuice\n+sell crypj <amount> --> Sell cryptojuice on the exchange \n+cryptoj --> See the historical prices and your holding')
        await bot.send_message(message.channel, '------------------------------------------')
        version = '0.5, Now with juicefactory!'
        await bot.send_message(message.channel, 'Running version {}'.format(version))





    #reset list (should be kept secret and only sent with PM)
    if message.content.startswith('+reset1115'):
        for key in gold:
            gold[key] = 1000
        for key in juicefactory:
            juicefactory[key] = [10,0,0,0,0]
        for key in weapons:
            weapons[key] = 0
        for key in cryptojuiceholding:
            cryptojuiceholding[key] = 0

        await bot.send_message(message.channel, 'Stats have been reset!')
        writefile()
        time.sleep(2)
        writejuiceholding()
        time.sleep(2)
        writejuice()
        time.sleep(2)
        writeweapon()
        await bot.send_message(discord.Object(id='493834729410527234'),  "{}".format('Stats have been reset by admin!'))
        
        with open('cryptojuice.txt', 'w') as csvfile:
            csvfile.write('406\n396\n392\n388\n378\n384\n370\n348\n342\n342\n358\n370\n364\n370\n350\n358\n370\n356\n362\n368\n362\n370\n360\n368\n362\
                            \n360\n366\n372\n368\n364\n368\n356\n364\n370\n374\n372\n384\n340\n378\n414\n409\n458\n481\n527\n545\n596\n597\n594\n')
            csvfile.close()



    # if message.content.startswith('+fc'):
    #     if '{0.author.mention}'.format(message) not in gold:
    #         await bot.send_message(message.channel, 'You must be registered to use this command!')
    #         return
        
    #     with open('quiz.txt', 'r') as csvfile:
    #         quiz = eval(csvfile.read())


    #     randomquiz = np.random.randint(0,len(quiz))
    #     randomgold = np.random.randint(200,1500)
    #     quizz = list(quiz.keys())[randomquiz]
    #     answer = list(quiz.values())[randomquiz].upper()
    #     await bot.send_message(message.channel, '{}'.format(quizz))

    #     def check(msg):
    #         if msg != None:
    #             msg.content = msg.content.upper()
    #             return msg.content.startswith('{}'.format(answer))
    #         if msg == None:
    #             return None

    #     msg = await bot.wait_for_message(author=message.author, check=check, timeout = 10.0)


    #     if msg != None:
    #         if msg.content == answer:

    #             if float(gold['{0.author.mention}'.format(message)]) > float(1000):
    #                 await bot.send_message(message.channel, 'You are too rich to win.')
    #                 return

    #             await bot.send_message(message.channel, '{} won {}<:juice:496261365212905472>'.format(message.author.mention,randomgold))
    #             gold['{}'.format(message.author.mention)] += randomgold
    #             writefile()

    #             with open('weapons.txt', 'r') as csvfile:
    #                 weapons = eval(csvfile.read())
    #             for weapon in weapons:
    #                 if float(weapons[weapon]) > 0:
    #                     gold[weapon] += weapons[weapon]
    #                     await bot.send_message(message.channel, '{} earned {}<:juice:496261365212905472> because of <:juice:496261365212905472> gaining item.'.format(weapon,weapons[weapon]))
    #                     writefile()
    #     if msg == None:
    #         await bot.send_message(message.channel, 'Failed to respond within 10 seconds')







    if message.content.startswith('+tip'):
        if '{0.author.mention}'.format(message) not in gold:
            await bot.send_message(message.channel, 'You must be registered to use this command!')
            return
        message.content = message.content.strip('+tip ')
        

        for char in range(len(message.content)):
            if message.content[char] != ' ':
                user = message.content[:char+1]
            else:
                tipamount = message.content[char+1:]
                break

        if float(gold['{0.author.mention}'.format(message)]) < float(tipamount):
            await bot.send_message(message.channel, 'You cant tip more <:juice:496261365212905472> then you have')
            return
        
        else:
            await bot.send_message(message.channel, '{} tipped {} with {}<:juice:496261365212905472>.'.format(message.author.mention,user,tipamount))
            gold['{0.author.mention}'.format(message)] -= round(float(tipamount),2)
            gold['{}'.format(user)] += round(float(tipamount),2)
            writefile()







    if message.content.startswith('+items'):
        if '{0.author.mention}'.format(message) not in gold:
            await bot.send_message(message.channel, 'You must be registered to use this command!')
            return
        for weapon in weapons:
            if weapon == message.author.mention:
                await bot.send_message(message.channel, '{} has {}<:juice:496261365212905472> gain per action(mobs/rolls/raids)'.format(message.author.mention,weapons[weapon]))
                






    if message.content.startswith('+bjall'):
        if '{0.author.mention}'.format(message) not in gold:
            await bot.send_message(message.channel, 'You must be registered to use this command!')
            return
        if gold[message.author.mention] < 500:
            await bot.send_message(message.channel, '{} do not have enough <:juice:496261365212905472> to give bj to everyone, the cost is 500 <:juice:496261365212905472>!'.format(message.author.mention))
            return
        gold[message.author.mention] -= 600
        for users in gold:
            gold[users] += 100
        await bot.send_message(message.channel, '<:juice:496261365212905472><:juice:496261365212905472><:juice:496261365212905472><:juice:496261365212905472><:juice:496261365212905472><:juice:496261365212905472>')
        await bot.send_message(message.channel, '{} IS FEELING SO GOOD HE BJ EVERYONE!! <:juice:496261365212905472> YEEEY!!! '.format(message.author.mention))
        await bot.send_message(message.channel, '<:juice:496261365212905472><:juice:496261365212905472><:juice:496261365212905472><:juice:496261365212905472><:juice:496261365212905472><:juice:496261365212905472>')
        writefile()


    if message.content.startswith('+factory'):
        if '{0.author.mention}'.format(message) not in gold:
            await bot.send_message(message.channel, 'You must be registered to use this command!')
            return
        await bot.send_message(message.channel, '{} earn {}<:juice:496261365212905472> Per hour from factories.'.format(message.author.mention,juicefactory[message.author.mention]))




    if message.content.startswith('+raid forest'):
        if '{0.author.mention}'.format(message) not in gold:
            await bot.send_message(message.channel, 'You must be registered to use this command!')
            return
        if raidlock == 1:
            await bot.send_message(message.channel, 'There is already an ongoing raid!')
            return

        
        with open('weapons.txt', 'r') as csvfile:
                    weapons = eval(csvfile.read())

        with open('gold.txt', 'r') as csvfile:
            gold = eval(csvfile.read())



        
        if gold[message.author.mention] < 2000:
            await bot.send_message(message.channel, '{} do not have enough <:juice:496261365212905472> to start FOREST raid! (Cost is 2000<:juice:496261365212905472>)'.format(message.author.mention))
            return

        raidlock = 1
        gold[message.author.mention] -= 2000
        writefile()

        
        for weapon in weapons:
            if float(weapons[weapon]) > 0:
                gold[weapon] += weapons[weapon]
                await bot.send_message(message.channel, '{} earned {}<:juice:496261365212905472> because of <:juice:496261365212905472> gaining item.'.format(weapon,weapons[weapon]))
                writefile()

        forest = ['Green goblin','Larva','Black mamba','Penis snake','Flying drake','Penis snake trophy hunter']
        await bot.send_message(message.channel, '{} has initiated a FOREST raid! Raid starts in 120 seconds!, send +join to join raid (Cost: 500<:juice:496261365212905472>)'.format(message.author.mention))
        raidstarter = message.author.mention
        raidlist = [message.author.mention]
        k = 0
        new = 0
        def check2(msg):
            if msg != None:
                global new
                new = 0
                if gold[msg.author.mention] < 500:
                    return msg
                if msg.author.mention not in raidlist:
                    joinedraid = msg.author.mention
                    raidlist.append(joinedraid)
                    gold[joinedraid] -= 500
                    writefile()
                    new = 1
                    return msg
                else:
                    return msg
        while k < 12:
            msg = await bot.wait_for_message(author=None, check = check2, timeout = 10.0)
            if msg != None and msg.author.mention not in raidlist and msg.content not in comlist and new == 1:
                await bot.send_message(message.channel, '{} has joined the raid!'.format(msg.author.mention))
            if msg != None and msg.author.mention in raidlist and msg.content not in comlist and msg.content[:5] == '+join' and new != 1:
                await bot.send_message(message.channel, '{} Is already in the raid!'.format(msg.author.mention))
            if msg != None and gold[msg.author.mention] < 500 and msg.content not in comlist:
                await bot.send_message(message.channel, '{} do not have enough <:juice:496261365212905472> to join! (Cost is 500<:juice:496261365212905472>)'.format(msg.author.mention))
            k += 1

        await bot.send_message(message.channel, 'Raid started!!')
        await bot.send_message(message.channel, '----------------------------------------')
        looper = 0
        while looper < 3:
            looper += 1
            for raider in raidlist:
                randomfore = np.random.randint(0,len(forest))
                randomdmg = np.random.randint(0,500)
                randomgold = np.random.randint(25000,450000)
                randomloss = np.random.randint(0,600)
                randomitem = np.random.randint(0,500)
                randomcrypto = np.random.randint(0,500)
                if randomdmg < 50:
                    if raider != raidstarter:
                        await bot.send_message(message.channel, '{} got attacked by {} which dealt {} damage since the damage was LOW he won the fight and got {}<:juice:496261365212905472>'.format(raider,forest[randomfore],randomdmg,randomgold))
                        gold[raider] += randomgold
                        if randomitem < 100:
                            rangain = np.random.randint(0,50)
                            randitem = np.random.randint(0,len(shoplist))
                            weapons[raider] += rangain
                            await bot.send_message(message.channel, '{} was very lucky and found {} on the corpse which has {}<:juice:496261365212905472> gain/action.'.format(raider,shoplist[randitem],rangain))
                            writeweapon()
                        if randomcrypto < 100:
                            cryptojuiceholding[raider] += 1
                            writejuiceholding()
                
                    
                    #If raidstarter gain bonus
                    else:
                        await bot.send_message(message.channel, '{} got attacked by {} which dealt {} damage since the damage was LOW he won the fight and got {}<:juice:496261365212905472>'.format(raider,forest[randomfore],randomdmg,randomgold*3))
                        gold[raider] += randomgold*3
                        if randomitem < 100:
                            rangain = np.random.randint(0,50)
                            randitem = np.random.randint(0,len(shoplist))
                            weapons[raider] += rangain*2
                            await bot.send_message(message.channel, '{} was very lucky and found {} on the corpse which has {}<:juice:496261365212905472> gain/action.'.format(raider,shoplist[randitem],rangain))
                            writeweapon()
                        if randomcrypto < 100:
                            cryptojuiceholding[raider] += 2
                            writejuiceholding()

                else:
                    await bot.send_message(message.channel, '{} got attacked by {} which dealt {} damage since the damage was HIGH he lost the fight and lost {}<:juice:496261365212905472>'.format(raider,forest[randomfore],randomdmg,randomloss))
                    gold[raider] -= randomloss
                    writefile()
            raidlock = 0
        




    if message.content.startswith('+raid shadowland'):
        if '{0.author.mention}'.format(message) not in gold:
            await bot.send_message(message.channel, 'You must be registered to use this command!')
            return
        if raidlock == 1:
            await bot.send_message(message.channel, 'There is already an ongoing raid!')
            return


        if gold[message.author.mention] < 10000:
            await bot.send_message(message.channel, '{} do not have enough <:juice:496261365212905472> to start SHADOWLAND raid! (Cost is 10,000 <:juice:496261365212905472>)'.format(message.author.mention))
            return

        raidlock = 1
        gold[message.author.mention] -= 10000
        writefile()

        with open('weapons.txt', 'r') as csvfile:
                    weapons = eval(csvfile.read())
        for weapon in weapons:
            if float(weapons[weapon]) > 0:
                gold[weapon] += weapons[weapon]
                await bot.send_message(message.channel, '{} earned {}<:juice:496261365212905472> because of <:juice:496261365212905472> gaining item.'.format(weapon,weapons[weapon]))
                writefile()

        shadowland = ['Haunting shadow','Mega tormenter','Phantom penis skin','King hydra','Black Cyclon','Hounted greyhound']
        await bot.send_message(message.channel, '{} has initiated a SHADOWLAND raid! Raid starts in 120 seconds!, send +join to join raid (Cost: 3000<:juice:496261365212905472>)'.format(message.author.mention))
        raidstarter = message.author.mention
        raidlist = [message.author.mention]
        k = 0
        new = 0
        def check3(msg):
            if msg != None:
                global new
                new = 0
                if gold[msg.author.mention] < 3000:
                    return msg
                    
                if msg.author.mention not in raidlist:
                    joinedraid = msg.author.mention
                    raidlist.append(joinedraid)
                    gold[joinedraid] -= 3000
                    writefile()
                    new = 1
                    return msg
                
                else:
                    return msg

        while k < 12:
            msg = await bot.wait_for_message(author=None, check = check3, timeout = 10.0)
            if msg != None and msg.author.mention not in raidlist and msg.content not in comlist and new == 1:
                await bot.send_message(message.channel, '{} has joined the raid!'.format(msg.author.mention))
            if msg != None and msg.author.mention in raidlist and msg.content not in comlist and msg.content[:5] == '+join' and new != 1:
                await bot.send_message(message.channel, '{} Is already in the raid!'.format(msg.author.mention))
            if msg != None and gold[msg.author.mention] < 500 and msg.content not in comlist:
                await bot.send_message(message.channel, '{} do not have enough <:juice:496261365212905472> to join! Cost is 500 <:juice:496261365212905472>!'.format(msg.author.mention))
            k += 1

        await bot.send_message(message.channel, 'Raid started!!')
        await bot.send_message(message.channel, '----------------------------------------')
        looper = 0
        while looper < 3:
            looper += 1
            for raider in raidlist:
                randomfore = np.random.randint(0,len(shadowland))
                randomdmg = np.random.randint(500,50000)
                randomgold = np.random.randint(100000,2500000)
                randomloss = np.random.randint(0,600)
                randomitem = np.random.randint(0,500)
                randomcrypto = np.random.randint(0,500)
                if randomdmg < 4000:
                    if raider != raidstarter:
                        await bot.send_message(message.channel, '{} got attacked by {} which dealt {} damage since the damage was LOW he won the fight and got {}<:juice:496261365212905472>'.format(raider,shadowland[randomfore],randomdmg,randomgold))
                        gold[raider] += randomgold
                        if randomitem < 100:
                            rangain = np.random.randint(50,500)
                            randitem = np.random.randint(0,len(shoplist))
                            weapons[raider] += rangain
                            await bot.send_message(message.channel, '{} was very lucky and found {} on the corpse which has {}<:juice:496261365212905472> gain/action.'.format(raider,shoplist[randitem],rangain))
                            writeweapon()
                        if randomcrypto < 100:
                            cryptojuiceholding[raider] += 3
                            writejuiceholding()

            
                
                    #If raidstarter gain bonus
                    else:
                        await bot.send_message(message.channel, '{} got attacked by {} which dealt {} damage since the damage was LOW he won the fight and got {}<:juice:496261365212905472>'.format(raider,shadowland[randomfore],randomdmg,randomgold*3))
                        gold[raider] += randomgold*3
                        if randomitem < 100:
                            rangain = np.random.randint(50,500)
                            randitem = np.random.randint(0,len(shoplist))
                            weapons[raider] += rangain*2
                            await bot.send_message(message.channel, '{} was very lucky and found {} on the corpse which has {}<:juice:496261365212905472> gain/action.'.format(raider,shoplist[randitem],rangain))
                            writeweapon()
                        if randomcrypto < 100:
                            cryptojuiceholding[raider] += 7
                            writejuiceholding()
                else:
                    await bot.send_message(message.channel, '{} got attacked by {} which dealt {} damage since the damage was HIGH he lost the fight and lost {}<:juice:496261365212905472>'.format(raider,shadowland[randomfore],randomdmg,randomloss))
                    gold[raider] -= randomloss
                    writefile()
            raidlock = 0
            

    if message.content.startswith('+cryptoj'):
        if '{0.author.mention}'.format(message) not in gold:
            await bot.send_message(message.channel, 'You must be registered to use this command!')
            return
        lst = []
        with open('cryptojuice.txt', 'r') as csvfile:
            cryptoworth = csv.reader(csvfile, delimiter = '\n')
            for prices in cryptoworth:
                lst.append(round(float(prices[0]),2))
        amountholded = cryptojuiceholding[message.author.mention]
        await bot.send_message(message.channel, 'You hold {} <:cryptojuice:498252039558791189>'.format(amountholded))
        await bot.send_message(message.channel, 'Current price is {}<:juice:496261365212905472>'.format(lst[-1]))
        plt.figure()
        plt.plot(lst, color = 'red', label = 'Current Price %s'%lst[-1])
        plt.title('Prices of Cryptojuice over time')
        plt.xlabel('Time')
        plt.ylabel('Price (in juice)')
        plt.legend(loc = 'best')
        plt.savefig('currentprice.png')

        await bot.send_file(message.channel, 'currentprice.png')
        await bot.send_message(message.channel, 'Price will update every 10 minute.')


    if message.content.startswith('+sell crypj '):
        if '{0.author.mention}'.format(message) not in gold:
            await bot.send_message(message.channel, 'You must be registered to use this command!')
            return
        sellamount = float(message.content.strip('+sell crypj '))

        if cryptojuiceholding[message.author.mention] < sellamount:
            await bot.send_message(message.channel, '{} do not have the amount of <:cryptojuice:498252039558791189> needed'.format(message.author.mention))
        else:
            cryptojuiceholding[message.author.mention] -= sellamount
            lst = []
            with open('cryptojuice.txt', 'r') as csvfile:
                cryptoworth = csv.reader(csvfile, delimiter = '\n')
                for prices in cryptoworth:
                    lst.append(round(float(prices[0]),2))
            gold[message.author.mention] += lst[-1]*sellamount
            await bot.send_message(message.channel, '<:cryptojuice:498252039558791189> sold for {}<:juice:496261365212905472> ({} per cryptojuice)'.format(lst[-1]*sellamount,lst[-1]))
            writefile()
            writejuiceholding()

    if message.content.startswith('+pur crypj '):
        if '{0.author.mention}'.format(message) not in gold:
            await bot.send_message(message.channel, 'You must be registered to use this command!')
            return
        buyamount = float(message.content.strip('+pur crypj '))
        lst = []
        with open('cryptojuice.txt', 'r') as csvfile:
            cryptoworth = csv.reader(csvfile, delimiter = '\n')
            for prices in cryptoworth:
                lst.append(round(float(prices[0]),2))
        
        if gold[message.author.mention] < lst[-1]*buyamount:
            await bot.send_message(message.channel, '{} do not have the amount of <:juice:496261365212905472> needed'.format(message.author.mention))
        else:
            gold[message.author.mention] -= lst[-1]*buyamount
            cryptojuiceholding[message.author.mention] += buyamount
            await bot.send_message(message.channel, 'Bought {} <:cryptojuice:498252039558791189> for {}<:juice:496261365212905472> ({} per cryptojuice)'.format(buyamount,lst[-1]*buyamount,lst[-1]))
            writefile()
            writejuiceholding()







timelock = 0
def juicefacc():
    global ticker
    global timelock
    if time.localtime()[4] != ticker and timelock == 1:
        timelock = 0
        time.sleep(10)
        juicefacc()
    if time.localtime()[4] == ticker and timelock == 0:
        timelock = 1
        global gold
        global juicefactory
        print('Wages: %s'%time.localtime()[4])
        for user in juicefactory:
            value = juicefactory[user][0]
            gold[user] += value
    else:
        time.sleep(10)
        juicefacc()
    writefile()
    juicefacc()



def cryptonjuice():
    time.sleep(5)
    price_list = []
    with open('cryptojuice.txt', 'r') as csvfile:
        cryptoworth = csv.reader(csvfile, delimiter = '\n')
        for worth in cryptoworth:
            price_list.append(round(float(worth[0]),2))
    csvfile.close()
    mu = 0.02
    vol = 0.2
    daily_returns=np.random.normal(mu,vol)+1
    price_list.append(round(price_list[-1]*daily_returns,2))
    with open('cryptojuice.txt', 'a') as csvfile:
        csvfile.write('%s\n'%(round(price_list[-1],2)))
    timercrypto = 60*10
    time.sleep(timercrypto)
    cryptonjuice()



def deletecj():
    time.sleep(10)
    lsttemp = []
    with open('cryptojuice.txt', 'r') as csvfile:
        cryptoworth = csv.reader(csvfile, delimiter = '\n')
        for worth in cryptoworth:
            lsttemp.append(round(float(worth[0]),2))
    csvfile.close()
    randomcrypto = lsttemp[-100:]
    os.remove('cryptojuice.txt')
    for value in randomcrypto:
        with open('cryptojuice.txt', 'a') as csvfile:
            csvfile.write('%s\n'%(value))
    timercrypto = 60*60*24
    time.sleep(timercrypto)
    deletecj()




thread = threading.Thread(target=juicefacc)
thread.start()

thread2 = threading.Thread(target=cryptonjuice)
thread2.start()


thread3 = threading.Thread(target=deletecj)
thread3.start()


bot.run(realkey)




