"""Minecraft server options — exposed via gamerule commands."""

# Minecraft doesn't have a showoptions-style command.
# Game rules are the closest equivalent and are readable/writable via RCON.

COMMON_GAMERULES = [
    "doDaylightCycle",
    "doWeatherCycle",
    "doMobSpawning",
    "doFireTick",
    "keepInventory",
    "mobGriefing",
    "pvp",
    "doInsomnia",
    "doImmediateRespawn",
    "naturalRegeneration",
    "announceAdvancements",
    "showDeathMessages",
    "commandBlockOutput",
    "logAdminCommands",
    "maxEntityCramming",
    "randomTickSpeed",
    "spawnRadius",
    "maxCommandChainLength",
    "playersSleepingPercentage",
]


def get_gamerule_meta(rule_name: str):
    """Return (option_type, category, description) for a known gamerule."""
    boolean_rules = {
        "doDaylightCycle": ("World", "Whether the daylight cycle progresses"),
        "doWeatherCycle": ("World", "Whether weather changes over time"),
        "doMobSpawning": ("Mobs", "Whether mobs can spawn naturally"),
        "doFireTick": ("World", "Whether fire spreads and extinguishes"),
        "keepInventory": ("Player", "Whether players keep items on death"),
        "mobGriefing": ("Mobs", "Whether mobs can modify blocks"),
        "doInsomnia": ("Mobs", "Whether phantoms spawn when players skip sleep"),
        "doImmediateRespawn": ("Player", "Whether players respawn immediately"),
        "naturalRegeneration": ("Player", "Whether players regenerate health naturally"),
        "announceAdvancements": ("Chat", "Whether advancements are announced in chat"),
        "showDeathMessages": ("Chat", "Whether death messages are shown"),
        "commandBlockOutput": ("Server", "Whether command blocks show output"),
        "logAdminCommands": ("Server", "Whether admin commands are logged"),
    }
    integer_rules = {
        "maxEntityCramming": ("Mobs", "Maximum entities in one space before suffocation"),
        "randomTickSpeed": ("World", "Speed of random block ticks (default 3)"),
        "spawnRadius": ("Player", "Spawn protection radius"),
        "maxCommandChainLength": ("Server", "Maximum command chain length"),
        "playersSleepingPercentage": ("Player", "Percentage of players needed to skip night"),
    }
    if rule_name in boolean_rules:
        cat, desc = boolean_rules[rule_name]
        return "boolean", cat, desc
    if rule_name in integer_rules:
        cat, desc = integer_rules[rule_name]
        return "integer", cat, desc
    return "string", "Other", f"Game rule: {rule_name}"


async def parse_options(send_command):
    """Fetch common gamerules as ServerOption list."""
    from app.plugins.base import ServerOption

    options = []
    for rule in COMMON_GAMERULES:
        try:
            raw = await send_command(f"gamerule {rule}")
            # Response: "doDaylightCycle = true" or "Game rule doDaylightCycle is currently set to: true"
            value = raw.split(":")[-1].strip() if ":" in raw else raw.split("=")[-1].strip()
        except Exception:
            value = ""
        opt_type, category, description = get_gamerule_meta(rule)
        options.append(ServerOption(
            name=rule,
            value=value,
            option_type=opt_type,
            category=category,
            description=description,
        ))
    return options
