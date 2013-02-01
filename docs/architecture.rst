Architettura
------------
L'architettura del sistema, con le componenti, è illustrata in questo schema:

.. image:: https://raw.github.com/openpolis/voisietequi/master/docs/images/architettura.png
   :height: 200
   :width: 600
   :scale: 50
   :alt: Architettura dei componenti

Il modulo **vsq** è l'app server per tutte le parti dinamiche, tranne le risposte degli utenti.
E' un'applicazione django, si appoggia su un DB postgres.

Il modulo **computer** effettua il calcolo del grafico (tramite octave) a partire dalle risposte dell'utente.
E' un'applicazione web.py, si appoggia su un DB sqlite locale, è configurabile dinamicamente,
per fornire la posizione di un utente in base a un set di domande.
Il modulo utilizza **rabbit mq** per mettere un una coda le richieste di scrittura delle risposte utente nel DB.

I moduli vsq e computer sono applicazioni wsgi, servite da **uwsgi**, in modalità zerg (dynamic scaling).

**Nginx** è utilizzato per servire i contenuti statici, fa da load balancer per le richieste indirizzate al modulo *computer*,
indirizza le richieste dinamiche non nella cache di varnish all'application server django, risponde su porta 8010.

**Varnish**  è il web server (cache e reverse proxy), risponde su porta 80.


Descrizione dei processi
------------------------
Ci sono tre processi che meritano una descrizione dettagliata:

* lo startup e la configurazione dinamica di un modulo computer,
* il calcolo del grafico di un utente
* la scrittura dei risultati nel DB, tramite message-queue (rabbit)

per il resto si tratta di un'applicazione web abbastanza standard.


Configurazione modulo computer
==============================
Il modulo computer è pensato per essere indipendente, può essere utilizzato in differenti contesti.
Una volta installato e lanciato, il modulo può ricevere una richiesta POST e una GET,
alla url ``http://computer.voisietequi.it/configuration``.

.. image:: https://raw.github.com/openpolis/voisietequi/master/docs/images/configurazione.png
   :height: 200
   :width: 600
   :scale: 50
   :alt: Diagramma interazione configurazione modulo computer

La richiesta POST, induce il componente ad autoconfigurarsi dinamicamente, a partire da una URL inviata nel
body del post.
La richiesta GET permette agli amministratori di leggere la configurazione attuale dei un modulo.

Configurazione a partire da una URL (POST)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code::

    request url: http://computer.voisietequi.it/configuration
    request method: POST
    postBody: { dj_url: 'http://www.voisietequi.it/computer_configuration' }

    response status:
      200, se OK,
      400 se KO

Il codice di status nel response header indica se la configurazione ha avuto successo o meno

``dj_url`` è la URL del componente vsq alla quale il componente computer
invia una richiesta  GET per l'auto-configurazione, ricevendo una response json.
Qui sotto i dettagli del dialogo::

    request url: http://www.voisietequi.it/computer_configuration
    request method: GET

    reponse:
    {
      election_code: 'VSQ13',
      risposte: {
        PD: { 1: 1, 2: -1, 3: -1, ... },
        PDL: { 1: -1, 2: -2, 3: 2, ... },
        ...
      }
    }

Le informazioni nella response sono usate dal modulo computer per memorizzare le risposte dei partiti
e l'election code, informazioni necessarie per il calcolo del grafico e la scrittura nel DB.


Lettura configurazione di un modulo computer (GET)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
La richiesta GET, ritorna la configurazione corrente del modulo, in formato json::

    request url: http://computer.voisietequi.it/configuration
    request method: GET

    response:
    {
      election_code: 'VSQ13',
      risposte: {
        PD: { 1: 1, 2: -1, 3: -1, ... },
        PDL: { 1: -1, 2: -2, 3: 2, ... },
        ...
      }
    }


Calcolo del grafico di un utente
================================
Il calcolo della posizione di un utente, date le sue risposte e le risposte ai partiti, è richiesto
direttamente dal javascript al modulo **computer** attraverso una richiesta AJAX di tipo POST.

Il componente riceve le risposte dell'utente, con i suoi dati ed effettua il calcolo, usando **octave**,
ottenendo le coordinate delle posizioni di utente e partiti. Poi, in modalità sincrona invia un messaggio
a una coda, per la scrittura su DB e invia la response JSON al browser dell'utente.

.. image:: https://raw.github.com/openpolis/voisietequi/master/docs/images/calcolo.png
   :height: 200
   :width: 600
   :scale: 50
   :alt: Diagramma interazione calcolo posizione utente

I dettagli della richiesta e della response::

    request url: http://computer.voisietequi.it/computation
    request method: POST
    postBody: {
      election_code: 'VSQ13',
      user_data: {
        email: 'utente@dominio.it',
        nome: 'nome utente'
      },
      risposte: { 1: -3, 2: 3, 3: 1, ... },
    }


    response:
    {
      codice_utente: 'H5033BN18',
      posizioni: {
        1:  [ 'PD', 287, 3945 ],
        2:  [ 'PDL', 3923, 1860 ],
        ...
        N: [ 'USER', 530, 1044 ],
      }
    }


Scrittura dei risultati nel DB
==============================
TODO
