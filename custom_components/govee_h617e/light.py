"""Light platform for Govee H617E."""
from __future__ import annotations

import json
from pathlib import Path

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_EFFECT,
    ATTR_RGB_COLOR,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import GoveeH617ECoordinator


def _load_scenes() -> dict[str, str]:
    path = Path(__file__).parent / "scenes.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    scenes = {}
    for scene in data.get("scenes", []):
        if scene.get("name") and scene.get("packet"):
            scenes[scene["name"]] = scene["packet"]
    return scenes


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator: GoveeH617ECoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    entities = [GoveeH617ELight(coordinator, entry.entry_id, _load_scenes())]
    
    # Add segment entities if experimentalSegments is enabled
    if coordinator.experimental_segments:
        for segment_index in range(15):
            entities.append(GoveeH617ESegmentLight(coordinator, entry.entry_id, segment_index))
    
    async_add_entities(entities)


class GoveeH617ELight(CoordinatorEntity[GoveeH617ECoordinator], LightEntity):
    _attr_has_entity_name = True
    _attr_name = None
    _attr_supported_color_modes = {ColorMode.RGB}
    _attr_supported_features = LightEntityFeature.EFFECT

    def __init__(self, coordinator: GoveeH617ECoordinator, entry_id: str, scenes: dict[str, str]) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_light"
        self._scenes = scenes

    @property
    def available(self) -> bool:
        return self.coordinator.state.available

    @property
    def is_on(self) -> bool:
        return self.coordinator.state.is_on

    @property
    def brightness(self) -> int:
        return self.coordinator.state.brightness

    @property
    def rgb_color(self) -> tuple[int, int, int]:
        return self.coordinator.state.rgb_color

    @property
    def effect(self) -> str | None:
        return self.coordinator.state.effect

    @property
    def effect_list(self) -> list[str]:
        return list(self._scenes.keys())

    async def async_turn_on(self, **kwargs) -> None:
        if not self.is_on:
            await self.coordinator.async_set_power(True)
        if ATTR_BRIGHTNESS in kwargs:
            await self.coordinator.async_set_brightness(kwargs[ATTR_BRIGHTNESS])
        if ATTR_RGB_COLOR in kwargs:
            await self.coordinator.async_set_rgb(kwargs[ATTR_RGB_COLOR])
        if ATTR_EFFECT in kwargs:
            effect = kwargs[ATTR_EFFECT]
            packet_hex = self._scenes.get(effect)
            if packet_hex is None:
                raise ValueError(f"Unsupported effect: {effect}")
            await self.coordinator.async_set_effect(effect, bytes.fromhex(packet_hex))

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_set_power(False)


class GoveeH617ESegmentLight(CoordinatorEntity[GoveeH617ECoordinator], LightEntity):
    """Light entity for controlling individual H617E segments."""
    
    _attr_has_entity_name = True
    _attr_supported_color_modes = {ColorMode.RGB}

    def __init__(self, coordinator: GoveeH617ECoordinator, entry_id: str, segment_index: int) -> None:
        super().__init__(coordinator)
        self._segment_index = segment_index
        self._attr_unique_id = f"{entry_id}_segment_{segment_index}"
        self._attr_name = f"Segment {segment_index + 1}"

    @property
    def available(self) -> bool:
        return self.coordinator.state.available and self.coordinator.experimental_segments

    @property
    def is_on(self) -> bool:
        # Segment is on if main light is on AND segment color is not black (0,0,0)
        if not self.coordinator.state.is_on:
            return False
        color = self.coordinator.state.segment_colors.get(self._segment_index)
        return color is not None and color != (0, 0, 0)

    @property
    def brightness(self) -> int | None:
        # Segments don't have independent brightness control in the current implementation
        return None

    @property
    def rgb_color(self) -> tuple[int, int, int] | None:
        color = self.coordinator.state.segment_colors.get(self._segment_index)
        # Return None if segment is "off" (black) to show as off in UI
        if color == (0, 0, 0):
            return None
        return color

    async def async_turn_on(self, **kwargs) -> None:
        # Ensure main light is on
        if not self.coordinator.state.is_on:
            await self.coordinator.async_set_power(True)
        
        # Set segment color if provided by user
        if ATTR_RGB_COLOR in kwargs:
            color = kwargs[ATTR_RGB_COLOR]
            # Save this as the last known color
            self.coordinator.state.segment_last_colors[self._segment_index] = color
            await self.coordinator.async_set_segment_color(self._segment_index, color)
        else:
            # If no color provided, restore the last known color
            # This preserves the color when turning back on
            last_color = self.coordinator.state.segment_last_colors.get(
                self._segment_index, (255, 255, 255)
            )
            await self.coordinator.async_set_segment_color(self._segment_index, last_color)

    async def async_turn_off(self, **kwargs) -> None:
        # Save current color before turning off
        current_color = self.coordinator.state.segment_colors.get(self._segment_index)
        if current_color and current_color != (0, 0, 0):
            self.coordinator.state.segment_last_colors[self._segment_index] = current_color
        
        # Set segment to black (off) but keep main light on
        # This allows independent segment control without turning off entire light
        await self.coordinator.async_set_segment_color(self._segment_index, (0, 0, 0))

