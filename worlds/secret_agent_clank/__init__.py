"""Archipelago world for Secret Agent Clank (PS2, SCUS-97623)"""
from worlds.LauncherComponents import (
    Component,
    SuffixIdentifier,
    Type,
    components,
    icon_paths,
    launch_subprocess,
)
from worlds.secret_agent_clank.world import (
    SecretAgentClankWorld,  # noqa: F401 — registers world
)


def run_client(_url: str | None = None):
    """Launch the Secret Agent Clank Archipelago client."""
    # Imported here so generation never loads the client's PINE/GUI dependencies.
    from worlds.secret_agent_clank.client import run_client as _run
    launch_subprocess(_run, name="SACClient")


components.append(Component(
    "Secret Agent Clank Client",
    func=run_client,
    component_type=Type.CLIENT,
    file_identifier=SuffixIdentifier(".apsac"),
    description="Launch the Client for connecting to Secret Agent Clank",
    icon="sac_icon",
))

icon_paths["sac_icon"] = f"ap:{__name__}/icon/Secret_Agent_Clank_AP.png"
