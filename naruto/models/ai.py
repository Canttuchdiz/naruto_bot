from __future__ import annotations
import openai
# from asyncstdlib import enumerate, sorted
from discord import Member, User, TextChannel, Thread, Message, Interaction, Embed, Color
from discord.ext.commands import Bot
from naruto.utils.config import Config
from dataclasses import dataclass
from typing import Union, List


@dataclass
class AIThread:
    op: Union[User, Member]
    topic: str
    channel: Thread

    async def close(self, interaction: Interaction) -> AIThread:
        await interaction.response.send_message("Closing...")
        await self.channel.delete()
        ThreadManager.threads.remove(self)
        return self


class ThreadManager:

    threads: List[AIThread] = []

    def __init__(self, bot: Bot) -> None:
        self.client = bot
        openai.api_key = Config.OPENAI_KEY

    async def last_messages(self, limit: int, channel: Thread) -> str:
        messages = channel.history(limit=limit)
        mystr = []
        iterable = [response async for response in messages if response.author.bot]
        for index, message in enumerate(reversed(iterable)):
            if index == 0:
                mystr.append(f'The first message, written by '
                             f'{"a person" if not message.author.bot else "you"}, says: "{message.content}"')
            else:
                print("occurred")
                mystr.append(f'This is the message after that message, written by '
                             f'{message.author.name if not message.author.bot else "you"}: "{message.content}"')
        return '; '.join(mystr[1:])

    async def conversate(self, message: Message, user: Union[User, Member], channel: Thread) -> str:
        thread = await self.client.fetch_channel(channel.id)
        can_respond = await self.can_respond(user, thread)
        text = await self.prompt_gen(can_respond, message, thread)

        return text

    async def prompt_gen(self, can_respond: bool, message: Message, thread: Thread) -> str:
        text_response = ""
        if can_respond:
            limit = 5 if thread.message_count >= 5 else thread.message_count
            memory = await self.last_messages(limit, thread)
            response = openai.Completion.create(
                engine=Config.MODEL,
                prompt=f"These messages are your memory: {memory}."
                       f"Please respond to the prompt: {message.content} as if you were {Config.CHARACTER}. "
                       f"Respond with less than 185 characters. "
                       f"Be friendly but serious in your responses, and act like {Config.CHARACTER} "
                       f"and naturally like them the character, "
                       f"because you ARE {Config.CHARACTER}.",
                max_tokens=2048,
                temperature=0.75
            )
            text_response = response.choices[0].text
        return text_response

    async def create_thread(self, user: Union[User, Member], topic: str, channel: TextChannel) -> AIThread:
        channel = await channel.create_thread(name=topic)
        embed = Embed(title="Naruto Thread", description=f"**Created by**: ``{user.name}``", color=Color.blue())
        await channel.send(embed=embed)
        thread = AIThread(user, topic, channel)
        self.threads.append(thread)
        return thread

    async def get_thread(self, channel: Thread) -> AIThread:
        for thread in self.threads:
            if thread.channel.id == channel.id:
                return thread

    async def can_respond(self, user: Union[User, Member], channel: Thread) -> bool:
        if not user.bot:
            for thread in self.threads:
                if channel.id == thread.channel.id:
                    return True
            return False


class AI:
    pass
