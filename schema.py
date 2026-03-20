"""Minecraft Java Edition 1.21.11 RCON command schema."""


def get_commands():
    """Return the list of CommandDef objects for Minecraft Java Edition."""
    from app.plugins.base import CommandDef, CommandParam

    return [
        # ── MODERATION ───────────────────────────────────────────────
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
        CommandDef(
            name="kill",
            description="Kill an entity or player",
            category="MODERATION",
            params=[
                CommandParam(name="target", type="string", description="Target selector or player name"),
            ],
            example="kill Steve",
        ),

        # ── WHITELIST ────────────────────────────────────────────────
        CommandDef(
            name="whitelist on",
            description="Enable whitelist enforcement",
            category="WHITELIST",
            example="whitelist on",
        ),
        CommandDef(
            name="whitelist off",
            description="Disable whitelist enforcement",
            category="WHITELIST",
            example="whitelist off",
        ),
        CommandDef(
            name="whitelist list",
            description="List whitelisted players",
            category="WHITELIST",
            example="whitelist list",
        ),
        CommandDef(
            name="whitelist add",
            description="Add a player to the whitelist",
            category="WHITELIST",
            params=[
                CommandParam(name="player", type="string", description="Player to whitelist"),
            ],
            example="whitelist add Steve",
        ),
        CommandDef(
            name="whitelist remove",
            description="Remove a player from the whitelist",
            category="WHITELIST",
            params=[
                CommandParam(name="player", type="string", description="Player to remove"),
            ],
            example="whitelist remove Steve",
        ),
        CommandDef(
            name="whitelist reload",
            description="Reload the whitelist from disk",
            category="WHITELIST",
            example="whitelist reload",
        ),

        # ── SERVER ───────────────────────────────────────────────────
        CommandDef(
            name="say",
            description="Broadcast a message to all players",
            category="SERVER",
            params=[
                CommandParam(name="message", type="string", description="Message to broadcast"),
            ],
            example="say Hello everyone!",
        ),
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
            example="save-all",
        ),
        CommandDef(
            name="save-off",
            description="Disable automatic world saving",
            category="SERVER",
            example="save-off",
        ),
        CommandDef(
            name="save-on",
            description="Enable automatic world saving",
            category="SERVER",
            example="save-on",
        ),
        CommandDef(
            name="reload",
            description="Reload data packs and other server resources",
            category="SERVER",
            example="reload",
        ),
        CommandDef(
            name="seed",
            description="Show world seed",
            category="SERVER",
            example="seed",
        ),
        CommandDef(
            name="version",
            description="Show server version",
            category="SERVER",
            example="version",
        ),
        CommandDef(
            name="setidletimeout",
            description="Set the idle kick timeout in minutes",
            category="SERVER",
            params=[
                CommandParam(name="minutes", type="integer", description="Minutes before idle kick (0 to disable)"),
            ],
            example="setidletimeout 15",
        ),
        CommandDef(
            name="perf",
            description="Start or stop a server performance profiling session",
            category="SERVER",
            example="perf start",
        ),
        CommandDef(
            name="jfr",
            description="Start or stop Java Flight Recorder profiling",
            category="SERVER",
            example="jfr start",
        ),
        CommandDef(
            name="transfer",
            description="Transfer a player to another server",
            category="SERVER",
            example="transfer Steve localhost 25566",
        ),

        # ── WORLD ────────────────────────────────────────────────────
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
            name="difficulty",
            description="Set server difficulty",
            category="WORLD",
            params=[
                CommandParam(
                    name="level", type="choice",
                    description="Difficulty level",
                    choices=["peaceful", "easy", "normal", "hard"],
                ),
            ],
            example="difficulty normal",
        ),
        CommandDef(
            name="defaultgamemode",
            description="Set the default game mode for new players",
            category="WORLD",
            example="defaultgamemode survival",
        ),
        CommandDef(
            name="gamerule",
            description="Get or set a game rule",
            category="WORLD",
            params=[
                CommandParam(name="rule", type="string", description="Game rule name (e.g. keepInventory, doDaylightCycle, doWeatherCycle, doFireTick, mobGriefing, pvp, randomTickSpeed, immediateRespawn, fallDamage, fireDamage, drowningDamage, freezeDamage, doInsomnia, spawnRadius, maxEntityCramming, etc.)"),
                CommandParam(name="value", type="string", required=False, description="New value (true/false for booleans, integer for numeric rules)"),
            ],
            example="gamerule doDaylightCycle false",
        ),
        CommandDef(
            name="worldborder",
            description="Manage the world border size and properties",
            category="WORLD",
            example="worldborder set 10000",
        ),
        CommandDef(
            name="setworldspawn",
            description="Set the world spawn point",
            category="WORLD",
            example="setworldspawn 0 64 0",
        ),
        CommandDef(
            name="spawnpoint",
            description="Set a player's spawn point",
            category="WORLD",
            example="spawnpoint Steve 0 64 0",
        ),
        CommandDef(
            name="fill",
            description="Fill a region with a specific block",
            category="WORLD",
            example="fill 0 64 0 10 64 10 minecraft:stone",
        ),
        CommandDef(
            name="fillbiome",
            description="Fill a region with a specific biome",
            category="WORLD",
            example="fillbiome 0 -64 0 100 320 100 minecraft:plains",
        ),
        CommandDef(
            name="setblock",
            description="Place a block at coordinates",
            category="WORLD",
            example="setblock 0 64 0 minecraft:stone",
        ),
        CommandDef(
            name="forceload",
            description="Force chunks to remain loaded",
            category="WORLD",
            example="forceload add 0 0",
        ),
        CommandDef(
            name="clone",
            description="Clone a region of blocks to another location",
            category="WORLD",
            example="clone 0 64 0 10 70 10 20 64 20",
        ),
        CommandDef(
            name="place",
            description="Place a feature, structure, template, or jigsaw at a location",
            category="WORLD",
            example="place feature minecraft:oak 0 64 0",
        ),

        # ── PLAYERS ──────────────────────────────────────────────────
        CommandDef(
            name="list",
            description="List online players",
            category="PLAYERS",
            example="list",
        ),
        CommandDef(
            name="gamemode",
            description="Set a player's game mode",
            category="PLAYERS",
            params=[
                CommandParam(
                    name="gamemode", type="choice",
                    description="Game mode",
                    choices=["survival", "creative", "adventure", "spectator"],
                ),
                CommandParam(name="target", type="string", required=False, description="Target player (defaults to self)"),
            ],
            example="gamemode creative Steve",
        ),
        CommandDef(
            name="tp",
            description="Teleport a player to a destination",
            category="PLAYERS",
            params=[
                CommandParam(name="target", type="string", description="Player or entity to teleport"),
                CommandParam(name="destination", type="string", description="Destination player or coordinates (x y z)"),
            ],
            example="tp Steve Alex",
        ),
        CommandDef(
            name="spectate",
            description="Spectate an entity in spectator mode",
            category="PLAYERS",
            example="spectate Steve Alex",
        ),
        CommandDef(
            name="effect",
            description="Give or remove status effects",
            category="PLAYERS",
            example="effect give Steve minecraft:speed 60 1",
        ),
        CommandDef(
            name="enchant",
            description="Enchant a player's held item",
            category="PLAYERS",
            example="enchant Steve minecraft:sharpness 5",
        ),
        CommandDef(
            name="experience",
            description="Add, set, or query player experience (alias: xp)",
            category="PLAYERS",
            example="experience add Steve 100 points",
        ),
        CommandDef(
            name="give",
            description="Give an item to a player",
            category="PLAYERS",
            params=[
                CommandParam(name="target", type="string", description="Target player"),
                CommandParam(name="item", type="string", description="Item ID (e.g. minecraft:diamond)"),
                CommandParam(name="count", type="integer", required=False, description="Number of items (default 1)"),
            ],
            example="give Steve minecraft:diamond 64",
        ),
        CommandDef(
            name="clear",
            description="Clear items from a player's inventory",
            category="PLAYERS",
            example="clear Steve minecraft:dirt",
        ),
        CommandDef(
            name="spreadplayers",
            description="Spread players around a point",
            category="PLAYERS",
            example="spreadplayers 0 0 10 100 false @a",
        ),
        CommandDef(
            name="title",
            description="Display a title on a player's screen",
            category="PLAYERS",
            example='title Steve title {"text":"Welcome!"}',
        ),
        CommandDef(
            name="tellraw",
            description="Send a JSON text message to players",
            category="PLAYERS",
            example='tellraw @a {"text":"Hello","color":"gold"}',
        ),
        CommandDef(
            name="msg",
            description="Send a private message to a player (aliases: tell, w)",
            category="PLAYERS",
            example="msg Steve Hello!",
        ),
        CommandDef(
            name="me",
            description="Send an action message in chat",
            category="PLAYERS",
            example="me is building a house",
        ),
        CommandDef(
            name="recipe",
            description="Give or take recipes from a player",
            category="PLAYERS",
            example="recipe give Steve *",
        ),
        CommandDef(
            name="tag",
            description="Manage entity tags",
            category="PLAYERS",
            example="tag Steve add vip",
        ),
        CommandDef(
            name="team",
            description="Manage scoreboard teams",
            category="PLAYERS",
            example="team add red",
        ),
        CommandDef(
            name="teammsg",
            description="Send a message to team members (alias: tm)",
            category="PLAYERS",
            example="teammsg Hello team!",
        ),

        # ── DATA ─────────────────────────────────────────────────────
        CommandDef(
            name="data",
            description="Get, merge, modify, or remove NBT data from entities, blocks, or storage",
            category="DATA",
            example="data get entity Steve",
        ),
        CommandDef(
            name="datapack",
            description="Manage data packs (enable, disable, list)",
            category="DATA",
            example="datapack list",
        ),
        CommandDef(
            name="function",
            description="Run a data pack function",
            category="DATA",
            example="function mypack:my_function",
        ),
        CommandDef(
            name="execute",
            description="Execute a command with modified context (as, at, if, unless, etc.)",
            category="DATA",
            example="execute as @a at @s run say hello",
        ),
        CommandDef(
            name="scoreboard",
            description="Manage scoreboard objectives and player scores",
            category="DATA",
            example="scoreboard objectives list",
        ),
        CommandDef(
            name="bossbar",
            description="Create and manage boss bars",
            category="DATA",
            example="bossbar add mybar \"My Bar\"",
        ),
        CommandDef(
            name="advancement",
            description="Grant or revoke advancements",
            category="DATA",
            example="advancement grant Steve everything",
        ),
        CommandDef(
            name="attribute",
            description="Get or modify entity attributes",
            category="DATA",
            example="attribute Steve minecraft:generic.max_health base get",
        ),
        CommandDef(
            name="schedule",
            description="Schedule a function to run after a delay",
            category="DATA",
            example="schedule function mypack:delayed 100t",
        ),
        CommandDef(
            name="trigger",
            description="Set or add to a trigger objective (usable by non-ops)",
            category="DATA",
            example="trigger my_objective set 1",
        ),
        CommandDef(
            name="locate",
            description="Locate the nearest structure or biome",
            category="DATA",
            example="locate structure minecraft:village_plains",
        ),
        CommandDef(
            name="loot",
            description="Drop, give, insert, or replace loot from a loot table",
            category="DATA",
            example="loot give Steve loot minecraft:chests/simple_dungeon",
        ),
        CommandDef(
            name="item",
            description="Manipulate items in inventories and item slots",
            category="DATA",
            example="item replace entity Steve weapon.mainhand with minecraft:diamond_sword",
        ),
        CommandDef(
            name="summon",
            description="Summon an entity at a location",
            category="DATA",
            example="summon minecraft:creeper ~ ~ ~",
        ),
        CommandDef(
            name="particle",
            description="Create particle effects",
            category="DATA",
            example="particle minecraft:flame ~ ~1 ~ 0.5 0.5 0.5 0.01 100",
        ),
        CommandDef(
            name="playsound",
            description="Play a sound to players",
            category="DATA",
            example="playsound minecraft:entity.experience_orb.pickup master Steve",
        ),
        CommandDef(
            name="stopsound",
            description="Stop playing sounds to a player",
            category="DATA",
            example="stopsound Steve",
        ),
        CommandDef(
            name="random",
            description="Generate random values or manage random sequences",
            category="DATA",
            example="random value 1..6",
        ),
        CommandDef(
            name="return",
            description="Return a value from a function",
            category="DATA",
            example="return 1",
        ),
        CommandDef(
            name="ride",
            description="Mount or dismount entities",
            category="DATA",
            example="ride Steve mount @e[type=horse,limit=1]",
        ),
        CommandDef(
            name="rotate",
            description="Rotate an entity to face a direction",
            category="DATA",
            example="rotate Steve 90 0",
        ),
        CommandDef(
            name="tick",
            description="Control the server tick rate (freeze, step, rate)",
            category="DATA",
            example="tick rate 20",
        ),
        CommandDef(
            name="stopwatch",
            description="Measure elapsed time for profiling",
            category="DATA",
            example="stopwatch start",
        ),
        CommandDef(
            name="test",
            description="Run game test functions",
            category="DATA",
            example="test runall",
        ),
        CommandDef(
            name="debug",
            description="Start or stop a debug profiling session",
            category="DATA",
            example="debug start",
        ),
        CommandDef(
            name="damage",
            description="Deal damage to entities",
            category="DATA",
            example="damage Steve 5 minecraft:generic",
        ),
        CommandDef(
            name="dialog",
            description="Show or manage NPC dialogs",
            category="DATA",
            example="dialog open Steve my_dialog",
        ),
        CommandDef(
            name="fetchprofile",
            description="Fetch a player's profile from the session service",
            category="DATA",
            example="fetchprofile Steve",
        ),
        CommandDef(
            name="waypoint",
            description="Manage waypoints",
            category="DATA",
            example="waypoint add home 0 64 0",
        ),
        CommandDef(
            name="help",
            description="Show command help",
            category="UTILITY",
            params=[CommandParam(name="command", type="string", required=False, description="Command to get help for")],
            example="help kick",
        ),
        CommandDef(
            name="teleport",
            description="Teleport entities to a location or player (alias: tp)",
            category="WORLD",
            params=[
                CommandParam(name="target", type="string", description="Entity or player to teleport"),
                CommandParam(name="destination", type="string", description="Destination player or coordinates"),
            ],
            example="teleport Steve Alex",
        ),
        CommandDef(
            name="time",
            description="Query or change world time",
            category="WORLD",
            params=[
                CommandParam(name="action", type="string", description="set/add/query"),
                CommandParam(name="value", type="string", required=False, description="day/night/noon/midnight/number"),
            ],
            example="time set day",
        ),
        CommandDef(
            name="whitelist",
            description="Manage the server whitelist",
            category="MODERATION",
            params=[
                CommandParam(name="action", type="string", description="on/off/list/add/remove/reload"),
                CommandParam(name="player", type="string", required=False, description="Player name (for add/remove)"),
            ],
            example="whitelist add Steve",
        ),
    ]
