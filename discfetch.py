
from login import TOKEN, CLIENT_ID, generalChannelId, botChannelId, ownerId
from imagegetter import get_image
import discord
from discord.ext import tasks
from bulb import changeLighting, restorewhite, setwhite
import asyncio
from spotifyapi import get_current_track

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
lightsyncflag = False


@tree.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction):
    if interaction.user.id == ownerId:
        await tree.sync()
        print('Command tree synced.')
    else:
        await interaction.response.send_message('You must be the owner to use this command!')


@tree.command(name='lightwhite', description='Bright Mid Tone White Lighting')
async def sync(interaction: discord.Interaction):
    if interaction.user.id == ownerId:
        setwhite()
        print("Setting lights to White")
    else:
        await interaction.response.send_message('You must be the owner to use this command!')


@tree.command(name="enablels", description="Toggle Activity-Light Color Sync ON")
async def enablels(interaction: discord.Interaction):
    global lightsyncflag
    lightsyncflag = True
    await interaction.response.send_message("Turning on light sync.")
    await activityCheck.start(interaction)

@tree.command(name="disablels", description="Toggle Activity-Light Color Sync OFF")
async def disablels(interaction: discord.Interaction):
    global lightsyncflag
    lightsyncflag = False
    restorewhite()
    await interaction.response.send_message("Turning off light sync.")


@client.event
async def on_ready():

    print("Ready!")


@tasks.loop(hours=0, minutes=0, seconds=5)
async def activityCheck(interaction):
    if lightsyncflag:
        trackinfo = get_current_track()
        await get_image(trackinfo['imageurl'], trackinfo['track_name'])
        await changeLighting(trackinfo['track_name'])


client.run(TOKEN)
