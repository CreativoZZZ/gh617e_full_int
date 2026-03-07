from custom_components.govee_h617e.ble.protocol import (
    brightness_packet,
    experimental_segment_packet,
    parse_hex_packet,
    power_packet,
    rgb_packet,
)


def test_power_packet_has_20_bytes() -> None:
    payload = power_packet(True)
    assert len(payload) == 20
    assert payload[0] == 0x33


def test_brightness_packet_scaling() -> None:
    payload = brightness_packet(255)
    assert payload[2] == 0xFE


def test_rgb_packet_prefix() -> None:
    payload = rgb_packet(1, 2, 3)
    assert payload[1] == 0x05


def test_parse_hex_packet_length_validation() -> None:
    try:
        parse_hex_packet("AA")
        assert False
    except ValueError:
        assert True


def test_experimental_segment_packet_format() -> None:
    pkt = experimental_segment_packet(7, 1, 2, 3)
    # ensure 20 bytes, first byte constant
    assert len(pkt) == 20
    assert pkt[0] == 0x33
    # command 0x05 second byte
    assert pkt[1] == 0x05
    # payload prefix 0x15 in third byte
    assert pkt[2] == 0x15
    # static rgb command selector
    assert pkt[3] == 0x01
    # colors in subsequent bytes
    assert pkt[4] == 1
    assert pkt[5] == 2
    assert pkt[6] == 3
    # segment bitmask starts at byte 12, little-endian
    assert pkt[12] == 0x80
    assert pkt[13] == 0x00
