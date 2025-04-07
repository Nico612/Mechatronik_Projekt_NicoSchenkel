# Mechatronik_Projekt_NicoSchenkel

Im Rahmen des Mechatronik Studiums der Frankfurt University of Applied Sciences wurde unter der Betreuung von Prof. Dr.-Ing. Eric Guiffo Kaigom das Modul "Mechatronik-Projekt" durchgeführt.

# Kurzzusammenfassung
Ziel des Projekts war es, den 3-Finger-Greifer von Robotiq durch Sensordaten automatisiert zur
Objektmanipulation zu konfigurieren. Hierzu wurde eine Stereokamera am Greifer montiert und
ein vortrainiertes Echtzeit-Objekterkennungsmodell (!YOLO11) eingesetzt. Die Kombination
aus Tiefenbildverarbeitung und Objekterkennung ermöglichte die Identifikation relevanter
Objekte sowie die Bestimmung ihrer Dimensionen. Darauf basierend erfolgte eine automatische
Anpassung des Greifers hinsichtlich Greifmodus und Öffnungsweite. Sowie das Schließen des
Greifers, sobald das Objekt in Reichweite ist.
Zusätzlich wurde durch die Nutzung der internen Sensorik eine objektspezifische Kraftsteue-
rung realisiert. Die gesamte Steuerung wurde in Python entwickelt und modular aufgebaut,
sodass sie leicht anpassbar und erweiterbar ist.
Das Projekt bietet eine praxisnahe Grundlage für eine intuitive, sensorbasierte Interakti-
on zwischen Mensch und Maschine mit einem 3-Finger-Greifer – sowohl in kollaborativen
Anwendungsszenarien als auch bei automatisierten Pick-and-Place-Aufgaben.

## Motivation
Die Motivation für das Projekt entspringt zum einen dem persönlichen Interesse, das All-
tagsleben von Menschen durch den Einsatz von Technologie zu vereinfachen. Zum anderen
aus dem fachlichen Interesse, ein Robotersystem so zu programmieren, dass eine intuitive
Interaktion zwischen Mensch und Maschine ermöglicht wird. Zudem kommt das Interesse
an Sensortechnologien, die ein größeres Verständnis der eigenen Umweltwahrnehmung er-
möglichen. Da die Hand eines der wichtigsten Werkzeuge des Menschen darstellt, um mit
der Umwelt zu interagieren, war das Interesse groß, den handähnlichen 3-Finger-Greifer von
Robotiq so zu programmieren, dass eine intuitive Interaktion zwischen Mensch und Maschine
erreicht wird. Ziel war es, eine Grundlage für diese Form der Zusammenarbeit zu schaffen –
sowohl im alltäglichen als auch im industriellen Kontext


## Ergebnisse
### Modus Wahl und zugreifen
 #### Basic
https://github.com/user-attachments/assets/77ec5cd7-3a51-4e67-9ec9-bc7a5ed30a57

 ###Scissor

https://github.com/user-attachments/assets/8f732cc7-6318-4de4-9797-5b23e53353ec

 ### Pinch
https://github.com/user-attachments/assets/a84617e2-63d8-4120-b9c0-dbeea5d2b813)](https://github.com/user-attachments/assets/22571515-0a4d-4b16-b702-79c79daacaea

### Zu Groß
https://github.com/user-attachments/assets/721227b0-25e7-4cde-9df0-f06c05f0bd77

## Kraftsteuerung
### Mit Steuerung
https://github.com/user-attachments/assets/1ec876d4-64b2-4d2b-bd0c-846bce38c20b](https://github.com/user-attachments/assets/1ec876d4-64b2-4d2b-bd0c-846bce38c20b

### Ohne Steuerung
https://github.com/user-attachments/assets/22d462dd-9e95-494e-b32d-cf39c58db372










