import json
import requests
import asyncio
from datetime import date, datetime
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)
import base64

# Setting configuration values
api_id = ""
api_hash = ""
api_hash = str(api_hash)

phone = ""
username = ""

max_messages_per_channel = 10000 # Number of messages per channel
max_total_messages = 50000 # Total number of overall messages obtained
all_messages = [] # List that holds all messages
channel_messages = [] # List that holds channel messages

filename = "telegram_messages.txt" # Filename that holds all of the saved messages

# List of telegram channels to get messages from.
# This needs to be the share url for 
telegram_channels = [
    "",
]



# async def main(phone):
#     await client.start()
#     print("Client Created")
#     # Ensure you're authorized
#     if await client.is_user_authorized() == False:
#         await client.send_code_request(phone)
#         try:
#             await client.sign_in(phone, input('Enter the code: '))
#         except SessionPasswordNeededError:
#             await client.sign_in(password=input('Password: '))

#     me = await client.get_me()

#     user_input_channel = input('enter entity(telegram URL or entity id):')

#     if user_input_channel.isdigit():
#         entity = PeerChannel(int(user_input_channel))
#     else:
#         entity = user_input_channel

async def get_messages(entity):

    print(f"Gathering messages from {entity}")

    # Clear channel list. If this is the second iteration of the function, then channel_messages is populated and will ruin our counting.
    channel_messages.clear()

    channel = await client.get_entity(entity)

    offset_id = 0
    limit = 100


    while len(all_messages) < max_total_messages and len(channel_messages) < max_messages_per_channel:
        
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))

        if not history.messages:
            break # Break out of the loop
        
        messages = history.messages
        channel_title = str(channel.title)

        # Seems silly, but when we call history.messages it runs everything from the channel
        # This could be an empty message in some cases like when it's just a file attachment
        # I do not enjoy the telegram API...
        for message in messages:

            if message.message:
                message_date = str(message.date)
                message = str(message.message).encode("ascii", errors="ignore").decode()
                line = f"On {message_date} in the telegram channel named {channel_title}, the following message was sent: \n{message}"

                # Doing this because there's all kinds of random stuff and it just seemed easier to b64 everything to keep newlines and such intact.
                b64 = base64.b64encode(line.encode("ascii"))
                b64 = b64.decode("ascii")
                
                # Add new messages to our list
                channel_messages.append(b64)
                all_messages.append(b64)

        offset_id = messages[len(messages) - 1].id
        #total_messages = len(all_messages)

    print(f"Total messages obtained {len(all_messages)}")

'''

Main

'''
async def main():
    print("Hello human")
    print("telegather running...")

    await client.start()

    for c in telegram_channels:
        await get_messages(c)

    with open(filename, 'w', newline='') as file: 
        for l in all_messages:
            file.write(l + "\n")

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)

with client:
    client.loop.run_until_complete(main())

