# PDF ChatBot
> Chatte mit deinen PDF-Dokumenten über die ChatGPT-API von OpenAI

PDF ChatBot ist ein privates Projekt, mit dem ich das Erstellen eines Chat Bots mit Streamlit
und Langchain ausprobiert habe, um damit Konversationen mit ChatGPT unter Verwendung der API
von OpenAI und beliebigen PDF-Dokumenten führen zu können.

Streamlit stellt hier das Web-Frontend für den Upload von PDF-Dokumenten in einen
lokalen FAISS Vector Store (CPU-basiert) sowie für die Darstellung der Konversation
über die Inhalte der PDF-Dokumente mit dem Large Language Model (LLM) von ChatGPT.

Langchain bildet hier das Backend für die Verbindung zum FAISS Vector Store und die
Konversation mit ChatGPT.

Die Verwendung der API von OpenAI ist kostenpflichtig, ohne eure Zahlungsinformationen
wird euer angelegter API-Schlüssel nur eine bedingte Zeit für Abfragen ausreichen, wenn ihr 
den PDF Chat Bot selbst verwenden möchtet.

## Installation und Starten von PDF ChatBot

PDF ChatBot habe ich auf einem Ubuntu-Rechner entwickelt und getestet. Er wird
mit hoher Wahrscheinlichkeit aber auch unter einem Windows- oder Mac OS-Betriebssystem
laufen können, insbesondere, wenn ihr Docker verwendet. Da ich das aber nicht getestet
habe, beschränke ich mich in der Installationsanleitung auf ein Debian-basiertes
Betriebssystem.

Das Repository könnt ihr entweder als .zip-Datei über den entsprechenden Button im
Web-Browser herunterladen und manuell auf euerem Rechner entpacken oder ihr verwendet
dafür git:

```shell
sudo apt update && sudo apt install git
git clone https://github.com/steffen-roesemann/pdf_chat_bot.git
cd pdf_chat_bot
```

### Konfiguration der .env-Datei

Egal, ob ihr das Repository nun mit git oder manuell heruntergeladen und entpackt habt,
müsst ihr nun eine .env-Datei erzeugen. Hierzu steht euch die Datei .env.example
zur Verfügung.

Öffnet die Datei mit einem Texteditor eurer Wahl und tragt in die dort enthaltenen
Schlüssel die erforderlichen Werte ein.

Die Datei .env.example sieht wie folgt aus:

```
OPENAI_API_KEY=""
OPENAI_MODEL="gpt-3.5-turbo"
FAISS_LOCAL_VECTORSTORE="faiss_index"
APPLICATION_HEADER="PDF ChatBot"
APPLICATION_USER_AVATAR=""
APPLICATION_BOT_AVATAR=""
```

Hierzu folgende Hinweise zu den einzelnen Schlüsseln:

OPENAI_API_KEY:

Unter https://platform.openai.com/account/api-keys könnt ihr für die Applikation einen
API-Schlüssel erstellen. Kopiert diesen und fügt ihn zwischen die Anführungszeichen ein,
damit der PDF ChatBot sich mit dem API-Schlüssel bei ChatGPT authentifizieren kann.

Gebt diesen API-Schlüssel unter keinen Umständen an Dritte weiter, da dieser ansonsten
missbräuchlich verwendet werden kann und euch Kosten entstehen. 

Unter https://platform.openai.com/account/billing/overview könnt ihr eurem OpenAI-Account
eine Zahlungsmethode (z.B. Kreditkarte) hinzufügen, um für die API-Nutzung von ChatGPT
zu zahlen.

OPENAI_MODEL:

Das Sprachmodell "gpt-3.5-turbo" ist derzeit das standardisierte Sprachmodell für Anfragen
an die ChatGPT-API von OpenAI. Nachdem ihr eine Zahlungsmethode hinzugefügt habt, müsst ihr
zwei Tage warten, damit ihr die API im vollen Umfang verwenden könnt. Dies soll
missbräuchlicher Nutzung vorbeugen.

Sofern ich es richtig verstanden habe, könnt ihr hier für den Zugriff auf das verbesserte
Sprachmodell GPT-4 den Wert "gpt-4" eintragen, sofern ihr bereits einen US-Dollar an OpenAI
für die Nutzung der API bezahlt habt (die Warteliste für den Zugriff auf GPT-4 ist meines
Wissens nach aufgelöst worden).

FAISS_LOCAL_VECTORSTORE:

Hier könnt ihr einen beliebigen Namen wählen. ;-)

APPLICATION_HEADER:

Der Wert, den ihr hier eintragt, bestimmt die Bezeichnung des Tabs im Web-Browser, in dem
ihr den PDF ChatBot geöffnet habt, sowie die Überschrift des Chat-Hauptfensters. Den Wert
könnt ihr frei wählen.

APPLICATION_USER_AVATAR:

Hier könnt ihr eine URL eintragen, um ein benutzerdefiniertes Bild für den Benutzer oder die
Benutzerin des PDF ChatBots zu hinterlegen.

APPLICATION_BOT_AVATAR:

Hier könnt ihr eine URL eintragen, um ein benutzerdefiniertes Bild für den Bot zu hinterlegen, das
während Konversationen angezeigt wird.

### Betrieb der Applikation nativ oder über Docker

Danach müsst ihr euch entscheiden, ob ihr die Applikation nativ auf dem Rechner
laufen lassen wollt oder über einen Docker-Container. 

Ich empfehle die Verwendung von Docker (1. Alternative), beschreibe aber auch die Schritte 
zum nativen Betrieb auf dem Rechner (2. Alternative).

1. Alternative (Betrieb im Docker-Container):

Eine Anleitung für die Installation von Docker für die unterschiedlichen
Betriebssysteme findet ihr auf der offiziellen Docker-Webseite unter https://docs.docker.com/engine/.

Nach der Installation von Docker könnt ihr folgende Befehle auf der Kommandozeile eingeben,
um die Applikation in einem Docker-Container zu starten (ggf. müsst ihr die Befehle
mit administrativen Rechten ausführen):

```shell
docker build -t pdf_chat_bot .
docker run -p 8501:8501 pdf_chat_bot
```

Wollt ihr den PDF ChatBot dauerhaft im Hintergrund als Dienst laufen lassen, könnt ihr in dem
docker run-Befehl auch den Schalter -d verwenden:

```shell
docker run -dp 8501:8501 pdf_chat_bot
```

2. Alternative (Nativer Betrieb):

Ich empfehle, die folgenden Befehle in einer virtuellen Python-Umgebung auszuführen. Diese legt
ihr mit folgendem Befehl an und aktiviert sie:

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Im Anschluss könnt ihr die für den PDF ChatBot benötigten Python-Bibliotheken installieren:

```shell
pip3 install -r requirements.txt
```

Nun könnt ihr mit folgendem Befehl streamlit anweisen, über den http-Server von streamlit 
die Applikation auszuliefern, damit ihr über den Web-Browser darauf zugreifen könnt. Das
Sammeln von Nutzungsstatisiken von streamlit wird mit "--browser.gatherUsageStats false" des
des folgende Befehls unterdrückt:

```shell
$(which streamlit) run app.py --browser.gatherUsageStats false
```

### Erreichen des Web-Frontends des PDF ChatBots über einen Web-Browser

Egal, ob ihr euch für die Alternative 1 oder 2 des Betriebs der Applikation entschieden habt,
steht euch der PDF ChatBot danach über http://localhost:8501 zur Verfügung, wenn ihr die URL
über einen Web-Browser aufruft.

## Haftungsausschluss für die Verwendung der Applikation PDF ChatBot

Die folgenden Bedingungen regeln die Nutzung dieser Software. Durch die Verwendung erklären 
ihr euch mit den nachstehenden Bedingungen einverstanden:

Die Software wird "wie sie ist" zur Verfügung gestellt, ohne jegliche ausdrückliche oder stillschweigende Gewährleistung. Dies schließt, aber ist nicht beschränkt auf, Gewährleistungen hinsichtlich der Eignung für einen bestimmten Zweck, der Marktgängigkeit und der Nichtverletzung von Rechten Dritter ein.

Ich übernehme keine Verantwortung oder Haftung für die Richtigkeit, Vollständigkeit, Zuverlässigkeit oder Aktualität der Software oder der damit erzielten Ergebnisse.

In keinem Fall hafte ich für direkte, indirekte, zufällige, besondere oder Folgeschäden, die sich aus der Nutzung oder Unmöglichkeit der Nutzung der Software ergeben, einschließlich, aber nicht beschränkt auf entgangenen Gewinn, Datenverlust, Geschäftsunterbrechung oder jegliche andere kommerzielle Schäden oder Verluste.

Ihr stimmt zu, die Software nur in Übereinstimmung mit den geltenden Gesetzen und Vorschriften zu nutzen. Ich übernehme keine Verantwortung für rechtliche Konsequenzen, die sich aus einer rechtswidrigen Nutzung der Software ergeben.

Ihr erkennt an, dass die Software möglicherweise Fehler, Unvollkommenheiten oder technische Probleme aufweisen kann. Ich übernehme keine Verantwortung für etwaige Schäden oder Datenverluste, die durch solche Probleme verursacht werden.

Jegliche Kommunikation, die über die Software erfolgt, liegt in eurer Verantwortung. Ich hafte nicht für den Inhalt solcher Kommunikation oder die Verwendung, die ihr davon macht.

Durch die Verwendung dieser Software erklären ihr euch damit einverstanden, auf jegliche Ansprüche, Klagen oder Forderungen gegenüber mir zu verzichten, die sich aus der Nutzung der Software ergeben könnte.

Bitte lesen Sie diesen Haftungsausschluss sorgfältig durch, bevor ihr die Software nutzt. Wenn ihr nicht mit den Bedingungen dieses Haftungsausschlusses einverstanden sind, dürfen ihr die Software nicht verwenden.

## Lizensierung dieses Projektes



