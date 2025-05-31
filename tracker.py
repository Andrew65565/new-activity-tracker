import requests, time
from datetime import datetime

USER_ID = 2387879471
WEBHOOK_URL = "https://discord.com/api/webhooks/1374885341114142791/YzlOJDCJqe1IsYO4QThuFDNwwRj4ZmWyAqnkN8XIssTuSV1VTfc36cdobdP4HTcNyOFw"

last_presence_type = None
last_avatar_url = None

def get_display_info(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    res = requests.get(url)
    data = res.json()
    return data["name"], data["displayName"]

def get_presence(user_id):
    url = "https://presence.roblox.com/v1/presence/users"
    response = requests.post(url, json={"userIds": [str(user_id)]})
    return response.json()["userPresences"][0]

def get_avatar_headshot(user_id):
    url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=720x720&format=Png&isCircular=false"
    response = requests.get(url)
    return response.json()["data"][0]["imageUrl"]

def log(message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {message}")

def send_discord_message(content):
    payload = {"content": content}
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        log(f"Failed to send to Discord: {e}")

# Get initial info
try:
    username, display_name = get_display_info(USER_ID)
except:
    username, display_name = "Unknown", "Unknown"

startup_msg = f"📡 **Tracking started for {display_name}** (@{username})"
log(startup_msg)
send_discord_message(startup_msg)

while True:
    try:
        presence = get_presence(USER_ID)
        presence_type = presence["userPresenceType"]
        game_name = presence.get("lastLocation", "N/A")

        if presence_type != last_presence_type:
            if presence_type == 2:
                msg = f"🎮 **{display_name} is now IN-GAME** — Playing: `{game_name}`"
            elif presence_type == 1:
                msg = f"🟢 **{display_name} is now ONLINE (not in-game)**"
            else:
                msg = f"🔴 **{display_name} is now OFFLINE**"
            log(msg)
            send_discord_message(msg)
            last_presence_type = presence_type

        # Avatar check
        avatar_url = get_avatar_headshot(USER_ID)
        if avatar_url != last_avatar_url:
            msg = f"🧑‍🎨 **{display_name} updated their avatar!**\n{avatar_url}"
            log(msg)
            send_discord_message(msg)
            last_avatar_url = avatar_url

    except Exception as e:
        log(f"Error occurred: {e}")

    time.sleep(60)
