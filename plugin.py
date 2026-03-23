"""Garrison plugin for Minecraft Java Edition dedicated servers."""

import re
import logging
from datetime import datetime, timezone, timedelta

from app.plugins.base import GamePlugin, PlayerInfo, ServerStatus, CommandDef

logger = logging.getLogger(__name__)

# Track seen log lines per server to avoid duplicate events
# Keyed by server_id -> set of seen raw log lines
_seen_lines: dict[int, set] = {}
# Last poll time per server
_last_poll: dict[int, datetime] = {}


class MinecraftPlugin(GamePlugin):
    """Minecraft Java Edition RCON plugin (standard Source RCON)."""

    custom_connection = False

    @property
    def game_type(self) -> str:
        return "minecraft"

    @property
    def display_name(self) -> str:
        return "Minecraft"

    async def parse_players(self, raw_response: str) -> list[PlayerInfo]:
        """Parse 'list' or 'list uuids' response into PlayerInfo list.

        Standard: "There are N of a max of M players online: Name1, Name2"
        With UUIDs: "There are N of a max of M players online: Name1 (uuid1), Name2 (uuid2)"
        """
        if not raw_response:
            return []
        m = re.search(
            r"There are (\d+) of a max of (\d+) players online:\s*(.*)",
            raw_response,
            re.DOTALL,
        )
        if not m:
            return []
        names_str = m.group(3).strip()
        if not names_str:
            return []

        players = []
        # Try to parse "Name (uuid)" format first
        uuid_pattern = re.compile(
            r"([A-Za-z0-9_]{2,16})\s*\(([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\)"
        )
        uuid_matches = uuid_pattern.findall(names_str)
        if uuid_matches:
            for name, uuid in uuid_matches:
                players.append(PlayerInfo(name=name.strip(), steam_id=uuid))
        else:
            # Plain name list
            for name in names_str.split(","):
                name = name.strip()
                if name:
                    players.append(PlayerInfo(name=name))
        return players

    async def get_players(self) -> list[PlayerInfo]:
        """Not called directly; parse_players is used via get_status."""
        return []

    async def get_status(self, send_command) -> ServerStatus:
        try:
            # Use 'list uuids' to get player UUIDs if available
            raw = await send_command("list uuids")
            if not raw or "There are" not in raw:
                raw = await send_command("list")
            players = await self.parse_players(raw)
            version = None
            try:
                ver_raw = await send_command("version")
                if ver_raw and not ver_raw.startswith("Unknown"):
                    version = ver_raw.strip()
            except Exception:
                pass
            return ServerStatus(
                online=True, player_count=len(players), version=version
            )
        except Exception:
            return ServerStatus(online=False, player_count=0)

    def get_commands(self) -> list[CommandDef]:
        from schema import get_commands
        return get_commands()

    async def get_options(self, send_command):
        from options import parse_options
        return await parse_options(send_command)

    async def set_option(self, send_command, name: str, value: str) -> str:
        return await send_command(f"gamerule {name} {value}")

    async def kick_player(self, send_command, name: str, reason: str = "") -> str:
        cmd = f"kick {name} {reason}".rstrip()
        return await send_command(cmd)

    async def ban_player(self, send_command, name: str, reason: str = "") -> str:
        cmd = f"ban {name} {reason}".rstrip()
        return await send_command(cmd)

    async def unban_player(self, send_command, name: str) -> str:
        return await send_command(f"pardon {name}")

    async def get_player_roles(self) -> list[str]:
        return ["op"]

    async def promote_player(self, send_command, player: str, role: str) -> str:
        return await send_command(f"op {player}")

    async def demote_player(self, send_command, player: str) -> str:
        return await send_command(f"deop {player}")

    async def message_player(self, send_command, name: str, message: str) -> str:
        """Send a private message to a player using /tell."""
        return await send_command(f"tell {name} {message}")

    async def poll_events(self, send_command, since: str | None = None) -> list[dict]:
        """Minecraft RCON has no event stream. Join/leave covered by player tracker."""
        return []

