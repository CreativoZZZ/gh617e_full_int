# 🚀 SCHNELLSTART - Dashboard in 2 Minuten

## ⚡ Der einfachste Weg

### Schritt 1: Datei öffnen
Öffnen Sie die Datei: **`CARD_SIMPLE_CONFIG.yaml`**

### Schritt 2: Code kopieren
- Öffnen Sie die Datei
- Kopieren Sie **ALLES** (Strg+A, Strg+C)

### Schritt 3: In Home Assistant einfügen
1. Öffnen Sie Ihr leeres Dashboard
2. Klicken Sie oben rechts "✎ Edit Dashboard"
3. Klicken Sie "**Create card**"
4. Suchen Sie "**Manual**"
5. Fügen Sie den Code ein (Strg+V)
6. Klicken Sie "**Save**"

**Das war's! ✅**

---

## 🎨 Jetzt können Sie:

✅ Auf jedes Segment klicken  
✅ Eine Farbe auswählen (Farbrad)  
✅ Die Farbe wird sofort angewendet  
✅ Alle 15 Segmente steuern  

---

## ❌ Wenn Sie einen Fehler bekommen:

### "No card type configured"
**Lösung**: Sie haben nur einen Teil des Codes kopiert. 
- Öffne die Datei erneut
- Kopiere von **ganz oben** (`type: vertical-stack`)
- Bis **ganz unten**

### Entity nicht gefunden
**Lösung**: Überprüfen Sie die Entity-ID
1. Settings → Devices & Services
2. Suchen Sie "Govee H617E"
3. Notieren Sie die exakte Entity-ID
4. Ersetzen Sie `light.govee_h617e` durch Ihre ID

### Segmente sichtbar aber ausgraut
**Lösung**: 
- Experimentelle Segmente sind nicht aktiviert
- OR: Hauptlicht ist aus
- Schalten Sie das Hauptlicht an

---

## 📚 Nächste Schritte

Jetzt können Sie:
1. ✅ Lesen Sie [SEGMENT_LAYOUT.md](SEGMENT_LAYOUT.md) - Segment Nummern verstehen
2. ✅ Nutzen Sie [EXAMPLES_AUTOMATIONS.yaml](EXAMPLES_AUTOMATIONS.yaml) - Rainbow-Effekt erstellen
3. ✅ Lesen Sie [FAQ.md](FAQ.md) - Häufige Fragen

---

**Fertig! Genießen Sie die Segment-Steuerung! 🌈**
