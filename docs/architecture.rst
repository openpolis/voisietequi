Architettura
------------
L'architettura del sistema, con le componenti, è illustrata in questo schema:

.. image:: https://raw.github.com/openpolis/voisietequi/master/docs/images/architettura2016.png
   :height: 200
   :width: 600
   :scale: 50
   :alt: Architettura dei componenti


VSQ
===
Il modulo **vsq** è l'applicazione django che permette la visualizzazione e la gestione del sito
relativo a una singola istanza. Ad esempio: http://rom2016.voisietequi.it. 
Sia la parte di front-end che quella di back-end dell'applicazione sono generate da questo modulo, 
che, si appoggia su un DB postgres.


COMPUTER
========
Il modulo **computer** effettua il calcolo della posizione degli utenti o dei partiti (tramite octave) a partire dalle risposte date.
E' configurato come un servizio esterno *disaccoppiato* rispetto alla applicazione principale.
E' un'applicazione web (web.py), configurabile dinamicamente da remoto, attraverso dei messaggi ZMQ appositi.
Il suo compito principale è fornire la posizione di un utente in base alle risposte date al set di domande,
conoscendo le risposte date dai partiti (inviate nel messaggio di configurazione).

Il modulo utilizza il sistema di messaggistica (**0mq**) sia per mettere in coda le richieste
di scrittura delle risposte utente nel DB, sia ricevere messaggi di configurazione da remoto. 
In particolare, sono usati:

  - una versione modificata del pattern Pipeline (http://rfc.zeromq.org/spec:30)
per l'invio dei risultati del calcolo al server che ha il compito di effettuare la scrittura sul DB;
i computer inviano i risultati su un socket di tipo PUSH/PULL;
  - il pattern Publish and Subscribe (http://rfc.zeromq.org/spec:29) per l'invio 
da remoto dei messaggi di configurazione del computer; i computer sottoscrivono un canale PUB/SUB sul 
quale ricevono i messaggi;



WEBSHOTS
========
Il modulo **webshots** effettua la rasterizzazione del contenuto visualizzato da un browser,
in una certa URL. E' un modulo generico, riadattato per voisietequi, in modo che risponda esclusivamente
a richieste con url ``/vsq-screenshots``.
Il suo compito è si trasformare l'html + javascript d3 che genera la mappa di un risultato utente in
un'immagine raster, in modo che essa possa essere scaricata e condivisa.

E' un'applicazione express (node.js), che utilizza phantomJS (http://phantomjs.org/screen-capture.html).


SAVER
=====
Il modulo **saver** implementa il socket PULL del pattern Pipeline per la ricezione dei messaggi contenenti
le risposte al test degli utenti e il loro posizionamento (coordinate) rispetto ai partiti. 
La ricezione di un messaggio scatena l'inserimento di risultati e posizionamento nel DB.


DEPLOY
======
Il deploy dell'istanza è fatto attraverso ansible, il codice del deploy è in un repository privato.

Il sito web (modulo VSQ) è servito da uWSGI, su porte 8011-8015 (vedi tabella seguente).
I singoli servizi sono definiti in upstart con nome ``voisietequi-roma2016-uwsgi`` e simili.

**Nginx** è utilizzato per servire i contenuti statici del sito, 
fa da load balancer per le richieste indirizzate ai moduli *vsq*, *computer*, e *webshots*.
Quando è attivo varnish, risponde su porta 8001, altrimenti direttamente su porta 80.

**Varnish**  è il web server (cache e reverse proxy), quando necessario risponde su porta 80.

Il modulo saver è lanciato e tenuto in piedi attraverso ``supervisord``, ed è un management task di django.
Il bind al socket di tipo PULL avviene su porta 5561-5565 (vedi tabella).

Il modulo computer è servito da uwsgi in modalità emperor e l'emperor è nell'upstart, con nome uwsgi, 
i servizi gestiti sono in ``/etc/uwsgi/vassals``. Le porte sono 8081-8085 (vedi tabella).

Il modulo webshots è direttamente servito da node su porta 3000, tenuto in piedi da supervisor e
apache risponde su porta 80 del dominio webshots.openpolis.it, effettuando un proxy su porta 3000.





Descrizione dei processi
------------------------
Ci sono tre processi che meritano una descrizione dettagliata:

* lo startup e la configurazione dinamica di un modulo computer,
* il calcolo del grafico di un utente
* la scrittura dei risultati nel DB

per il resto si tratta di un'applicazione web abbastanza standard.


Configurazione modulo computer
==============================
Il modulo computer è pensato per essere indipendente, può essere utilizzato in differenti contesti.
Una volta installato e lanciato, la configurazione avviene attraverso un messaggio in broadcast (PUB-SUB),
lanciato dal server manualmente (django management task).

L'immagine mostra il pattern.

.. image:: https://raw.github.com/openpolis/voisietequi/master/docs/images/command.png
   :height: 200
   :width: 600
   :scale: 50
   :alt: Pattern di invio comando e ricezione risposta ai computers

Il computer deve conoscere l'indirizzo del server che invia i comandi e il codice elezione. (es: tcp://localhost:5556)
All'avvio, il computer si mette in ascolto (SUB) sul canale equivalente al codice elezione, specificato
in configurazione (env).

Attraverso un management task sul server, si può inviare in broadcast, ai computer, un
comando di configurazione (PUB), specificando, come topic del broadcast, il codice elezione.
Nel corpo del comando è indicato l'indirizzo dove inviare la risposta al comando (status: ok) ed eventualmente l'indirizzo
dove inviare i messaggi da salvare.
La risposta viene inviata al server al termine della configurazione, attraverso il pattern PUSH-PULL.
Il management task di configurazione termina quando non sono più presenti messaggi di risposta,
o dopo un timeout adeguato.

Struttura del messaggio di configurazione
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code::

    {
        header: {
            cmd: 'configure',
            reply_address: 'tcp://SERVER_HOST:REPLY_PORT'
        },
        body {
            risposte: {
                PD: { 1: 1, 2: -1, 3: -1, ... },
                PDL: { 1: -1, 2: -2, 3: 2, ... },
                ...
            },
            saver_address: 'tcp://SERVER_HOST:SAVER_PORT'
        }
    }


Struttura del messaggio di risposta alla configurazione
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code::

    {
        computer_id: C_ID,
        response: OK|ERR,
        error_message: ""|"Messaggio di errore"
    }



Lettura configurazione dei moduli computer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Seguendo un identico pattern, si può inviare a tutti i computer, per tutti i topic,
una richiesta di mostrare i dettagli della configurazione.

Richiesta in broadcast, no topic.
.. code::

    {
        header: {
            cmd: 'discover',
            reply_address: 'tcp://SERVER_HOST:REPLY_PORT'
        },
        body {
        }
    }


Risposta
.. code::

    {
        computer_id: C_ID,
        response:
        {
            election_code: 'POLITICHE_2013',
            risposte: {
                PD: { 1: 1, 2: -1, 3: -1, ... },
                PDL: { 1: -1, 2: -2, 3: 2, ... },
                ...
            },
            saver_address: 'tcp://SERVER_HOST:SAVER_PORT'
        }
    }



Calcolo del grafico di un utente
================================
Il calcolo della posizione di un utente, date le sue risposte e le risposte ai partiti, è richiesto
direttamente dal javascript al modulo **computer** attraverso una richiesta AJAX di tipo POST.

Il componente riceve le risposte dell'utente, con i suoi dati ed effettua il calcolo, usando **numpy** e **scipy**,
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
