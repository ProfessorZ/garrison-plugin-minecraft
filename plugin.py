"""Garrison plugin for Minecraft Java Edition dedicated servers."""

import re

from app.plugins.base import GamePlugin, PlayerInfo, ServerStatus, CommandDef


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
        # Response format: "There are N of a max of M players online: Name1, Name2"
        # Empty server:    "There are 0 of a max of 20 players online:"
        if not raw_response:
            return []
        m = re.search(
            r"There are (\d+) of a max of (\d+) players online:\s*(.*)",
            raw_response,
        )
        if not m:
            return []
        names_str = m.group(3).strip()
        if not names_str:
            return []
        return [
            PlayerInfo(name=name.strip())
            for name in names_str.split(",")
            if name.strip()
        ]

    async def get_status(self, send_command) -> ServerStatus:
        try:
            raw = await send_command("list")
            players = await self.parse_players(raw)
            # Try to get version string
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

