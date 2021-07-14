
# Inline Telegram Sticker Bot
A Telegram inline bot to add tags to a sticker to make it easier to find them. Currently Telegram only allows assigning emojis to a sticker, with this bot custom alias(es) or tag(s) can be assigned to stickers just like aliases in emotes on Discord for easier access. The tags are saved into a database. Multiple tags can be added per sticker.

![usage](https://i.imgur.com/m4K86Cw.png)

## Deployment and setup instructions
### Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://www.heroku.com/deploy/?template=https://github.com/JeelPatel231/telegram-inline-sticker-bot)
1. Create a new bot using @BotFather and enable inline mode by sending `/mybots` > Bot Settings > Inline Mode.
2. Use the one-click Heroku deploy button above and provide the bot token for the bot you just created, along with the owner id which can be obtained by sending `/id` to @MissRose_bot.
3. Wait for the bot to get deployed, after it's done turn on the dyno in Heroku. Voila the bot must now be up.

### Manual/native deployment
>You should have redis preinstalled in the server
```sh
git clone https://github.com/JeelPatel231/telegram-inline-sticker-bot
cd telegram-inline-sticker-bot
pip3 install -r requirements.txt
python3 main.py $port (your redis port number)
```
Create 'config.env' in the bot's root directory and copy the contents from sample.env, then create a new bot and provide bot token and owner id.

## Usage
Since the bot is currently W.I.P, you'll have to add yourself into the authorized users list manually to be able to use the bot. Will be fixed later. 

Message the bot in private with `/authorize` while replying to your own message to add yourself into the list of authorized users. 

|Command|Description  
|--|--|
|/authorize|Authorize users, to be used in reply to a message from the person you want to authorize.|
|/addtags|Add tags to a sticker, to be used in reply to a sticker. The command may either used in bot pm or in group but only works if you're in the authorized users list. Example usage: `/addtags tag1 tag2 tag3`.|
|/export|Export the database containing the list of sticker ids and tags
|/import|Imports db from .rdb file, must be used in reply to the file.


## Future plans/todo:
1. Make a web interface to manage/view the stickers and tags.
2. Add command to remove stickers from db.

