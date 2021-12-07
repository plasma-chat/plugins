# Copyright 2021 iiPython
# Friend plugin for Plasma

# Modules
import os
import json
from typing import Union

# Configuration
config = {
    "friend_icon": "*"
}

# Load friends
friends_file = os.path.join(os.path.dirname(__file__), "friends.json")
def get_friends() -> list:
    with open(friends_file, "r") as f:
        return json.loads(f.read())

def set_friends(uids: list) -> list:
    with open(friends_file, "w+") as f:
        f.write(json.dumps(uids))

    return uids

try:
    friends = get_friends()

except Exception:
    friends = set_friends([])

# Friends class
class Friends(object):
    def __init__(self, loader) -> None:
        self.loader = loader
        self.plugin_id = "friends"

        self.cmap = {
            "add": self.add,
            "remove": self.remove,
            "list": self.list
        }

        # Metadata
        self.name = "Plasma Embed Creator"
        self.author = "iiPython"

    def list(self, args: list) -> None:
        for u in get_friends():
            self.loader.print(f"{u['name']} - {u['uid'][:6]}")

    def add(self, args: list) -> None:
        try:
            user = args[0]
            for u in self.loader.last.guild.users:
                if u.name == user:
                    set_friends(get_friends() + [{"name": u.name, "uid": u.uid}])
                    return self.loader.print(f"[green]Added {user} to your friends list.")

            return self.loader.print("[red]No user by that name is in the server.")

        except Exception:
            return self.loader.print("[red]No user provided to add.")

    def remove(self, args: list) -> None:
        try:
            user = args[0]
            friends = get_friends()
            for u in friends:
                if u["name"] == user:
                    friends.remove(u)
                    set_friends(friends)
                    return self.loader.print(f"[green]Removed {user} from your friends list.")

            return self.loader.print("[red]No user by that name is your friend.")

        except Exception:
            return self.loader.print("[red]No user provided to remove.")

    def on_fire(self, args: list) -> str:
        if not args:
            for line in [
                "[yellow]Plasma Friend Plugin",
                "  /friends list",
                "  /friends add <user>",
                "  /friends remove <user>"
            ]:
                self.loader.print(line)

            return

        command, args = args[0], args[1:]
        if command in self.cmap:
            return self.cmap[command](args)

        else:
            return self.loader.print(f"[red]Unknown command: '{command}'.[reset]")

    def get_name_prefix(self, user) -> Union[str, None]:
        if user.uid in [u["uid"] for u in get_friends()]:
            return config["friend_icon"] + " "
