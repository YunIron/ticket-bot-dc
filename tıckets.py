import inspect
import discord
from discord import channel
from discord import user
from discord.errors import NotFound
from discord.ui import view
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from discord.utils import get
import asyncio
import time
import datetime
import threading

intents = discord.Intents.default()
intents.members = True
TOKEN = ""
client = discord.Client()
Bot = commands.Bot(command_prefix="!l", intents=intents)
global ticketcount
global tickets
tickets = []
ticketcount = 0


@Bot.event
async def on_ready():
    print("Ben hazirim")
    await ticketolustur()


@Bot.event
async def ticket(ctx, member, interactions):
    global tickets
    guild = ctx.guild
    interaction = interactions
    member = member
    admin_role = get(guild.roles, name="Admin")
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True),
        admin_role: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_text_channel(f"ticket#{ticketcount}", overwrites=overwrites)
    tickets.append(channel.id)
    zaman = datetime.datetime.now()
    Embed = discord.Embed(color=discord.Color.green())
    Embed.add_field(name=F"TICKET#{ticketcount}", value=f"<@{member.id}> buradan ticket ile ilgili bilgileri görebilir ve ya ticket'ı kapatabilirsiniz.", inline=False)
    Embed.add_field(name="Saat", value=f"{zaman.hour}:{zaman.minute}:{zaman.second}", inline=True)
    Embed.add_field(name="Tarih", value=f"{zaman.day}/{zaman.month}/{zaman.year}", inline=True)
    #while True:
    view = ticketclose(member, interaction)
    await channel.set_permissions(guild.default_role, read_messages=False, send_messages=False)
    await channel.set_permissions(member, read_messages=True, send_messages=True)
    await channel.send(embed=Embed, view=view)
    await view.wait()
    #break
    return channel.id
        
    # await channel.send("Oda olusturuldu")

@Bot.event
async def ticketadmins(ctx):
    print(ctx.guild.member_count)
    role = get(ctx.guild.roles, name="Sosis")
    print(ctx.guild.roles)
    #print(Bot.guilds)
    #print(ctx.guild.members)
    for x in ctx.guild.members:
        print(x)

@Bot.event 
async def ticketolustur():
    global users
    users = []
    Embed = discord.Embed(color=discord.Color.green())
    Embed.add_field(name="TICKET OLUSTUR", value=f"Buradan ticket açabilirsiniz.", inline=False)
    channel = Bot.get_channel(912681874026025041)
    msg = await channel.fetch_message(912683195403743264)
    try:
        view = ticketbutton()
        await msg.edit(embed=Embed, view=view)
        #await view.wait()
    except Exception:
        await view.wait()

class ticketbutton(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Ticket Olustur',emoji="📩", style=discord.ButtonStyle.green)
    async def olustur(self, button: discord.ui.Button, interaction: discord.Interaction):
        global users
        global ticketcount
        try:
            self.value = True
            member = interaction.user
            ctx = interaction.message
            ticketcount +=1
            ticket_id = await ticket(ctx, member, interaction)
            #await interaction.response.send_message("Ticket kapatildi", ephemeral=True)
            print("hatada degiliz")
            self.stop()
        except Exception as e:
            print("hata\n", e)
            #self.stop()
            #self.stop()
            #await interaction.response.send_message("Ticket kapatildi", ephemeral=True)

class ticketclose(discord.ui.View):
    global ticketcount
    def __init__(self, member, interaction):
        super().__init__()
        self.value = None
        self.member = member
        self.interactions = interaction

    @discord.ui.button(label='Ticket\'ı kapat',emoji="🔒", style=discord.ButtonStyle.grey)
    async def close(self, button: discord.ui.Button, interaction: discord.Interaction):
        global ticketcount
        global users
        print("geldik")
        self.value = True
        ctx = interaction.message
        dm_user = self.member
        member = interaction.user
        ticketch = interaction.channel
        await ticketch.delete()
        ticketcount -=1
        #channel = await dm_user.create_dm()
        #Embed = discord.Embed(color=discord.Color.red())
        #Embed.add_field(name="TICKET KAPATILDI", value=f"@{member.name} tarafindan ticket kapatildi.", inline=False)
        #await channel.send(embed=Embed)
        await interaction.response.send_message("Ticket kapatildi", ephemeral=True)
        #self.stop()
        
        #tickets.remove(interaction.channel.id)
        #self.stop()

@Bot.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content == "Selam":
        await message.channel.send("Aleykum selam")

    elif message.content.startswith("!l"):
        s = message.content.split(" ")
        if len(s) <= 2:
            if s[1] == "time":
                try:
                    pass
                    #await _time(message)
                except Exception as e:
                    print(e)
            elif s[1] == "mizah":
                import random
                miza = ["napim","bane","31","sen aglion"]
                await message.channel.send(f"{random.choice(miza)}")
            elif s[1] == "private":
                #await private()
                pass
            elif s[1] == "kisiler":
                for x in message.guild.members:
                    print(x)
            elif s[1] == "test":
                view = Confirm()
                await message.channel.send("Deneme", view=view)
                await view.wait()
                if view.value is None:
                    print("Sure asimi")
                elif view.value:
                    print("Sozlesmeyi kabul ettiniz.")
                else:
                    print("Baska zamana o zaman")
        elif len(s) <= 3:
            if s[1] == "temizle":

                await message.channel.purge(limit=int(s[2]))
                
        else:
            await message.channel.purge(limit=1)

Bot.run(TOKEN)