# Mechatronik_Projekt_NicoSchenkel

Im Rahmen des Mechatronik Studiums der Frankfurt University of Applied Sciences wurde unter der Betreuung von Prof. Dr.-Ing. Eric Guiffo Kaigom das Modul "Mechatronik-Projekt durchgeführt.

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
Die Ergbnisvideos sind in dem Ordner mit dem selbigen Namen. 
Dabei sindde Ergebnisse unterteilt in:
  - Algorithmus: Zeigt wie der Benutzer die Algorithmen der Objketerkennung und der des Schließens sieht
  - Greifer: Zeigt die Konfiguration bei verschiedenen Objektgrößen, sowie den Unterschied zum Schließen mit und ohne der realsierten Kraftsteuerung

Der wichtigste Code ist die projekt.ipynb file, in dieser ist der Ablauf des Programms
