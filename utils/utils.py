import discord

def create_error_embed(title, description):
    emb = discord.Embed(
        title=title,
        color=discord.Color.red(),
    )
    emb.add_field(
        name="Erreur",
        value=description,
    )
    return emb