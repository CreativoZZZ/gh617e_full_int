# UI Integration für H617E Segment-Steuerung

Dieses Dokument gibt einen Überblick über die neue Segment-Steuerungs-UI-Integration für die Govee H617E RGBIC Light Strip.

## 🎯 Übersicht

Die H617E hat 15 Segmente, die jetzt einzeln über die Home Assistant UI gesteuert werden können. Jedes Segment kann eine eigene Farbe haben.

## 📋 Neue Dateien

### 1. **light.py** (Erweitert)
- Neue Klasse: `GoveeH617ESegmentLight`
- Erstellt automatisch 15 Light-Entitäten (eine pro Segment)
- Entitäten werden nur erstellt, wenn "experimental_segments" aktiviert ist
- Entity IDs: `light.govee_h617e_segment_0` bis `light.govee_h617e_segment_14`

### 2. **SEGMENT_CONTROL_GUIDE.md**
Vollständiges Benutzerhandbuch mit:
- Installation und Aktivierung
- Verwendungsbeispiele
- Automationen und Scripts
- Fehlerbehebung
- Technische Details

### 3. **SEGMENT_LAYOUT.md**
Referenzdokumentation mit:
- Segment-Nummern und Indizes
- Entity ID Mappings
- Häufige Verwendungsmuster (Gruppen)
- Farb-Referenztabelle

### 4. **dashboard_template.yaml**
Ein einfaches Dashboard-Template mit:
- Hauptlicht-Steuerung
- 15 Segment-Light-Karten
- Übersichtliche Anordnung in Gruppen

### 5. **lovelace_advanced_config.yaml**
Ein fortgeschrittenes Dashboard mit:
- Bessere Visualisierung
- Button-Card Integration
- Horizontal-Stack Layout
- Quick Actions

### 6. **EXAMPLES_AUTOMATIONS.yaml**
Praktische Beispiele für:
- Rainbow-Effekt über Automationen
- Movie-Mode
- Police/Emergency Effekt
- Nützliche Scripts für verschiedene Szenen

## 🚀 Quick Start

### 1. Experimentelle Segmente aktivieren
```
Home Assistant → Settings → Devices & Services → Govee H617E
→ Klick auf Zahnrad (Options) → Aktiviere "Enable experimental segment features"
```

### 2. Dashboard erstellen (Optional)
Kopieren Sie den Inhalt aus `dashboard_template.yaml` oder `lovelace_advanced_config.yaml` in ein neues Home Assistant Dashboard.

### 3. Segments über UI steuern
- Öffnen Sie das Dashboard
- Klicken Sie auf ein Segment
- Wählen Sie eine Farbe
- Die Farbe wird sofort angewendet

## 💡 Wichtigste Features

| Feature | Beschreibung |
|---------|-------------|
| **15 Segment-Entitäten** | Jedes Segment als eigenständige Light-Entität |
| **Individuelle Farben** | Jedes Segment kann seine eigene Farbe haben |
| **Einfache UI** | Drag-and-Drop in Home Assistant Dashboards |
| **Automationen** | Vollständige Unterstützung für Home Assistant Automationen |
| **Groups** | Segmente können in Gruppen zusammengefasst werden |
| **Services** | Volle API für Custom Integrations |

## 📝 Verwendungsbeispiele

### Einfache Farbsetzung
```yaml
service: light.turn_on
data:
  entity_id: light.govee_h617e_segment_0
  rgb_color: [255, 0, 0]  # Red
```

### Rainbow-Effekt
Siehe `EXAMPLES_AUTOMATIONS.yaml` für ein komplettes Beispiel

### Custom Script
```yaml
service: script.set_all_segments_color
data:
  rgb_color: [255, 255, 0]  # Yellow
```

## 🔧 Technische Details

### Entity Struktur
```
light.govee_h617e                    # Hauptlicht
├── light.govee_h617e_segment_0      # Segment 1
├── light.govee_h617e_segment_1      # Segment 2
├── light.govee_h617e_segment_2      # Segment 3
├── ...
└── light.govee_h617e_segment_14     # Segment 15
```

### Supported Features
- ✅ RGB Color Control
- ✅ On/Off Toggle
- ✅ On/Off Status
- ❌ Brightness (pro Segment) - nur für Hauptlicht
- ❌ Effects (pro Segment) - nur für Hauptlicht
- ❌ Transitions

### Abhängigkeiten
- Home Assistant Core
- Govee H617E Integration (experimental_segments flag)
- BLE Device (H617E)

## 📚 Dokumentation

- **[SEGMENT_CONTROL_GUIDE.md](SEGMENT_CONTROL_GUIDE.md)** - Ausführliches Benutzerhandbuch
- **[SEGMENT_LAYOUT.md](SEGMENT_LAYOUT.md)** - Segment-Nummern und Entity-Referenz
- **[EXAMPLES_AUTOMATIONS.yaml](EXAMPLES_AUTOMATIONS.yaml)** - Praktische Beispiele
- **[dashboard_template.yaml](dashboard_template.yaml)** - Basic Dashboard
- **[lovelace_advanced_config.yaml](lovelace_advanced_config.yaml)** - Advanced Dashboard

## 🐛 Troubleshooting

### Segmente tauchen nicht auf
1. Überprüfen Sie, dass "Enable experimental segment features" aktiviert ist
2. Starten Sie Home Assistant neu
3. Überprüfen Sie die Logs in Settings → System → Logs

### Segment-Farben ändern sich nicht
1. Überprüfen Sie die BLE-Verbindung
2. Aktivieren Sie "Optimistic Mode" in den Optionen
3. Versuchen Sie, das Hauptlicht auszuschalten und wieder einzuschalten

### Entity IDs passen nicht
Die Entity IDs hängen von Ihrem Config Entry Namen ab. Überprüfen Sie:
- Settings → Devices & Services
- Suchen Sie nach "Govee H617E"
- Die korrekten Entity IDs werden dort angezeigt

## 🤝 Support

Für Fragen oder Probleme:
1. Überprüfen Sie [SEGMENT_CONTROL_GUIDE.md](SEGMENT_CONTROL_GUIDE.md)
2. Lesen Sie die Home Assistant Dokumentation
3. Erstellen Sie ein Issue im GitHub Repository

## 📝 Versionsverlauf

- **v0.1.0** - Initial UI Integration
  - 15 Segment Light Entities
  - Dashboard Templates
  - Examples und Documentation

---

**Kontakt**: Siehe Repository für Kontaktinformationen
**Lizenz**: Siehe LICENSE
