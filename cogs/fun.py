import random
import discord

from io import BytesIO
from discord.ext import commands
from assets import lists, permissions, http


class Fun_Commands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx, *, question: commands.clean_content):
        """ Consult 8ball to receive an answer """
        answer = random.choice(lists.ballresponse)
        await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {answer}")

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def cat(self, ctx):
        """ Posts a random cat """
        req, cat = await http.get('http://random.cat/meow', as_json=True)

        if cat is None:
            return await ctx.send("Couldn't find any cute cats ;-;")

        await ctx.send(cat['file'])

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def dog(self, ctx):
        """ Posts a random dog """
        req, dog = await http.get('https://random.dog/woof.json', as_json=True)

        if dog is None:
            return await ctx.send("Couldn't find any cute dogs ;-;")

        await ctx.send(dog['url'])

    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ['Heads', 'Tails']
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def urban(self, ctx, *, search: str):
        """ Find the 'best' definition to your words """
        if not permissions.can_embed(ctx):
            return await ctx.send("I cannot send embeds here ;-;")

        req, url = await http.get(f'http://api.urbandictionary.com/v0/define?term={search}', as_json=True)

        if url is None:
            return await ctx.send("I think the API broke...")

        count = len(url['list'])
        if count == 0:
            return await ctx.send("Couldn't find your search in the dictionary...")
        result = url['list'][random.randint(0, count - 1)]

        definition = result['definition']
        if len(definition) >= 1000:
                definition = definition[:1000]
                definition = definition.rsplit(' ', 1)[0]
                definition += '...'

        embed = discord.Embed(colour=0xC29FAF, description=f"**{result['word']}**\n*by: {result['author']}*")
        embed.add_field(name='Definition', value=definition, inline=False)
        embed.add_field(name='Example', value=result['example'], inline=False)
        embed.set_footer(text=f"👍 {result['thumbs_up']} | 👎 {result['thumbs_down']}")

        try:
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("I found something, but have no access to post it... [Embed permissions]")

    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """ !poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    @commands.command()
    async def rate(self, ctx, *, thing: commands.clean_content):
        """ Rates what you desire """
        numbers = random.randint(0, 100)
        decimals = random.randint(0, 9)

        if numbers == 100:
            decimals = 0

        await ctx.send(f"I'd rate {thing} a **{numbers}.{decimals} / 100**")

    @commands.command(aliases=['noticemesenpai'])
    async def noticeme(self, ctx):
        """ Notice me senpai! owo """
        if not permissions.can_upload(ctx):
            return await ctx.send("I cannot send images here ;-;")

        bio = BytesIO(await http.get("https://i.alexflipnote.xyz/500ce4.gif"))
        await ctx.send(file=discord.File(bio, filename="noticeme.gif"))

    @commands.command(aliases=['slots', 'bet'])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        if (a == b == c):
            message = 'and won! 🎉'
        elif (a == b) or (a == c) or (b == c):
            message = 'and almost won (2/3)'
        else:
            message = 'and lost...'

        result = f"**{ctx.author.name}** rolled the slots...\n**[ {a} {b} {c} ]**\n{message}"
        await ctx.send(result)


def setup(bot):
    bot.add_cog(Fun_Commands(bot))
