# Segment Control UI Integration Guide

## Overview

Die H617E RGBIC Light Strip hat 15 Segmente, die einzeln angesteuert werden können. Nach dem Aktivieren der experimentellen Segment-Funktionen werden automatisch 15 zusätzliche Light-Entitäten in Home Assistant erstellt.

## Features

- **Individuelle Segmentsteuerung**: Jedes der 15 Segmente kann eine eigene Farbe haben
- **Einfache UI**: Jedes Segment erscheint als Light-Entität in Home Assistant
- **Automatische Entity-Kreierung**: Keine manuelle Konfiguration notwendig
- **Automation-Unterstützung**: Alle Standard-Light-Automationen funktionieren

## Installation

1. **Experimentelle Segmente aktivieren**:
   - Settings → Devices & Services → Govee H617E
   - Klick auf "Optionen"
   - Aktivieren Sie "Enable experimental segment features"

2. **Dashboard konfigurieren** (optional):
   - Öffnen Sie Settings → Dashboards
   - Erstellen Sie ein neues Dashboard
   - Nutzen Sie die Vorlage aus `dashboard_template.yaml`
   - Nutzen Sie die Entity IDs: `light.govee_h617e_segment_0` bis `light.govee_h617e_segment_14`

## UI-Entitäten

Nach dem Aktivieren erscheinen folgende Entitäten in Home Assistant:

```
light.govee_h617e                # Hauptlicht (mit Effekten und Helligkeit)
light.govee_h617e_segment_0      # Segment 1
light.govee_h617e_segment_1      # Segment 2
light.govee_h617e_segment_2      # Segment 3
...
light.govee_h617e_segment_14     # Segment 15
```

## Verwendungsbeispiele

### Beispiel 1: Segment über UI ansteuern

1. Öffnen Sie das Dashboard
2. Klicken Sie auf ein Segment (z.B. "Segment 1")
3. Wählen Sie eine Farbe
4. Die Farbe wird sofort auf das Segment angewendet

### Beispiel 2: Automation für Rainbow-Effekt

```yaml
automation:
  - alias: "Rainbow on Segment"
    trigger:
      platform: time
      at: "18:00:00"
    action:
      - service: light.turn_on
        target:
          entity_id:
            - light.govee_h617e_segment_0
            - light.govee_h617e_segment_2
            - light.govee_h617e_segment_4
        data:
          rgb_color: [255, 0, 0]  # Red
      - service: light.turn_on
        target:
          entity_id:
            - light.govee_h617e_segment_1
            - light.govee_h617e_segment_3
        data:
          rgb_color: [0, 255, 0]  # Green
```

### Beispiel 3: Script für Farbverlauf

```yaml
script:
  set_segment_gradient:
    description: "Set a color gradient across segments"
    sequence:
      - service: light.turn_on
        target:
          entity_id: light.govee_h617e_segment_0
        data:
          rgb_color: [255, 0, 0]
      - service: light.turn_on
        target:
          entity_id: light.govee_h617e_segment_1
        data:
          rgb_color: [255, 127, 0]
      - service: light.turn_on
        target:
          entity_id: light.govee_h617e_segment_2
        data:
          rgb_color: [255, 255, 0]
      # ... continue for all segments
```

## Technische Details

### Entity-Attribute

Jede Segment-Entity hat folgende Attribute:
- `rgb_color`: RGB-Farbe des Segments [R, G, B]
- `is_on`: Aktiv/Inaktiv (folgt dem Hauptlicht)
- `available`: Verfügbarkeit basierend auf BLE-Verbindung

### API (Services)

Es gibt zwei Möglichkeiten, Segmente zu steuern:

**Methode 1: Light Service (empfohlen)**
```yaml
service: light.turn_on
data:
  entity_id: light.govee_h617e_segment_0
  rgb_color: [255, 0, 0]  # Red
```

**Methode 2: Raw Service (fortgeschritten)**
```yaml
service: govee_h617e.set_segment_color
data:
  entry_id: "YOUR_ENTRY_ID"
  segment_index: 0
  rgb_color: [255, 0, 0]
```

## Hinweise

- Das Hauptlicht (light.govee_h617e) muss an sein, damit Segmente aktiv sind
- Wenn das Hauptlicht ausgeschaltet wird, werden auch alle Segmente ausgeschaltet
- Die Helligkeit wird auf dem Hauptlicht gesteuert, nicht auf einzelnen Segmenten
- Effekte können nur auf dem Hauptlicht angewendet werden, nicht auf einzelnen Segmenten

## Fehlerbehebung

**Segmente tauchen nicht auf:**
- Überprüfen Sie, ob "Enable experimental segment features" in den Optionen aktiviert ist
- Starten Sie Home Assistant neu
- Überprüfen Sie die Logs: `Settings → System → Logs`

**Segmente werden nicht angesteuert:**
- Überprüfen Sie die BLE-Verbindung
- Aktivieren Sie "Optimistic Mode" in den Optionen
- Überprüfen Sie, dass das Hauptlicht eingeschaltet ist

**Entity IDs stimmen nicht überein:**
- Die Entity IDs hängen von Ihrem Konfigurationsnamen ab
- Navigieren Sie zu `Settings → Devices & Services` und suchen Sie nach "Govee H617E"
- Die korrekten Entity IDs werden dort angezeigt
