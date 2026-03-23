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
        """Poll Minecraft server events via AMP API console log.

        To enable event polling, configure AMP credentials in the server's
        plugin options or environment:
          AMP_URL: http://cpu01.vps.profszone.xyz:8080
          AMP_USER: admin
          AMP_PASS: <password>
          AMP_INSTANCE: Minecraft01

        Without AMP credentials, returns [] (RCON has no event stream).
        Join/leave events are covered by the player tracker diff.
        """
        import os
        amp_url = os.environ.get("MINECRAFT_AMP_URL", "")
        amp_user = os.environ.get("MINECRAFT_AMP_USER", "")
        amp_pass = os.environ.get("MINECRAFT_AMP_PASS", "")
        amp_instance = os.environ.get("MINECRAFT_AMP_INSTANCE", "Minecraft01")

        if not (amp_url and amp_user and amp_pass):
            return []

        try:
            return await self._poll_amp_console(
                amp_url, amp_user, amp_pass, amp_instance, since
            )
        except Exception as e:
            logger.debug("Minecraft AMP poll failed: %s", e)
            return []

    async def _poll_amp_console(
        self,
        amp_url: str,
        amp_user: str,
        amp_pass: str,
        instance_name: str,
        since: str | None,
    ) -> list[dict]:
        """Fetch console log from AMP API and parse events."""
        import httpx

        async with httpx.AsyncClient(timeout=10.0) as client:
            # 1. Login to AMP
            login_resp = await client.post(
                f"{amp_url}/API/Core/Login",
                headers={"Accept": "application/json"},
                json={
                    "username": amp_user,
                    "password": amp_pass,
                    "token": "",
                    "rememberMe": False,
                },
            )
            login_data = login_resp.json()
            if not login_data.get("success"):
                logger.warning("AMP login failed: %s", login_data.get("resultReason"))
                return []

            session_id = login_data["sessionID"]

            # 2. Get instance ID from ADS
            instances_resp = await client.post(
                f"{amp_url}/API/ADSModule/GetInstances",
                headers={"Accept": "application/json"},
                json={"SESSIONID": session_id},
            )
            instances = instances_resp.json()
            target_url = None
            for controller in instances.get("result", []):
                for inst in controller.get("AvailableInstances", []):
                    if inst.get("InstanceName") == instance_name:
                        target_url = inst.get("ManagementURLFor")
                        break

            if not target_url:
                logger.warning("AMP instance %s not found", instance_name)
                return []

            # 3. Login to the specific instance
            inst_login = await client.post(
                f"{target_url}/API/Core/Login",
                headers={"Accept": "application/json"},
                json={
                    "username": amp_user,
                    "password": amp_pass,
                    "token": "",
                    "rememberMe": False,
                },
            )
            inst_data = inst_login.json()
            if not inst_data.get("success"):
                return []
            inst_session = inst_data["sessionID"]

            # 4. Get console output
            console_resp = await client.post(
                f"{target_url}/API/Core/GetUpdates",
                headers={"Accept": "application/json"},
                json={"SESSIONID": inst_session},
            )
            updates = console_resp.json()
            console_entries = updates.get("result", {}).get("ConsoleEntries", [])

        return _parse_console_entries(console_entries, since)


def _parse_console_entries(entries: list, since: str | None) -> list[dict]:
    """Parse AMP console entries into Garrison events."""
    since_dt = None
    if since:
        try:
            since_dt = datetime.fromisoformat(since)
            if since_dt.tzinfo is None:
                since_dt = since_dt.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            pass

    events = []
    now = datetime.now(timezone.utc)

    for entry in entries:
        contents = entry.get("Contents", "")
        timestamp_str = entry.get("Timestamp")

        # Parse AMP timestamp
        ts = now
        if timestamp_str:
            try:
                ts = datetime.fromisoformat(timestamp_str)
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=timezone.utc)
            except (ValueError, TypeError):
                pass

        if since_dt and ts <= since_dt:
            continue

        # Parse Minecraft log patterns
        # Format: [HH:MM:SS] [Server thread/INFO]: message
        m = re.match(r"\[[\d:]+\] \[Server thread/INFO\]: (.+)", contents)
        if not m:
            # Try without timestamp prefix (AMP may strip it)
            m = re.match(r"(.+)", contents)
            if not m:
                continue
        msg = m.group(1).strip()

        event = _classify_message(msg, ts, contents)
        if event:
            events.append(event)

    return events


def _classify_message(msg: str, ts: datetime, raw: str) -> dict | None:
    """Classify a Minecraft log message into a Garrison event."""
    # Chat: <PlayerName> message
    chat_m = re.match(r"<([A-Za-z0-9_]+)> (.+)", msg)
    if chat_m:
        return {
            "event_type": "chat",
            "timestamp": ts.isoformat(),
            "player_name": chat_m.group(1),
            "message": chat_m.group(2),
            "raw": raw,
        }

    # Join: "PlayerName joined the game"
    join_m = re.match(r"([A-Za-z0-9_]+) joined the game", msg)
    if join_m:
        return {
            "event_type": "connect",
            "timestamp": ts.isoformat(),
            "player_name": join_m.group(1),
            "raw": raw,
        }

    # Leave: "PlayerName left the game"
    leave_m = re.match(r"([A-Za-z0-9_]+) left the game", msg)
    if leave_m:
        return {
            "event_type": "disconnect",
            "timestamp": ts.isoformat(),
            "player_name": leave_m.group(1),
            "raw": raw,
        }

    # Kill/death events — various patterns
    # "PlayerName was slain by X"
    # "PlayerName was killed by X"
    # "PlayerName drowned"
    # "PlayerName burned to death"
    # "PlayerName fell from a high place"
    # "PlayerName was shot by X"
    death_patterns = [
        (r"([A-Za-z0-9_]+) was slain by (.+)", "player_name", "target_name"),
        (r"([A-Za-z0-9_]+) was killed by (.+)", "player_name", "target_name"),
        (r"([A-Za-z0-9_]+) was shot by (.+)", "player_name", "target_name"),
        (r"([A-Za-z0-9_]+) was fireballed by (.+)", "player_name", "target_name"),
        (r"([A-Za-z0-9_]+) was pummeled by (.+)", "player_name", "target_name"),
        (r"([A-Za-z0-9_]+) was blown up by (.+)", "player_name", "target_name"),
        (r"([A-Za-z0-9_]+) drowned.*", "player_name", None),
        (r"([A-Za-z0-9_]+) burned to death.*", "player_name", None),
        (r"([A-Za-z0-9_]+) fell from a high place.*", "player_name", None),
        (r"([A-Za-z0-9_]+) fell out of the world.*", "player_name", None),
        (r"([A-Za-z0-9_]+) starved to death.*", "player_name", None),
        (r"([A-Za-z0-9_]+) suffocated in a wall.*", "player_name", None),
        (r"([A-Za-z0-9_]+) was struck by lightning.*", "player_name", None),
        (r"([A-Za-z0-9_]+) hit the ground too hard.*", "player_name", None),
        (r"([A-Za-z0-9_]+) experienced kinetic energy.*", "player_name", None),
        (r"([A-Za-z0-9_]+) was frozen to death.*", "player_name", None),
        (r"([A-Za-z0-9_]+) tried to swim in lava.*", "player_name", None),
    ]

    for pattern, player_field, killer_field in death_patterns:
        dm = re.match(pattern, msg)
        if dm:
            ev = {
                "event_type": "kill",
                "timestamp": ts.isoformat(),
                "player_name": dm.group(1),
                "raw": raw,
                "message": msg,
            }
            if killer_field and len(dm.groups()) >= 2:
                ev["target_name"] = dm.group(2)
            return ev

    return None
