import discord
from discord import app_commands, ButtonStyle, Object, Interaction
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
from discord.ui import Button, View
import asyncio
import api_key
from itertools import cycle
import levelsys
import llama
from lia_logger import logger
import traceback
import os
import settings
import platform

# Project LIA Main Code Discord
# Created : 2023.12.21
# Last Modified : 2024.03.02

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
version = "2.0.0"
copyright = "ⓒ2023. MintServer. All rights reserved."
bot_name = ""

@client.event
async def on_ready():
    global bot_name
    bot_name = str(client.user).split("#")[0]
    print("[alert] LIA Module 로드완료")
    print("Discord 로그인 중 입니다..")
    print(f"{client.user}로 로그인되었습니다.")
    settings.setting(bot_name)
    synced = await tree.sync()
    print(f"커맨드 {len(synced)}개 동기화 됨.")
    client.loop.create_task(change_status())
    logger(None,"reboot",None)
    
async def change_status():
    while True:
        status_messages = ["{0}개의 서버에서 서비스".format(len(client.guilds)), "2.0.0 업데이트 홍보", "한국어 지원"]
        for status in status_messages:
            await client.change_presence(activity=discord.Game(name=status))
            await asyncio.sleep(10)

@tree.command(name = 'level', description=f'대화 레벨 확인하기')  
async def level(interaction: discord.Interaction):
    userid = f"<@{interaction.user.id}>"
    levelsys.data_check(userid)
    embed = discord.Embed(title="Level Info", color=0x62c1cc)
    embed.set_author(name=bot_name, icon_url=settings.icon_url)
    embed.set_thumbnail(url=settings.thumbnail)
    embed.add_field(name="Level", value=f"{levelsys.result[1]}", inline=True)
    embed.add_field(name="Count", value=f"{levelsys.result[0]}", inline=True)
    embed.set_footer(text=copyright)
    await interaction.response.send_message(embed=embed) 

@tree.command(name = 'version', description=f'버전 확인하기')  
async def bot_version(interaction: discord.Interaction):
    embed = discord.Embed(title="Version Info", color=0x62c1cc)
    embed.set_author(name=bot_name, icon_url=settings.icon_url)
    embed.set_thumbnail(url=settings.thumbnail)
    embed.add_field(name="Version", value=version, inline=True)
    if settings.version_type == "Debug":
        embed.add_field(name="Version Type", value=f"{settings.version_type}", inline=True)
        embed.add_field(name="Platform", value=f"{platform.system()} {platform.version()}", inline=True)
        embed.add_field(name="Current Model", value=settings.llama_file + " With Ollama", inline=True)
    else:
        embed.add_field(name="Version Type", value=settings.version_type, inline=True)
    embed.set_footer(text=copyright)
    await interaction.response.send_message(embed=embed)


if api_key.type == "Debug":
    @tree.command(name = 'shutdown', description=f'[디버그용] 강제종료')  
    async def shutdown(interaction: discord.Interaction):
        await interaction.response.send_message(f"강제종료 {llama.now}")
        exit()

else:
    pass

@tree.command(name='stream', description='메시지 스트리밍')  
async def stream(interaction: discord.Interaction, prompt: str):
    user_mention = interaction.user.mention
    levelsys.levels(user_mention)
    await interaction.response.send_message(f'메시지를 생성합니다.')
    
    content = []
    chunk_size = 10
    counter = 0
    
    async for data in llama.stream(prompt, interaction.user.name, levelsys.count, levelsys.level):
        content.append(data)
        counter += 1
        if counter % chunk_size == 0:
            await interaction.edit_original_response(content="".join(content))
    if counter % chunk_size != 0:
        await interaction.edit_original_response(content="".join(content))
    
    final_data = "".join(content)

@client.event
async def on_message(message):
    userid = message.author.mention
    if message.author == client.user:
        return
    if message.reference is not None:
        levelsys.levels(userid)
        referenced_message = await message.channel.fetch_message(message.reference.message_id)
        if referenced_message.author == client.user:
            if levelsys.level < levelsys.updated_level:
                await message.channel.send(f'{message.author.mention}님! 레벨{levelsys.level}에서 레벨{levelsys.updated_level}(으)로 레벨업 축하드립니다!', reference=message)
                # logger(message.author.mention, "levelup", message.author.name, None, None, levelsys.level,levelsys.updated_level)
            else:
                # 대화
                chat = llama.chat(message.content, message.author.name, levelsys.count, levelsys.level)
                await message.channel.send(f'{chat}', reference=message)
                # logger(message.author.mention, "normal", message.author.name, message.content, chat)
    elif client.user.mentioned_in(message):
        levelsys.levels(userid)
        mention = client.user.mention
        msg_content = message.content
        mention_index = msg_content.find(mention)
        following_message = msg_content[mention_index + len(mention):].strip()
        if following_message == "":
            # 뒤에 따라오는거 없을떄
            if levelsys.level < levelsys.updated_level:
                await message.channel.send(f'{message.author.mention}님! 레벨{levelsys.level}에서 레벨{levelsys.updated_level}(으)로 레벨업 축하드립니다!')
                # logger(message.author.mention, "levelup", message.author.name, None, None, levelsys.level,levelsys.updated_level)
                await message.channel.send(f'{message.author.mention}님, 멘션 뒤에 하고 싶은 말을 적어주세요!')
                # logger(message.author.mention, "nodata", message.author.name)
            else:
                await message.channel.send(f'{message.author.mention}님, 멘션 뒤에 하고 싶은 말을 적어주세요!')
                # logger(message.author.mention, "nodata", message.author.name)
        # 대화
        elif mention_index != -1:
            if levelsys.level < levelsys.updated_level:
                #레벨업 처리 + 대화
                await message.channel.send(f'{message.author.mention}님! 레벨{levelsys.level}에서 레벨{levelsys.updated_level}(으)로 레벨업 축하드립니다!')
                # logger(message.author.mention, "levelup", message.author.name, None, None, levelsys.level,levelsys.updated_level)
                chat = llama.chat(following_message, message.author.name, levelsys.count, levelsys.level)
                await message.channel.send(f'{chat}', reference=message)
                # logger(message.author.mention, "normal", message.author.name, message.content, chat)
            else:
                # 대화
                chat = llama.chat(following_message, message.author.name, levelsys.count, levelsys.level)
                await message.channel.send(f'{chat}', reference=message)
                # logger(message.author.mention, "normal", message.author.name, message.content, chat)

    elif isinstance(message.channel, discord.DMChannel):
        levelsys.levels(userid)
        if levelsys.level < levelsys.updated_level:
            await message.channel.send(f'{message.author.mention}님! 레벨{levelsys.level}에서 레벨{levelsys.updated_level}(으)로 레벨업 축하드립니다!')
            # logger(message.author.mention, "levelup", message.author.name, None, None, levelsys.level,levelsys.updated_level)
            chat = llama.chat(message.content, message.author.name, levelsys.count, levelsys.level)
            await message.channel.send(f'{chat}')
            # logger(message.author.mention, "normal", message.author.name, message.content, chat)
        else:
            chat = llama.chat(message.content, message.author.name, levelsys.count, levelsys.level)
            await message.channel.send(f'{chat}')
            # logger(message.author.mention, "normal", message.author.name, message.content, chat)

@client.event
async def on_guild_join(guild):
    logger(guild,"join",None)


client.run(api_key.token)