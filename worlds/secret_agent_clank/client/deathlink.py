import time
from typing import Any

from CommonClient import logger
from Utils import async_start


class DeathLinkMixin:
    async def _set_death_link_enabled(self, enabled: bool) -> None:
        self._death_link_enabled = enabled
        await self._worker.request("death_enabled", enabled)
        await self.update_death_link(enabled)
        logger.info(f"[SAC] DeathLink {'enabled' if enabled else 'disabled'}.")

    def _send_death_link_from_sync(self, death: dict[str, str | None]) -> None:
        if death['planet']:
            self.current_planet = death['planet']
        cause = death['cause'] or 'died'
        if not self._death_link_enabled:
            return
        now = time.time()
        if now - self._last_death_link < 1:
            return
        self._last_death_link = now
        source = self.auth or "Ratchet"
        planet_name = self.current_planet or "an unknown planet"
        message = f"{source} {cause} on {planet_name}."
        self._debug_log("[SAC] DeathLink sent.")
        async_start(
            self.send_msgs([{
                "cmd": "Bounce",
                "tags": ["DeathLink"],
                "data": {
                    "time": now,
                    "source": source,
                    "cause": message,
                },
            }])
        )
        async_start(self._worker.request("death_sent", message))

    async def _receive_death_link(self, data: dict[str, Any]) -> None:
        if not self.pine_connected:
            return
        timestamp = float(data.get("time", 0))
        if timestamp and timestamp <= self._last_death_link:
            return
        self._last_death_link = max(timestamp, time.time())
        source = data.get("source", "Unknown")
        cause = data.get("cause") or f"{source} died"
        self._debug_log(f"[SAC] DeathLink received: {cause}")
        async with self._pine_lock:
            await self._worker.request("death", (source, cause))
