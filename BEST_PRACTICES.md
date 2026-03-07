# Best Practices & Tips für H617E Segment-Steuerung

## 🎨 Design-Tipps

### 1. Farb-Harmonie
Verwenden Sie complementary Farben für bessere visuelle Effekte:

```
Complementary Pairs:
- Rot & Cyan: [255,0,0] & [0,255,255]
- Blau & Orange: [0,0,255] & [255,165,0]
- Grün & Magenta: [0,255,0] & [255,0,255]
```

### 2. Fraktale Muster
Nutzen Sie mathematische Muster:

```yaml
# Fibonacci Sequence
segment_0: Red
segment_1: Red
segment_2: Orange
segment_3: Orange
segment_4: Yellow
segment_5: Green
segment_6: Green
segment_7: Blue
...
```

### 3. Ambient Lighting
Nutzen Sie gedimmte Farben für entspannende Atmosphäre:

```yaml
# Warm Ambient Light
segments: [255, 100, 50]  # Soft Orange

# Cool Ambient Light
segments: [100, 150, 255]  # Soft Blue
```

## ⚡ Performance-Tipps

### 1. Batch-Updates
Statt einzelne Segmente zu aktualisieren, verwenden Sie Gruppen:

```yaml
# ❌ Langsam (15 Requests)
- service: light.turn_on
  target:
    entity_id: light.govee_h617e_segment_0
  data:
    rgb_color: [255, 0, 0]
- service: light.turn_on
  target:
    entity_id: light.govee_h617e_segment_1
  data:
    rgb_color: [255, 0, 0]
# ... repeat 13 times

# ✅ Schneller (1 Request)
- service: light.turn_on
  target:
    entity_id: group.h617e_all_segments
  data:
    rgb_color: [255, 0, 0]
```

### 2. Delay Optimization
Nutzen Sie parallelisierte Updates:

```yaml
# ❌ Langsam (mit Delays)
- service: light.turn_on
  target:
    entity_id: light.govee_h617e_segment_0
  data:
    rgb_color: [255, 0, 0]
- delay: "00:00:01"
- service: light.turn_on
  target:
    entity_id: light.govee_h617e_segment_1
  data:
    rgb_color: [255, 0, 0]

# ✅ Schneller (parallel)
- service: light.turn_on
  target:
    entity_id:
      - light.govee_h617e_segment_0
      - light.govee_h617e_segment_1
  data:
    rgb_color: [255, 0, 0]
```

### 3. BLE Connection
Tipps zur stabilen Verbindung:

- Behalten Sie das Device in Bluetooth-Reichweite
- Verwenden Sie "Optimistic Mode" für schnellere Updates
- Setzen Sie angemessene Poll-Intervals
- Verwenden Sie "Retry Count" > 1 für Zuverlässigkeit

## 🎬 Szenen-Beispiele

### Entertainment Mode
```yaml
- alias: "Movie Start"
  trigger:
    platform: state
    entity_id: media_player.tv
    to: "playing"
  action:
    - service: light.turn_on
      target:
        entity_id: light.govee_h617e
      data:
        brightness: 50
    - service: light.turn_on
      target:
        entity_id: group.h617e_all_segments
      data:
        rgb_color: [20, 20, 40]  # Dark blue
```

### Party Mode
```yaml
- alias: "Party Mode"
  trigger:
    platform: time
    at: "22:00:00"
  action:
    - repeat:
      count: 10
      sequence:
        - service: script.checkerboard_pattern
          data:
            color1: [255, 0, 0]
            color2: [0, 0, 255]
        - delay: "00:00:02"
        - service: script.checkerboard_pattern
          data:
            color1: [0, 255, 0]
            color2: [255, 255, 0]
        - delay: "00:00:02"
```

### Workspace Mode
```yaml
- alias: "Work Mode"
  trigger:
    platform: time
    at: "09:00:00"
  condition:
    condition: state
    entity_id: input_boolean.work_day
    state: "on"
  action:
    - service: light.turn_on
      target:
        entity_id: light.govee_h617e
      data:
        brightness: 200
    - service: light.turn_on
      target:
        entity_id: group.h617e_all_segments
      data:
        rgb_color: [200, 200, 255]  # Cool White
```

## 🔧 Fortgeschrittene Konfiguration

### Template Lights (für komplexere Szenen)
```yaml
light:
  - platform: template
    lights:
      h617e_gradient_red_blue:
        friendly_name: "H617E Red to Blue Gradient"
        turn_on:
          service: script.gradient_red_to_blue
        turn_off:
          service: light.turn_off
          target:
            entity_id: light.govee_h617e
```

### Automations mit Bedingungen
```yaml
- id: conditional_segment_control
  alias: "Smart Segment Control"
  trigger:
    platform: state
    entity_id: sensor.color_temperature
  action:
    - choose:
        - conditions:
            - condition: numeric_state
              entity_id: sensor.color_temperature
              below: 3000
          sequence:
            - service: light.turn_on
              target:
                entity_id: group.h617e_all_segments
              data:
                rgb_color: [255, 100, 0]  # Warm
        - conditions:
            - condition: numeric_state
              entity_id: sensor.color_temperature
              above: 5000
          sequence:
            - service: light.turn_on
              target:
                entity_id: group.h617e_all_segments
              data:
                rgb_color: [100, 150, 255]  # Cool
```

## 📊 Monitoring & Diagnostics

### Entity State Überwachung
```yaml
- id: monitor_segment_status
  alias: "Monitor Segment Status"
  trigger:
    platform: time_pattern
    minutes: "/5"
  action:
    - service: logbook.log
      data:
        name: "Segment States"
        message: |
          Segment 0: {{ states('light.govee_h617e_segment_0') }}
          Segment 1: {{ states('light.govee_h617e_segment_1') }}
          ...
```

### BLE Signal Strength
```yaml
automation:
  - id: weak_signal_alert
    alias: "Weak BLE Signal Alert"
    trigger:
      platform: state
      entity_id: light.govee_h617e
      to: "unavailable"
    action:
      - service: notify.notify
        data:
          message: "H617E BLE connection lost!"
```

## 🎯 Nützliche Templates

### Calculate RGB from HSL
```python
# In Home Assistant Node-RED oder Custom Component
def hsl_to_rgb(h, s, l):
    import colorsys
    r, g, b = colorsys.hls_to_rgb(h/360, l/100, s/100)
    return int(r*255), int(g*255), int(b*255)
```

### Create Gradient
```python
def create_gradient(color1, color2, steps=15):
    """Create gradient between two RGB colors"""
    result = []
    for i in range(steps):
        t = i / (steps - 1)
        r = int(color1[0] * (1-t) + color2[0] * t)
        g = int(color1[1] * (1-t) + color2[1] * t)
        b = int(color1[2] * (1-t) + color2[2] * t)
        result.append([r, g, b])
    return result

# Usage:
gradient = create_gradient([255, 0, 0], [0, 0, 255])  # Red to Blue
```

## 🆘 Häufige Probleme

### Problem: Segmente flackern
**Lösung**: 
- Erhöhen Sie den Poll-Interval
- Reduzieren Sie Automationen die zu oft triggern
- Nutzen Sie Optimistic Mode

### Problem: Timeout Fehler
**Lösung**:
- Erhöhen Sie Connect Timeout in Options
- Überprüfen Sie BLE-Reichweite
- Reduzieren Sie Retry Count

### Problem: Inkonsistente Farbwerte
**Lösung**:
- Setzen Sie explizite RGB-Werte statt Hex-Werte
- Validieren Sie die RGB-Werte (0-255)
- Verwenden Sie State Templates für Konsistenz

## 📚 Weitere Ressourcen

- [Home Assistant Automation Docs](https://www.home-assistant.io/docs/automation/)
- [Home Assistant Scripts Docs](https://www.home-assistant.io/docs/scripts/)
- [Light Integration Docs](https://www.home-assistant.io/integrations/light/)
- [Govee Integration Repo](https://github.com/example/govee_h617e)

---

**Hinweis**: Diese Tipps sind basierend auf Best Practices für Home Assistant Automationen. 
Passen Sie sie an Ihre spezifische Umgebung an.
