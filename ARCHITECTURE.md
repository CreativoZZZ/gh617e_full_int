# H617E UI Integration - System Architecture

## Entity Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│            Home Assistant Light Platform                      │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
    ┌────────────┐  ┌────────────┐  ┌──────────────────┐
    │Main Light  │  │ Segment 0  │  │ ... Segment 14   │
    │(Effects    │  │ (RGB only) │  │ (RGB only)       │
    │Brightness) │  │            │  │                  │
    └─────┬──────┘  └─────┬──────┘  └────────┬─────────┘
          │                │                  │
          └────────────────┼──────────────────┘
                           │
                ┌──────────▼───────────┐
                │  Coordinator        │
                │  (State Manager)    │
                └──────────┬──────────┘
                           │
                ┌──────────▼───────────┐
                │  BLE Client         │
                │  (Protocol Handler) │
                └──────────┬──────────┘
                           │
                ┌──────────▼───────────┐
                │  Bluetooth Device   │
                │  (H617E Hardware)   │
                └─────────────────────┘
```

## Data Flow

### Color Setting Flow
```
User Input (Dashboard/Service)
        │
        ▼
Home Assistant Light Service
        │
        ▼
GoveeH617ESegmentLight.async_turn_on()
        │
        ▼
Coordinator.async_set_segment_color()
        │
        ▼
Protocol: experimental_segment_packet()
        │
        ▼
BLE Write
        │
        ▼
H617E Device
        │
        ▼
Segment Color Updated
```

### State Synchronization
```
H617E Status Check (polling)
        │
        ▼
BLE Ping
        │
        ▼
Coordinator.state updated
        │
        ▼
All Light Entities refresh
        │
        ▼
Home Assistant UI Updated
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────┐
│                  light.py                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ async_setup_entry()                                  │  │
│  │  - Creates GoveeH617ELight (main)                    │  │
│  │  - Creates 15x GoveeH617ESegmentLight (segments)     │  │
│  │  - Only if experimental_segments=true               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
                            ├─ Returns new entities
                            │
┌─────────────────────────────────────────────────────────────┐
│                  __init__.py                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ async_setup_entry()                                  │  │
│  │  - Creates GoveeBleClient                            │  │
│  │  - Creates GoveeH617ECoordinator                      │  │
│  │  - Calls platform setup (light.py)                   │  │
│  │  - Registers services                                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
                            ├─ Configuration data
                            │
┌─────────────────────────────────────────────────────────────┐
│                  coordinator.py                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ GoveeH617ECoordinator                                │  │
│  │  - Manages H617EState                                │  │
│  │  - async_set_segment_color()                         │  │
│  │  - async_set_power()                                 │  │
│  │  - async_set_rgb()                                   │  │
│  │  - Periodic polling via _async_update_data()         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
                            ├─ Uses client for BLE
                            │
┌─────────────────────────────────────────────────────────────┐
│                  ble/client.py                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ GoveeBleClient                                       │  │
│  │  - async_write(packet: bytes)                        │  │
│  │  - async_ping()                                      │  │
│  │  - Connection management                             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
                            ├─ Sends protocol packets
                            │
┌─────────────────────────────────────────────────────────────┐
│                  ble/protocol.py                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Packet Builders                                      │  │
│  │  - power_packet()                                    │  │
│  │  - rgb_packet()                                      │  │
│  │  - experimental_segment_packet()                     │  │
│  │  - build_packet() [core]                             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
                            ├─ BLE Packets (bytes)
                            │
                        ╔═══╩═══╗
                        ║ Bleak ║
                        ╚═══╤═══╝
                            │
                            ▼
                    ┌─────────────────┐
                    │  H617E Device   │
                    │  (via Bluetooth)│
                    └─────────────────┘
```

## Features Overview

| Feature | Implemented | Status |
|---------|-------------|--------|
| **Main Light Control** | ✅ | Full |
| **RGB Color** | ✅ | Full |
| **Brightness** | ✅ | Full (Main only) |
| **Effects/Scenes** | ✅ | Full (Main only) |
| **Segment Color Control** | ✅ | Experimental |
| **15 Segment Entities** | ✅ | New |
| **Dashboard Support** | ✅ | New |
| **Automations Support** | ✅ | Full |
| **Service API** | ✅ | Full |
| **Groups Support** | ✅ | Via native HA |
| **Templates Support** | ✅ | Via native HA |

## Data Model

### H617EState
```python
@dataclass
class H617EState:
    is_on: bool
    brightness: int  # 0-254
    rgb_color: tuple[int, int, int]
    effect: str | None
    available: bool
    confirmed_effect: str | None
    segment_colors: dict[int, tuple[int, int, int]]  # Segment index -> RGB
```

### Service Schema
```
set_segment_color:
  - entry_id: str
  - segment_index: int (0-14)
  - rgb_color: [int, int, int]
```

## Configuration Flow

```
Device Pairing
    │
    ▼
Config Flow (config_flow.py)
    │
    ├─ MAC address
    ├─ Connection timeout
    ├─ Poll interval
    ├─ Optimistic mode
    ├─ Enable experimental segments ◄──── NEW
    └─ Retry count
    │
    ▼
ConfigEntry saved
    │
    ▼
async_setup_entry() called
    │
    ├─ BleClient created
    ├─ Coordinator created
    ├─ Platform setup (light)
    │   ├─ Main light entity
    │   ├─ 15 Segment entities (if experimental=true)
    │   └─ Entities registered
    └─ Services registered
```

## Performance Characteristics

### BLE Operations
- **Ping**: ~50-100ms
- **Write Color**: ~100-200ms
- **Set Segment**: ~100-200ms per segment
- **Batch Update**: ~100-200ms for multiple segments

### Polling Interval
- Default: 30 seconds
- Configurable: 5-300 seconds
- Lower = More responsive, Higher = Less BLE traffic

### Entity Updates
- Main light: Updates on write + polling
- Segments: Updates on write + polling
- Optimistic mode: Immediate local update

---

**Last Updated**: 2024
**Version**: 0.1.0
