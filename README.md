# garrison-plugin-minecraft

Garrison RCON plugin for **Minecraft Java Edition** dedicated servers.

## Setup

### Enable RCON on your Minecraft server

Edit `server.properties` and set:

```properties
enable-rcon=true
rcon.password=yourpassword
rcon.port=25575
broadcast-rcon-to-ops=false
```

Restart the server after changing these settings.

### Default ports

| Port  | Service |
|-------|---------|
| 25565 | Game    |
| 25575 | RCON    |

## Notes

- Uses the standard **Source RCON** protocol (same as Factorio and Project Zomboid)
- Commands are prefixed with `/` in-game but sent **without** `/` via RCON
- Responses are plain text, not JSON
- Player limit is reported in the `list` command response
- **Bedrock Edition is not supported** — it uses a different protocol

## Supported commands

**Players** — list, kick, ban, ban-ip, pardon, pardon-ip, banlist, op, deop

**Whitelist** — whitelist add/remove/list/on/off

**Chat** — say, tell

**World** — time set, weather, tp, give, seed, save-all, save-on, save-off

**Server** — difficulty, gamemode, gamerule, scoreboard objectives list, reload, stop
