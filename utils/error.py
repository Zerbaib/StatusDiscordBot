from utils.var import *

def error_embed(e):
    """
    Create an embed with an error message.

    Parameters:
        title (str): The title of the error embed.
        description (str): The description of the error embed.

    Returns:
        disnake.Embed: The error embed.
    """
    body = error_body + f"```{e}```"
    issue_link = "https://github.com/Zerbaib/StatusDiscordBot/issues/new?assignees=Zerbaib&labels=bug"
    embed = disnake.Embed(
        title=error_title,
        description=body,
        color=brand_red
    )
    embed.add_field(
        name="You can now create a Issue on GitHub",
        value=f"Tell us what command and the exeption [**here**]({issue_link})"
    )
    print(f"/n/n{error_title}\n{body}\n/n/n")
    return embed