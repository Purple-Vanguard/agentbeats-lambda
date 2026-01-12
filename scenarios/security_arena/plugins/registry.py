#!/usr/bin/env python3
"""
Scenario Plugin Registry

Maps scenario type names to plugin implementations and provides
a factory function to load scenario plugins from configuration.
"""

import importlib.util
from pathlib import Path
from typing import Any

from .base import ScenarioPlugin
from .portfolioiq import PortfolioIQPlugin
from .thingularity import ThingularityPlugin
from .example_medical import MedicalRecordsPlugin


# Registry mapping scenario names to plugin classes
SCENARIO_PLUGINS: dict[str, type[ScenarioPlugin] | None] = {
    "portfolioiq": PortfolioIQPlugin,
    "thingularity": ThingularityPlugin,
    "medical_records": MedicalRecordsPlugin,  # Example custom scenario
    "badblueprint": None,
}


def _load_badblueprint_plugin() -> type[ScenarioPlugin]:
    plugin_path = (
        Path(__file__).resolve().parents[1]
        / "submissions"
        / "purple_vanguard"
        / "badblueprint"
        / "plugin.py"
    )
    if not plugin_path.exists():
        raise ValueError(
            "Missing submission plugin at "
            "scenarios/security_arena/submissions/purple_vanguard/badblueprint/plugin.py"
        )

    spec = importlib.util.spec_from_file_location(
        "pv_badblueprint_plugin",
        plugin_path,
    )
    if spec is None or spec.loader is None:
        raise ValueError("Unable to load badblueprint submission plugin module.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    scenario_type = getattr(module, "SCENARIO_TYPE", None)
    if scenario_type != "badblueprint":
        raise ValueError(
            "Submission plugin SCENARIO_TYPE must be 'badblueprint'."
        )

    plugin_class = getattr(module, "PLUGIN_CLASS", None)
    if plugin_class is None:
        raise ValueError("Submission plugin must define PLUGIN_CLASS.")

    if not issubclass(plugin_class, ScenarioPlugin):
        raise TypeError(
            "Submission plugin PLUGIN_CLASS must inherit from ScenarioPlugin."
        )

    return plugin_class


def load_scenario(scenario_type: str, config: dict[str, Any]) -> ScenarioPlugin:
    """
    Load a scenario plugin by type name.

    Args:
        scenario_type: The scenario type from config (e.g., "portfolioiq")
        config: Configuration dict for the scenario

    Returns:
        Instantiated scenario plugin

    Raises:
        ValueError: If scenario_type is not registered

    Example:
        >>> config = {
        ...     "scenario_type": "portfolioiq",
        ...     "expected_risk_level": "High",
        ...     "target_risk_level": "Low",
        ...     "document_path": "data/ponzicorp_base.json"
        ... }
        >>> scenario = load_scenario("portfolioiq", config)
        >>> print(scenario.get_attack_objective())
    """
    # Local self-check: orchestrator should include "badblueprint" in available
    # scenarios and load with scenario_type="badblueprint" without unknown errors.
    if scenario_type == "badblueprint" and SCENARIO_PLUGINS["badblueprint"] is None:
        SCENARIO_PLUGINS["badblueprint"] = _load_badblueprint_plugin()

    if scenario_type not in SCENARIO_PLUGINS:
        available = ", ".join(SCENARIO_PLUGINS.keys())
        raise ValueError(
            f"Unknown scenario type: '{scenario_type}'. "
            f"Available scenarios: {available}"
        )

    plugin_class = SCENARIO_PLUGINS[scenario_type]

    if not plugin_class:
        raise ValueError(f"Scenario '{scenario_type}' did not load correctly.")

    return plugin_class(config)


def list_scenarios() -> list[str]:
    """
    List all registered scenario types.

    Returns:
        List of scenario type names
    """
    return list(SCENARIO_PLUGINS.keys())


def register_scenario(name: str, plugin_class: type[ScenarioPlugin]) -> None:
    """
    Register a custom scenario plugin.

    This allows participants to add custom scenarios without modifying
    the core registry file.

    Args:
        name: Scenario type name (used in config)
        plugin_class: Plugin class implementing ScenarioPlugin

    Example:
        >>> class CustomPlugin(ScenarioPlugin):
        ...     # ... implement methods ...
        ...     pass
        >>> register_scenario("custom", CustomPlugin)
    """
    if name in SCENARIO_PLUGINS:
        raise ValueError(f"Scenario '{name}' is already registered")

    if not issubclass(plugin_class, ScenarioPlugin):
        raise TypeError(
            f"Plugin class must inherit from ScenarioPlugin, "
            f"got {plugin_class.__name__}"
        )

    SCENARIO_PLUGINS[name] = plugin_class
