"""Data coordinator and state model for Govee H617E."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .ble.client import GoveeBleClient
from .ble.protocol import brightness_packet, experimental_segment_packet, power_packet, rgb_packet
from .const import OPTIMISTIC_PARTIAL

_LOGGER = logging.getLogger(__name__)
DEFAULT_SEGMENT_COUNT = 15


@dataclass
class H617EState:
    """State split between confirmed and optimistic values."""

    is_on: bool = False
    brightness: int = 255
    rgb_color: tuple[int, int, int] = (255, 255, 255)
    effect: str | None = None
    available: bool = False
    confirmed_effect: str | None = None
    segment_colors: dict[int, tuple[int, int, int]] = field(default_factory=dict)
    # Store the last non-black color for each segment (for restoring when turning on)
    segment_last_colors: dict[int, tuple[int, int, int]] = field(default_factory=dict)


class GoveeH617ECoordinator(DataUpdateCoordinator[H617EState]):
    """Coordinator owning BLE access and runtime state."""

    def __init__(
        self,
        hass: HomeAssistant,
        ble_client: GoveeBleClient,
        polling_interval: timedelta,
        optimistic_mode: str,
        experimental_segments: bool,
        segment_count: int = DEFAULT_SEGMENT_COUNT,
    ) -> None:
        self.ble_client = ble_client
        self.optimistic_mode = optimistic_mode
        self.experimental_segments = experimental_segments
        self.segment_count = max(1, min(56, segment_count))
        self.state = H617EState()

        super().__init__(
            hass,
            _LOGGER,
            name="govee_h617e",
            update_interval=polling_interval,
        )

    def _scale_rgb_for_brightness(self, rgb: tuple[int, int, int]) -> tuple[int, int, int]:
        """Apply global brightness to an RGB color before sending to device."""
        factor = max(0.0, min(1.0, self.state.brightness / 255))
        return (
            max(0, min(255, round(rgb[0] * factor))),
            max(0, min(255, round(rgb[1] * factor))),
            max(0, min(255, round(rgb[2] * factor))),
        )

    async def _async_update_data(self) -> H617EState:
        try:
            await self.ble_client.async_ping()
            self.state.available = True
            return self.state
        except Exception as err:
            self.state.available = False
            raise UpdateFailed(str(err)) from err

    async def async_set_power(self, on: bool) -> None:
        # Write the power packet first
        await self.ble_client.async_write(power_packet(on))
        self.state.is_on = on

        # Do not auto-restore segment colors on power-on.
        # Segment frames can interfere with global brightness on some firmware
        # variants; explicit segment writes remain available per entity/service.
        if not on:
            self.state.segment_colors.clear()

        # Force full brightness on every power-on so startup is not dim.
        if on:
            self.state.brightness = 255
            await self.ble_client.async_write(brightness_packet(self.state.brightness))

        await self.async_request_refresh()

    async def async_set_brightness(self, brightness: int) -> None:
        self.state.brightness = max(0, min(255, brightness))

        # Native brightness command (kept as best-effort).
        await self.ble_client.async_write(brightness_packet(self.state.brightness))

        # Fallback: many RGBIC firmware variants ignore global brightness in
        # segment mode, so re-send scaled colors explicitly.
        if self.state.is_on:
            await self.ble_client.async_write(rgb_packet(*self._scale_rgb_for_brightness(self.state.rgb_color)))
            if self.experimental_segments:
                for idx, color in self.state.segment_colors.items():
                    await self.ble_client.async_write(
                        experimental_segment_packet(idx, *self._scale_rgb_for_brightness(color))
                    )
        await self.async_request_refresh()

    async def async_set_rgb(self, rgb: tuple[int, int, int]) -> None:
        await self.ble_client.async_write(rgb_packet(*self._scale_rgb_for_brightness(rgb)))
        self.state.rgb_color = rgb
        self.state.effect = None
        await self.async_request_refresh()

    async def async_set_effect(self, name: str, packet: bytes) -> None:
        await self.ble_client.async_write(packet)
        if self.optimistic_mode == OPTIMISTIC_PARTIAL:
            self.state.effect = name
        self.state.confirmed_effect = name
        await self.async_request_refresh()

    async def async_set_segment_color(self, index: int, rgb: tuple[int, int, int]) -> None:
        if not self.experimental_segments:
            raise ValueError("Segment control disabled. Enable experimental segment features in options.")
        if index < 0 or index >= self.segment_count:
            raise ValueError(f"segment index {index} out of range (0..{self.segment_count - 1})")

        # keep track of last non-black color for restore after power cycle
        if rgb != (0, 0, 0):
            self.state.segment_last_colors[index] = rgb

        # Experimental: this packet format is not fully validated for all H617E firmware versions.
        await self.ble_client.async_write(
            experimental_segment_packet(index, *self._scale_rgb_for_brightness(rgb))
        )
        # Some RGBIC firmware revisions change effective brightness after a
        # segment packet; immediately re-apply configured brightness.
        if self.state.is_on:
            await self.ble_client.async_write(brightness_packet(self.state.brightness))
        self.state.segment_colors[index] = rgb
        await self.async_request_refresh()
