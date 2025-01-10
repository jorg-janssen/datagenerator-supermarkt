## Voorbeelddata voor de casus Autoverhuur
(c) 2024 Hogeschool van Arnhem en Nijmegen, opleiding HBO-ICT

Alle gegevens zijn gegenereerd. Iedere overeenkomst met de werkelijkheid berust op toeval en is niet zo bedoeld. 

Gebruik het bestand inserts.sql om records toe te voegen aan je eigen database. Let dan wel op het volgende:

    - Het bestand is waarschijnlijk te groot om te openen in Management Studio. Je kunt het dan uitvoeren via de command-line met de opdracht

        ```
        sqlcmd -S . -d Supermarkt -i inserts.sql -f 65001
        ```

        - Achter -S staat je server (. is kort voor localhost). Als je gebruikt maakt van Windows-authenticatie op je SQL Server hoef je geen username en wachtwoord op te geven. 
        - Achter -d staat jouw databasenaam.
        - Achter -i de naam van het bestand met insert-instructies.
        - Achter -f staat de 'code page', in dit geval 65001 (Unicode UTF8). Dit is nodig om diakritische tekens zoals ï, é etc. correct te importeren.


