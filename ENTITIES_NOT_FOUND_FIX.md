# 🔍 Entity-IDs überprüfen & Segmente finden

## Schritt 1: Überprüfen Sie die experimentellen Segmente

⚠️ **WICHTIG - Experimentelle Segmente aktiviert?**

1. Gehen Sie zu: **Settings → Devices & Services**
2. Suchen Sie nach "**Govee H617E**"
3. Klicken Sie auf das Gerät
4. Klicken Sie auf das **Zahnrad-Symbol (⚙️)** oben rechts
5. Aktivieren Sie "**Enable experimental segment features**"
6. Klicken Sie "Save"

✅ **Dann müssen Sie Home Assistant NEU STARTEN!**
- Settings → System → System Options → Restart Home Assistant

---

## Schritt 2: Überprüfen Sie die Entity-IDs

### Option A: Über Developer Tools (BESTE METHODE)

1. Öffnen Sie: **Settings → Developer Tools → States**
2. Suchen Sie im Search-Feld nach: `govee`
3. Sie sollten sehen:
   ```
   light.govee_h617e
   light.govee_h617e_segment_0
   light.govee_h617e_segment_1
   light.govee_h617e_segment_2
   ... etc
   ```

**Kopieren Sie die GENAUEN Entity-IDs die Sie sehen!**

---

### Option B: Über Geräte-Liste

1. Gehen Sie zu: **Settings → Devices & Services**
2. Suchen Sie: "**Govee H617E**"
3. Klicken Sie auf das Gerät
4. Scrollen Sie nach unten zu "**Entities**"
5. Sie sollten sehen:
   - `light.govee_h617e` (Hauptlicht)
   - `light.govee_h617e_segment_0` bis `light.govee_h617e_segment_14` (Segmente)

---

## 🆘 Was wenn die Segmente NICHT angezeigt werden?

### Überprüfungs-Checkliste:

- [ ] Experimentelle Segmente AKTIVIERT in Options?
- [ ] Home Assistant NEUGESTARTET nach Aktivierung?
- [ ] BLE-Verbindung OK (Device verfügbar)?
- [ ] Mindestens 30 Sekunden nach Neustart gewartet?

### Schritt für Schritt Fehlerbehebung:

#### 1. Experimentelle Segmente prüfen
```
Settings → Devices & Services → Govee H617E → ⚙️ Options
→ "Enable experimental segment features" sollte AKTIVIERT sein
```

#### 2. Home Assistant neu starten
```
Settings → System → System Options → Restart Home Assistant
```
Warten Sie 1-2 Minuten bis HA vollständig hochgefahren ist.

#### 3. Check ob Entities geladen sind
```
Settings → Developer Tools → States
Suchen Sie nach: "govee_h617e_segment"
```

#### 4. Logs überprüfen auf Fehler
```
Settings → System → Logs
Suchen Sie nach: "govee_h617e"
Kopieren Sie Fehlermeldungen
```

---

## 🔧 Falls Entity-IDs anders heißen

Wenn Ihre Entity-IDs anders heißen (z.B. `light.h617e` statt `light.govee_h617e`):

1. Notieren Sie die **genauen** Entity-IDs
2. Öffnen Sie das Dashboard
3. Klicken Sie "✎ Edit Dashboard"
4. Klicken Sie auf die Card mit den Segmenten
5. Bearbeiten Sie die YAML und ersetzen Sie:
   - `light.govee_h617e_segment_0` → `light.YOUR_ACTUAL_ID_segment_0`
   - etc.

Beispiel:
```yaml
# Von:
entity: light.govee_h617e_segment_0

# Zu (falls Ihre ID anders ist):
entity: light.h617e_segment_0
# oder
entity: light.govee_h617e
# oder was auch immer Sie in Developer Tools sehen
```

---

## ❓ Häufige Fehler

### Fehler 1: "entity not found"
**Ursache**: Entity-ID ist falsch  
**Lösung**: 
1. Gehen Sie zu Developer Tools → States
2. Suchen Sie nach der korrekten Entity-ID
3. Kopieren Sie diese
4. Ersetzen Sie sie in der Card-Config

### Fehler 2: Segmente sind da, aber ausgegraut
**Ursache**: 
- Experimentelle Segmente nicht aktiviert
- ODER: Hauptlicht ist ausgeschaltet
- ODER: Device nicht verbunden

**Lösung**:
1. Überprüfen Sie Options (experimentelle Segmente aktiv?)
2. Schalten Sie das Hauptlicht ein: `light.govee_h617e` → ON
3. Überprüfen Sie die BLE-Verbindung

### Fehler 3: Nur Hauptlicht angezeigt, keine Segmente
**Ursache**: 
- Home Assistant nicht neu gestartet
- ODER: Experimentelle Segmente sind nicht aktiviert
- ODER: light.py wurde nicht neu geladen

**Lösung**:
1. Aktivieren Sie experimentelle Segmente
2. Starten Sie Home Assistant EU:
   - Settings → System → System Options → Restart Home Assistant
3. Warten Sie 2-3 Minuten
4. Aktualisieren Sie den Browser (F5)

---

## 📝 So kopieren Sie die Entity-IDs

### Methode 1: Developer Tools (EMPFOHLEN)

1. **Settings → Developer Tools → States**
2. **Suchen**: `govee_h617e_segment`
3. Sie sehen eine Liste wie:
   ```
   light.govee_h617e_segment_0  (on/off)
   light.govee_h617e_segment_1  (on/off)
   light.govee_h617e_segment_2  (on/off)
   ...
   ```

Diese sind die **korrekten Entity-IDs** zum einfügen!

### Methode 2: Entities-Liste

1. **Settings → Devices & Services → Entities**
2. **Suchen**: `govee`
3. Alle Entity-IDs werden angezeigt
4. Klicken Sie auf eine, um die volle ID zu kopieren

---

## ✅ Checklist zum Überprüfen

```
✅ Schritt 1: Experimentelle Segmente aktiviert?
   [ ] Settings → Govee H617E → Options → "Enable experimental segment features" = ON

✅ Schritt 2: Neugestartet?
   [ ] Settings → System → System Options → Restart Home Assistant

✅ Schritt 3: Im Developer Tools sichtbar?
   [ ] Settings → Developer Tools → States → Suche "govee_h617e_segment"
   [ ] Mindestens 1 Segment-Entity sichtbar?

✅ Schritt 4: BLE-Verbindung OK?
   [ ] Device in "Bluetooth" verfügbar?
   [ ] light.govee_h617e "available" Status hat?

✅ Schritt 5: Entity-IDs korrekt?
   [ ] Card verwendet die GENAUEN Entity-IDs aus Step 3?
```

---

## 🚀 Quick Fix

Falls die Entity-IDs anders heißen, lesen Sie die Korrektur-Datei:
→ Siehe **ENTITY_ID_REPLACEMENT.md** (wird erstellt)

---

**Bitte führen Sie diese Schritte durch und teilen Sie mir mit:**
1. Sehen Sie die Segment-Entities in Developer Tools → States?
2. Wie heißen die Entity-IDs genau?
3. Welche Fehlermeldungen sehen Sie im Dashboard?

Dann kann ich die exakte Lösung bereitstellen! 🔧
