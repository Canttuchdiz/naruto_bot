import openai
from discord import Interaction, Embed, Color, Message
from discord.app_commands import command, Group
from discord.ext.commands import Cog, Bot
from naruto.models.ai import ThreadManager, Thread
from naruto.utils.config import Config


class Threads(Cog):

    thread_group = Group(name="thread", description="The group for all thread commands")

    def __init__(self, bot: Bot) -> None:
        self.client = bot
        self.manager = ThreadManager(self.client)

    @thread_group.command(name="create", description="Creates a thread")
    async def create(self, interaction: Interaction, topic: str) -> None:
        thread = await self.manager.create_thread(interaction.user, topic, interaction.channel)
        embed = Embed(title="Process Status", description=f"**Status**: *Completed*\n[Channel]"
                                                          f"({thread.channel.jump_url})", color=Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @thread_group.command(name="close", description="Closes a thread")
    async def close(self, interaction: Interaction) -> None:
        thread = await self.manager.get_thread(interaction.channel)
        try:
            await thread.close(interaction)
        except AttributeError as e:
            embed = Embed(title="Process Status", description="**Error**: *Not a thread*", color=Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        response = await self.manager.conversate(message, message.author, message.channel)
        if response:
            await message.reply(response)


async def setup(bot):
    await bot.add_cog(Threads(bot))
