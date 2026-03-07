# Häufig gestelle Fragen (FAQ) - H617E Segment Control

## 🎨 Funktionalität & Features

### F: Wie viele Segmente hat die H617E?
**A:** Die H617E hat **15 Segmente** (Index 0-14 oder Display 1-15).

### F: Kann ich die Helligkeit pro Segment steuern?
**A:** Nein, die Helligkeit wird nur für das Hauptlicht `light.govee_h617e` gesteuert. Die Helligkeit eines Segments folgt der Haupthelligkeit. Wenn Sie die Helligkeit auf 50% setzen, werden alle Segmente zu 50% ihrer aktuellen Farbintensität angezeigt.

Das ist eine Hardware-Limitation des H617E-Geräts.

### F: Kann ich Effekte auf einzelnen Segmenten anwenden?
**A:** Nein, Effekte können nur auf dem Hauptlicht gesteuert werden. Segmente unterstützen nur RGB-Farben.

Wenn Sie komplexe Effekte für Segmente möchten, müssen Sie Automationen mit Delays erstellen.

### F: Welcher Modus ist besser - Optimistic oder Normal?
**A:** Das hängt ab:
- **Optimistic Mode**: Schnellere UI-Reaktion, kann aber inkonsistent sein
- **Normal Mode**: Zuverlässiger, aber langsamer (wartet auf Device)

**Empfehlung**: Nutzen Sie Optimistic Mode für besseres UX, wenn Ihre BLE-Verbindung stabil ist.

### F: Kann ich mehrere Segmente gleichzeitig setzen?
**A:** Ja, über Home Assistant Services:
```yaml
service: light.turn_on
target:
  entity_id:
    - light.govee_h617e_segment_0
    - light.govee_h617e_segment_1
    - light.govee_h617e_segment_2
data:
  rgb_color: [255, 0, 0]
```

Dies ist schneller als einzelne Updates.

---

## 🚀 Installation & Setup

### F: Wie aktiviere ich experimentelle Segmente?
**A:** 
1. Öffnen Sie Settings → Devices & Services
2. Suchen Sie "Govee H617E BLE"
3. Klicken Sie auf das Gerät
4. Klicken Sie auf das Zahnrad-Symbol (⚙️) "Options"
5. Aktivieren Sie "Enable experimental segment features"
6. Speichern Sie die Einstellungen

### F: Warum werden die Segmente nicht angezeigt?
**A:** Die Segmente werden nur erstellt, wenn:
1. ✅ "Enable experimental segment features" aktiviert ist
2. ✅ Home Assistant neugestartet wurde
3. ✅ Das Gerät verfügbar ist (BLE-Verbindung OK)

Wenn es nicht funktioniert:
- Überprüfen Sie die Logs: Settings → System → Logs
- Suchen Sie nach "govee_h617e"
- Überprüfen Sie die Fehlermeldungen

### F: Welche Dashboard-Templates sollte ich verwenden?
**A:** Es gibt zwei:
- **dashboard_template.yaml**: Einfach und übersichtlich
- **lovelace_advanced_config.yaml**: Mehr Features und bessere Visuals

Wählen Sie basierend auf Ihren Anforderungen.

### F: Muss ich das Dashboard von Hand erstellen?
**A:** Nein, aber es ist optional. Sie können auch:
1. Entities zum Standarddashboard hinzufügen
2. Ein leeres Dashboard erstellen und die YAML-Template-Vorlage kopieren
3. Die Entitäten via Home Assistant UI hinzufügen

---

## 🔧 Fehlerbehebung

### F: Segment-Farben werden nicht angewendet
**A:** Der wahrscheinlichste Grund ist die BLE-Verbindung:

1. **Device-Reichweite überprüfen**
   - Die H617E sollte in Bluetooth-Reichweite sein
   - Überprüfen Sie "nearby_devices" in integrations

2. **Optimistic Mode aktivieren**
   - Settings → Devices & Services → Govee H617E → Options
   - Aktivieren Sie "Optimistic Mode"
   - Dies wird Timeouts reduzieren

3. **Hauptlicht überprüfen**
   - Das Hauptlicht muss eingeschaltet sein
   - Versuchen Sie: `light.turn_on` für `light.govee_h617e`

4. **Retry Count erhöhen**
   - Settings → Options → Retry Count (2-3 versuchen)

5. **Logs überprüfen**
   - Settings → System → Logs
   - Suchen Sie nach "govee_h617e"
   - Kopieren Sie die Fehlermeldung

### F: "light.govee_h617e_segment_0 is unavailable"
**A:** Das deutet auf ein Verbindungsproblem hin:

```
Mögliche Ursachen:
1. BLE-Verbindung unterbrochen
2. Device zu weit entfernt
3. Configuration Issue
4. Home Assistant Neustart erforderlich
```

Lösungen:
```yaml
# 1. Gerät neustarten
- service: homeassistant.restart

# 2. BLE-Einstellungen überprüfen
# Settings → System → About → Check Bluetooth

# 3. Manual reconnect via service
- service: govee_h617e.reconnect
  data:
    entry_id: "YOUR_ENTRY_ID"
```

### F: Warum ist die Verbindung so langsam?
**A:** Dies könnte mehrere Ursachen haben:

1. **Poll Interval zu niedrig**
   - Standard: 30 Sekunden ist OK
   - Nicht unter 5 Sekunden setzen

2. **BLE-Interferenz**
   - 2.4GHz WiFi kann Bluetooth stören
   - TV, Mikrowelle, etc.
   - Bewegen Sie das Device näher

3. **Zu viele Automationen**
   - Reduzieren Sie die Frequenz von Updates
   - Nutzen Sie Branching-Logik

4. **Hardware-Probleme**
   - Alte Bluetooth-Dongle
   - Überhitztes Device
   - Akku schwach (falls kabelloses Für)

### F: Fehler "rgb_color must contain exactly 3 values"
**A:** Das bedeutet, dass die RGB-Werte nicht im richtigen Format sind:

```yaml
# ❌ Falsch
rgb_color: [255, 0]  # Nur 2 Werte

# ✅ Richtig
rgb_color: [255, 0, 0]  # Genau 3 Werte [R, G, B]
```

RGB-Werte müssen im Bereich 0-255 sein.

---

## 📝 Konfiguration & Optionen

### F: Welche Options sind empfohlen?
**A:** 
```
👍 Empfohlen für Anfänger:
- Connect Timeout: 5 Sekunden
- Optimistic Mode: ON
- Poll Interval: 30 Sekunden
- Retry Count: 2
- Experimental Segments: ON

🔧 Erweitert:
- Connect Timeout: 3 Sekunden
- Optimistic Mode: OFF (für Zuverlässigkeit)
- Poll Interval: 10 Sekunden
- Retry Count: 3
```

### F: Was ist der Unterschied zwischen Entry IDs?
**A:** Von der Entry ID müssen Sie keine Sorge machen - sie wird automatisch generiert.

Falls Sie die Entry ID brauchen:
1. Settings → Devices & Services → Govee H617E
2. Klicken Sie auf die Geräte URL
3. Die Nummer in der URL ist die Entry ID

### F: Kann ich mehrere H617E-Geräte verbinden?
**A:** Ja! Sie müssen:
1. Jedes Gerät separat einrichten
2. Unterschiedliche MAC-Adressen verwenden
3. Jedes bekommt eigene Entitäten

Beispiel-Entities:
```
Gerät 1: light.govee_h617e_light_1
Gerät 2: light.govee_h617e_light_2
etc.
```

---

## 🎯 Automationen & Scripts

### F: Wie erstelle ich einen Rainbow-Effekt?
**A:** Siehe `EXAMPLES_AUTOMATIONS.yaml` für vollständige Beispiele.

Kurzes Beispiel:
```yaml
script:
  rainbow_effect:
    sequence:
      - service: light.turn_on
        target:
          entity_id: light.govee_h617e_segment_0
        data:
          rgb_color: [255, 0, 0]  # Red
      - service: light.turn_on
        target:
          entity_id: light.govee_h617e_segment_1
        data:
          rgb_color: [255, 127, 0]  # Orange
      # ... repeat for all segments
```

### F: Wie setze ich alle Segmente auf die gleiche Farbe?
**A:** Nutzen Sie eine Group:

```yaml
# groups.yaml
light_h617e_all_segments:
  entities:
    - light.govee_h617e_segment_0
    - light.govee_h617e_segment_1
    # ... all segments
```

Dann:
```yaml
service: light.turn_on
target:
  entity_id: group.light_h617e_all_segments
data:
  rgb_color: [255, 0, 0]
```

### F: Kann ich Segmente mit einem Template auswählen?
**A:** Ja, mit `target.entity_id`:

```yaml
service: light.turn_on
target:
  entity_id: |
    {% for i in range(0, 5) %}
      light.govee_h617e_segment_{{ i }}
      {%- if not loop.last %},{% endif %}
    {% endfor %}
data:
  rgb_color: [255, 0, 0]
```

---

## 📊 Monitoring & Debugging

### F: Wie überprüfe ich die Logging-Ausgaben?
**A:**
1. Öffnen Sie Settings → System → Logs
2. Geben Sie "govee_h617e" ein
3. Klicken Sie "START FOLLOW"
4. Sollte Logs in Echtzeit anzeigen

### F: Wie finde ich die BLE-MAC-Adresse?
**A:**
1. Öffnen Sie Settings → System → About
2. Scrollen Sie zu "Bluetooth"
3. Suchen Sie nach "H617E" oder "Govee"
4. Die MAC-Adresse ist neben dem Gerät aufgelistet

### F: Wie exportiere ich Logs zur Fehlerbehebung?
**A:**
1. Settings → System → Logs
2. Klicken Sie auf "DOWNLOAD FULL LOGS"
3. Dies speichert die kompletten Logs

### F: Welche Debugging-Informationen sollte ich sammeln?
**A:** Falls Sie einen Bug melden:
```
1. Home Assistant Version
2. Integration Version
3. H617E Firmware Version
4. Relevante Logs (30 Sekunden)
5. Fehlermeldung (komplett)
6. Schritte zum Reproduzieren
```

---

## 🔐 Sicherheit & Privacy

### F: Werden Farbdaten irgendwohin übertragen?
**A:** Nein, alles ist lokal:
- ✅ BLE-Verbindung nur zum Gerät
- ✅ Keine Cloud-Übertragung
- ✅ Keine Telemetrie
- ✅ Keine Analysen

### F: Ist die Integration sicher?
**A:** Ja, die Integration:
- ✅ Verwendet nur lokale BLE-Verbindung
- ✅ Hat keine externen Abhängigkeiten
- ✅ Wird regelmäßig aktualisiert
- ✅ Ist Open Source zum Prüfen

---

## 🚀 Performance & Optimization

### F: Beeinflusst die Segment-Steuerung die Performance?
**A:** Minimal, wenn Sie:
- ✅ Vernünftige Poll-Intervalle verwenden (>5 Sekunden)
- ✅ Batch-Updates nutzen
- ✅ Optimistic Mode für schnelle UI verwenden

Zeit pro Operation:
- Main Light Update: ~100-200ms
- Segment Color Update: ~150-250ms
- Poll Interval: 30 Sekunden (Standard)

### F: Wie viele Requests können die H617E verarbeiten?
**A:** Dies ist noch nicht vollständig testet, aber:
- ✅ 1-2 Requests pro Sekunde: Stabil
- ⚠️ 3-5 Requests pro Sekunde: Gelegentliche Timeouts
- ❌ >10 Requests pro Sekunde: Häufige Fehler

**Empfehlung**: max 1 Request pro Sekunde pro Gerät.

---

## 📞 Support

### F: Wo finde ich weitere Hilfe?
**A:**
1. **Dokumentation**: Siehe [SEGMENT_CONTROL_GUIDE.md](SEGMENT_CONTROL_GUIDE.md)
2. **Beispiele**: Siehe [EXAMPLES_AUTOMATIONS.yaml](EXAMPLES_AUTOMATIONS.yaml)
3. **GitHub Issues**: [Repository](https://github.com/example/govee_h617e)
4. **Home Assistant Docs**: [HA Integration Docs](https://www.home-assistant.io/integrations/)

### F: Wie melde ich einen Bug?
**A:**
1. Öffnen Sie ein Issue auf GitHub
2. Beschreiben Sie das Problem
3. Geben Sie Logs an
4. Geben Sie Schritte zum Reproduzieren an

### F: Wie kann ich zur Integration beitragen?
**A:**
1. Fork das Repository
2. Erstellen Sie einen Feature Branch
3. Machen Sie Ihre Änderungen
4. Erstellen Sie einen Pull Request
5. Warten Sie auf Code Review

---

**Zuletzt aktualisiert**: 2024
**Status**: Aktiv
**Unterstützte Version**: 0.1.0+
