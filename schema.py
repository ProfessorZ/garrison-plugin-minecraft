"""Minecraft Java Edition RCON command schema v1.0.0."""


def get_commands():
    """Return the list of CommandDef objects for Minecraft Java Edition."""
    from app.plugins.base import CommandDef, CommandParam

    return [
        # ── PLAYER MANAGEMENT ─────────────────────────────────────────
        CommandDef(
            name="list",
            description="List online players",
            category="PLAYER_MGMT",
            example="list",
        ),
        CommandDef(
            name="kick",
            description="Kick a player from the server",
            category="MODERATION",
            params=[
                CommandParam(name="player", type="string", description="Player to kick"),
                CommandParam(name="reason", type="string", required=False, description="Kick reason"),
            ],
            example="kick Steve Griefing",
        ),
        CommandDef(
            name="ban",
            description="Ban a player by username",
            category="MODERATION",
            params=[
                CommandParam(name="player", type="string", description="Player to ban"),
                CommandParam(name="reason", type="string", required=False, description="Ban reason"),
            ],
            example="ban Steve Cheating",
        ),
        CommandDef(
            name="ban-ip",
            description="Ban an IP address or player's IP",
            category="MODERATION",
            params=[
                CommandParam(name="target", type="string", description="Player name or IP address"),
                CommandParam(name="reason", type="string", required=False, description="Ban reason"),
            ],
            example="ban-ip 192.168.1.1",
        ),
        CommandDef(
            name="pardon",
            description="Unban a player",
            category="MODERATION",
            params=[
                CommandParam(name="player", type="string", description="Player to unban"),
            ],
            example="pardon Steve",
        ),
        CommandDef(
            name="pardon-ip",
            description="Unban an IP address",
            category="MODERATION",
            params=[
                CommandParam(name="ip", type="string", description="IP address to unban"),
            ],
            example="pardon-ip 192.168.1.1",
        ),
        CommandDef(
            name="banlist",
            description="List all bans",
            category="MODERATION",
            params=[
                CommandParam(
                    name="type", type="choice", required=False,
                    description="Ban list type",
                    choices=["players", "ips"],
                ),
            ],
            example="banlist players",
        ),
        CommandDef(
            name="op",
            description="Give operator status to a player",
            category="MODERATION",
            params=[
                CommandParam(name="player", type="string", description="Player to op"),
            ],
            example="op Steve",
        ),
        CommandDef(
            name="deop",
            description="Remove operator status from a player",
            category="MODERATION",
            params=[
                CommandParam(name="player", type="string", description="Player to deop"),
            ],
            example="deop Steve",
        ),

        # ── WHITELIST ─────────────────────────────────────────────────
        CommandDef(
            name="whitelist add",
            description="Add player to whitelist",
            category="WHITELIST",
            params=[
                CommandParam(name="player", type="string", description="Player to whitelist"),
            ],
            example="whitelist add Steve",
        ),
        CommandDef(
            name="whitelist remove",
            description="Remove player from whitelist",
            category="WHITELIST",
            params=[
                CommandParam(name="player", type="string", description="Player to remove"),
            ],
            example="whitelist remove Steve",
        ),
        CommandDef(
            name="whitelist list",
            description="List whitelisted players",
            category="WHITELIST",
            example="whitelist list",
        ),
        CommandDef(
            name="whitelist on",
            description="Enable whitelist",
            category="WHITELIST",
            example="whitelist on",
        ),
        CommandDef(
            name="whitelist off",
            description="Disable whitelist",
            category="WHITELIST",
            example="whitelist off",
        ),

        # ── COMMUNICATION ─────────────────────────────────────────────
        CommandDef(
            name="say",
            description="Broadcast a message to all players",
            category="COMMUNICATION",
            params=[
                CommandParam(name="message", type="string", description="Message to broadcast"),
            ],
            example="say Hello everyone!",
        ),
        CommandDef(
            name="tell",
            description="Send a private message to a player",
            category="COMMUNICATION",
            params=[
                CommandParam(name="player", type="string", description="Target player"),
                CommandParam(name="message", type="string", description="Message to send"),
            ],
            example="tell Steve Hello!",
        ),

        # ── SERVER ────────────────────────────────────────────────────
        CommandDef(
            name="stop",
            description="Gracefully shut down the server",
            category="SERVER",
            admin_only=True,
            example="stop",
        ),
        CommandDef(
            name="save-all",
            description="Save the world to disk",
            category="SERVER",
            params=[
                CommandParam(name="flush", type="boolean", required=False, description="Flush all chunks"),
            ],
            example="save-all flush",
        ),
        CommandDef(
            name="save-on",
            description="Enable automatic world saving",
            category="SERVER",
            example="save-on",
        ),
        CommandDef(
            name="save-off",
            description="Disable automatic world saving",
            category="SERVER",
            example="save-off",
        ),
        CommandDef(
            name="reload",
            description="Reload data packs",
            category="SERVER",
            example="reload",
        ),
        CommandDef(
            name="version",
            description="Show server version",
            category="SERVER",
            example="version",
        ),
        CommandDef(
            name="seed",
            description="Show world seed",
            category="SERVER",
            example="seed",
        ),

        # ── WORLD ─────────────────────────────────────────────────────
        CommandDef(
            name="difficulty",
            description="Set server difficulty",
            category="WORLD",
            params=[
                CommandParam(
                    name="difficulty", type="choice",
                    description="Difficulty level",
                    choices=["peaceful", "easy", "normal", "hard"],
                ),
            ],
            example="difficulty normal",
        ),
        CommandDef(
            name="time set",
            description="Set the world time",
            category="WORLD",
            params=[
                CommandParam(name="value", type="string", description="Time value (day, night, noon, midnight, or tick number)"),
            ],
            example="time set day",
        ),
        CommandDef(
            name="weather",
            description="Set the weather",
            category="WORLD",
            params=[
                CommandParam(
                    name="type", type="choice",
                    description="Weather type",
                    choices=["clear", "rain", "thunder"],
                ),
                CommandParam(name="duration", type="integer", required=False, description="Duration in seconds"),
            ],
            example="weather clear",
        ),
        CommandDef(
            name="gamerule",
            description="Get or set a game rule",
            category="WORLD",
            params=[
                CommandParam(name="rule", type="string", description="Game rule name"),
                CommandParam(name="value", type="string", required=False, description="New value"),
            ],
            example="gamerule doDaylightCycle false",
        ),
        CommandDef(
            name="tp",
            description="Teleport a player",
            category="WORLD",
            params=[
                CommandParam(name="target", type="string", description="Player or entity to teleport"),
                CommandParam(name="destination", type="string", description="Destination player or coordinates"),
            ],
            example="tp Steve Alex",
        ),
        CommandDef(
            name="give",
            description="Give an item to a player",
            category="WORLD",
            params=[
                CommandParam(name="player", type="string", description="Target player"),
                CommandParam(name="item", type="string", description="Item ID"),
                CommandParam(name="count", type="integer", required=False, description="Number of items"),
            ],
            example="give Steve minecraft:diamond 64",
        ),
        CommandDef(
            name="kill",
            description="Kill an entity or player",
            category="WORLD",
            params=[
                CommandParam(name="target", type="string", description="Target selector or player name"),
            ],
            example="kill Steve",
        ),
        CommandDef(
            name="summon",
            description="Summon an entity",
            category="WORLD",
            params=[
                CommandParam(name="entity", type="string", description="Entity type to summon"),
            ],
            example="summon minecraft:creeper",
        ),
        CommandDef(
            name="setblock",
            description="Place a block at coordinates",
            category="WORLD",
            params=[
                CommandParam(name="x", type="integer", description="X coordinate"),
                CommandParam(name="y", type="integer", description="Y coordinate"),
                CommandParam(name="z", type="integer", description="Z coordinate"),
                CommandParam(name="block", type="string", description="Block ID"),
            ],
            example="setblock 0 64 0 minecraft:stone",
        ),
    ]
