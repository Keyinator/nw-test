from typing import Optional

import discord
from redbot.core import Config, commands


class AtcCog(commands.Cog):
    def __init__(self):
        self.config = Config.get_conf(self, identifier=1846792015)

        default_guild = {
            "blacklisted_users": [],
        }
        self.config.register_guild(**default_guild)

    @commands.command()
    async def say(self, ctx: commands.Context, channel: Optional[discord.TextChannel] = None, *, content: str):
        """Responds (to optional channel) the supplied message"""
        blacklist = await self.config.guild(ctx.guild).blacklisted_users()
        if ctx.message.author.id not in blacklist:
            async with ctx.typing():
                if channel:
                    await channel.send(content)
                else:
                    await ctx.send(content)
        else:
            return

    @commands.group(pass_context=True)
    @commands.guild_only()
    @commands.mod_or_permissions(manage_messages=True)
    async def blist(self, ctx: commands.Context):
        """Blacklist of whoever should not be able to interact with the bot"""
        async with ctx.typing():
            if ctx.invoked_subcommand is None:
                await ctx.send('Please use either ``add`` or ``rem``')

    @blist.command(pass_context=True)
    async def add(self, ctx: commands.Context, user: discord.User):
        """Add Member to the blacklist"""
        async with ctx.typing():
            guild_group = self.config.guild(ctx.guild)
            async with guild_group.blacklisted_users() as blacklist:
                if user.id in blacklist:
                    await ctx.send('{0} already on blacklist.'.format(user))
                else:
                    blacklist.append(user.id)
                    await ctx.send('Added {0} to the blacklist'.format(user))

    @blist.command(pass_context=True)
    async def rem(self, ctx: commands.Context, user: discord.User):
        """Remove Member from the blacklist"""
        async with ctx.typing():
            guild_group = self.config.guild(ctx.guild)
            async with guild_group.blacklisted_users() as blacklist:
                if user.id in blacklist:
                    blacklist.remove(user.id)
                    await ctx.send('Removed {0} from the blacklist'.format(user))
                else:
                    await ctx.send('{0} not on the blacklist'.format(user))

    @blist.command(pass_context=True)
    async def list(self, ctx: commands.Context):
        """Output blacklist"""
        async with ctx.typing():
            guild_group = await self.config.guild(ctx.guild).blacklisted_users()
            if len(guild_group) != 0:
                await ctx.send("\n".join(str(ctx.bot.get_user(user)) for user in guild_group))
            else:
                await ctx.send('Blacklist empty')
