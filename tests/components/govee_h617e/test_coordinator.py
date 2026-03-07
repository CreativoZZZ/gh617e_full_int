from datetime import timedelta

import pytest

from custom_components.govee_h617e.const import OPTIMISTIC_PARTIAL
from custom_components.govee_h617e.coordinator import GoveeH617ECoordinator


class FakeBleClient:
    def __init__(self) -> None:
        self.available = True
        self.payloads: list[bytes] = []
        self.fail = False

    async def async_write(self, payload: bytes) -> None:
        if self.fail:
            raise RuntimeError("write failed")
        self.payloads.append(payload)

    async def async_ping(self) -> None:
        if self.fail:
            raise RuntimeError("unreachable")


@pytest.mark.asyncio
async def test_set_segment_disabled_raises(hass) -> None:
    coordinator = GoveeH617ECoordinator(
        hass,
        FakeBleClient(),
        timedelta(seconds=30),
        optimistic_mode=OPTIMISTIC_PARTIAL,
        experimental_segments=False,
    )
    with pytest.raises(ValueError):
        await coordinator.async_set_segment_color(1, (255, 0, 0))


@pytest.mark.asyncio
async def test_reconnect_error_propagates(hass) -> None:
    client = FakeBleClient()
    client.fail = True
    coordinator = GoveeH617ECoordinator(hass, client, timedelta(seconds=30), OPTIMISTIC_PARTIAL, False)
    with pytest.raises(Exception):
        await coordinator._async_update_data()

@pytest.mark.asyncio
async def test_set_segment_color_sends_packet_and_stores(hass) -> None:
    client = FakeBleClient()
    coordinator = GoveeH617ECoordinator(hass, client, timedelta(seconds=30), OPTIMISTIC_PARTIAL, True)
    await coordinator.async_set_segment_color(3, (10, 20, 30))
    # packet should include correct payload prefix and index
    assert len(client.payloads) == 1
    # the second byte (command) should be 0x05, third byte payload[2] should equal 0x15
    assert client.payloads[0][1] == 0x05
    assert client.payloads[0][2] == 0x15
    # static rgb selector in payload[3], segment mask starts at payload[12]
    assert client.payloads[0][3] == 0x01
    assert client.payloads[0][12] == 0x08
    assert coordinator.state.segment_colors[3] == (10, 20, 30)
    assert coordinator.state.segment_last_colors[3] == (10, 20, 30)

@pytest.mark.asyncio
async def test_power_restores_segment_colors(hass) -> None:
    client = FakeBleClient()
    coordinator = GoveeH617ECoordinator(hass, client, timedelta(seconds=30), OPTIMISTIC_PARTIAL, True)
    # simulate segment command before power off
    await coordinator.async_set_segment_color(1, (5, 6, 7))
    # power off then on
    await coordinator.async_set_power(False)
    await coordinator.async_set_power(True)
    # after powering on, one additional packet for segment restoration should be sent
    # there will be one packet from initial set, one for power off, one for power on
    # but power packets also use payloads so check segment-specific ones
    segment_packets = [p for p in client.payloads if p[1] == 0x05 and p[2] == 0x15]
    # initial set and restore = 2
    assert len(segment_packets) >= 2
    # state should reflect restored color
    assert coordinator.state.segment_colors[1] == (5, 6, 7)


@pytest.mark.asyncio
async def test_set_segment_color_out_of_range_raises(hass) -> None:
    client = FakeBleClient()
    coordinator = GoveeH617ECoordinator(hass, client, timedelta(seconds=30), OPTIMISTIC_PARTIAL, True, segment_count=3)
    with pytest.raises(ValueError):
        await coordinator.async_set_segment_color(3, (10, 20, 30))
