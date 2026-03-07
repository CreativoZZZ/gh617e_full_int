# Anleitung: Dashboard in Home Assistant einrichten

## Option 1: YAML-Editor nutzen (EMPFOHLEN) ⭐

Das ist die einfachste Methode für das komplette Dashboard:

### Schritt-für-Schritt:

1. **Dashboard-Konfiguration öffnen:**
   - Gehen Sie zu: Settings → Dashboards
   - Klicken Sie auf das Dashboard das Sie erstellt haben
   - Klicken Sie rechts oben auf "⋮" (drei Punkte)
   - Wählen Sie "Edit Dashboard"

2. **YAML-Editor öffnen:**
   - Klicken Sie rechts oben auf "⋮" (drei Punkte)
   - Wählen Sie "Edit Dashboard in YAML"

3. **Inhalt einfügen:**
   - Löschen Sie den existierenden Inhalt
   - Kopieren Sie den kompletten Inhalt von `dashboard_template.yaml`
   - Fügen Sie ihn ein

4. **Speichern:**
   - Klicken Sie "Save"
   - Das Dashboard wird automatisch aktualisiert

---

## Option 2: UI-Editor mit einzelnen Karten

Wenn Sie lieber im UI-Editor arbeiten:

### Schritt-für-Schritt:

1. **Dashboard im UI-Modus öffnen:**
   - Settings → Dashboards → Ihr Dashboard
   - Klicken Sie oben rechts "Edit Dashboard" Button

2. **Heading hinzufügen:**
   - Klicken Sie "Create Card"
   - Suchen Sie "Heading"
   - Geben Sie "H617E RGBIC Control" ein

3. **Hauptlicht hinzufügen:**
   - Klicken Sie "Create Card"
   - Suchen Sie "Light"
   - Wählen Sie `light.govee_h617e`
   - Name: "Main Light"

4. **Segment-Karten hinzufügen:**
   - Für jedes Segment (0-14):
     - Klicken Sie "Create Card"
     - Wählen Sie "Light"
     - Entity: `light.govee_h617e_segment_X` (X = 0-14)
     - Name: "Segment X+1"

5. **Anordnung:**
   - Klicken Sie und ziehen Sie Karten um sie zu arrangieren
   - Gruppieren Sie Segmente in 5er-Gruppen

6. **Speichern:**
   - Klicken Sie oben "Save" Button

---

## Option 3: Schnell mit einer Vertical-Stack Card (Für Anfänger)

Wenn Sie nur einige Segmente testen möchten:

### Konfiguration für einzelne Card:

```yaml
type: vertical-stack
cards:
  - type: heading
    heading: H617E Segments Test
  
  - type: light
    entity: light.govee_h617e
    name: Main Light
  
  - type: horizontal-stack
    cards:
      - type: light
        entity: light.govee_h617e_segment_0
        name: "1"
      - type: light
        entity: light.govee_h617e_segment_1
        name: "2"
      - type: light
        entity: light.govee_h617e_segment_2
        name: "3"
      - type: light
        entity: light.govee_h617e_segment_3
        name: "4"
      - type: light
        entity: light.govee_h617e_segment_4
        name: "5"
```

### So verwenden Sie diese:

1. Im Dashboard: "Create Card" → "Manual"
2. Kopieren Sie die komplette YAML oben ein
3. Klicken Sie "Save"

Jetzt haben Sie die Hauptlicht-Steuerung und 5 Test-Segmente! 

---

## ⚠️ Wichtig: Richtige Entity-IDs

**Überprüfen Sie die Entity-IDs!**

Die Entity-IDs in den Beispielen gehen von standardmäßiger Benennung aus:
- `light.govee_h617e` 
- `light.govee_h617e_segment_0`

Falls Ihre Entity-IDs anders heißen:
1. Gehen Sie zu Settings → Devices & Services
2. Suchen Sie "Govee H617E"
3. Notieren Sie die exakten Entity-IDs
4. Verwenden Sie diese in der Konfiguration

---

## 🎯 Empfohlener Weg

**Für Anfänger**: Option 2 (UI-Editor) - Einfach und intuitiv  
**Für Fortgeschrittene**: Option 1 (YAML-Editor) - Vollständiges Dashboard in Sekunden  
**Zum Testen**: Option 3 (Single Card) - Schnell 5 Segmente überprüfen

---

## Troubleshooting

### "No card type configured" Error
**Ursache**: Sie verwenden eine komplette Dashboard-YAML für eine einzelne Card  
**Lösung**: Nutzen Sie entweder YAML-Editor des Dashboards (Option 1) oder verwenden Sie nur die Card-Config (Option 3)

### Entity nicht gefunden
**Ursache**: Falsche Entity-ID  
**Lösung**: Überprüfen Sie die genaue Entity-ID in Settings → Devices & Services

### Segmente werden nicht angezeigt
**Ursache**: Experimentelle Segmente nicht aktiviert  
**Lösung**: Settings → Devices & Services → Govee H617E → Options → Enable experimental segment features

---

**Tip**: Nach dem Speichern müssen Sie die Website nicht neu laden - das Dashboard aktualisiert sich automatisch!
