import discord



helpEmbed = discord.Embed(
    title = f"JoeBot\n",
    description = "Bot prefix: **$**\n\n",
    color = 0x1FB4DA
)

helpEmbed.add_field(name=f"`1.` `afk`", value="Adds the AFK role to user and changes nick to '<name>[AFK]'.\n")

helpEmbed.add_field(name="`2.` `gp <target><count>`", value="ghostpings the target 'count' times.", inline=False)

helpEmbed.add_field(name="`3.` `av <target>`", value="displays target avatar.", inline=False)

helpEmbed.add_field(name="`4.` `em <expression>`", value="Evaluates a python expression (Mod specific)", inline= False)

helpEmbed.add_field(name="`5.` `gh <username>`", value="Displayes the github profile of the target.", inline=False)

helpEmbed.add_field(name="`6.` `j <target>`", value="Jails the target until it is unjailed.", inline= False)

helpEmbed.add_field(name="`7.` `unj <target>`", value="Unjails the target.", inline= False)

helpEmbed.add_field(name="`8.` `mute <target>`", value="Mutes the target", inline=False)

helpEmbed.add_field(name="`9.` `unmute <target>`", value="Unmuted the target", inline=False)

helpEmbed.add_field(name="`10.` `nick <new_nick>`", value="Changes name of user to specified nick.", inline=False)

helpEmbed.add_field(name="`11.` `pc <target>`", value="Gives the discord platform of the target.", inline=False)

helpEmbed.add_field(name="`12.` `r <subreddit_name(required)> <sub_filter> <post_count> <time_filter>`",
    value="Displays reddit posts constraint to the given params.",
    inline=False)


helpEmbed.add_field(name="`13.` `send <channel_id> <message>`", 
    value="Sends <message> to channel constraint to <channel_id>",
    inline=False)


helpEmbed.add_field(name="`14.` `wr <place>`", value="Displays weather for a give <place>.", inline=False)

helpEmbed.add_field(name="`15.` `vct`", value="Sets the server up for a voice chat.", inline=False)

helpEmbed.add_field(name="`16.` `unvct`", value="Resets the server structure.", inline=False)

helpEmbed.add_field(name="`17.` `move <VCid_1> <VCid_2>`", value="Transfers members from VC1 to VC2 contraint to VC IDs", inline=False)

helpEmbed.add_field(name="`18.` `move <member_id>`", value="(ALT) Disconnects member from VC constraint to member ID", inline=False)













helpEmbed.set_thumbnail(url='https://cdn.discordapp.com/avatars/833596215856988190/21baccc64d717a41ec846eaff92bc2d7.webp?size=1024')