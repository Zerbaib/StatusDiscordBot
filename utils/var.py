import disnake

config_data = {
    "TOKEN": "your_bot_token",
    "CHAN_ID": None,
    "MSG_ID": None,
    "YOUR_ID": 1234567890,
    "sec_loop": 60,
    "del_time": 3
}

# Emoji config
on = "<:on:1118875860854915152> ``Online``"
idle = "<:idle:1118875857512038560> ``Idle``"
off = "<:off:1118875858841649183> ``Offline``"
not_h = "<:no:1121213438505517197> ``Not Here``"

# Error embed
error_title = "A error as poped !"
error_body = "The exception is\n\n"

# Variables of colors
red = disnake.Color.red()
brand_red = disnake.Color.brand_red()
dark_red = disnake.Color.dark_red()

green = disnake.Color.green()
brand_green = disnake.Color.brand_green()
dark_green = disnake.Color.dark_green()

orange = disnake.Color.orange()
brand_orange = disnake.Color.brand_orange()
dark_orange = disnake.Color.dark_orange()

blurple = disnake.Color.blurple()
random_color = disnake.Color.random()