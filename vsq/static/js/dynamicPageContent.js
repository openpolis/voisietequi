/*
 * columns matrix
 * returns the column where a symbol must be put, whe user (rows)
 * and party (columns) gave certain answers to the same question
 */
var dist = {
    '-3': { '-3': 0, '-2': 1, '-1': 2, '1': 3, '2': 4, '3': 5 },
    '-2': { '-3': 1, '-2': 0, '-1': 1, '1': 2, '2': 3, '3': 4 },
    '-1': { '-3': 2, '-2': 1, '-1': 0, '1': 2, '2': 3, '3': 4 },
    '1': { '-3': 4, '-2': 3, '-1': 2, '1': 0, '2': 1, '3': 2 },
    '2': { '-3': 4, '-2': 3, '-1': 2, '1': 1, '2': 0, '3': 1 },
    '3': { '-3': 5, '-2': 4, '-1': 3, '1': 2, '2': 1, '3': 0 }
};

var risposte = {
    '-3': 'Molto contrario/a',
    '-2': 'Contrario/a',
    '-1': 'Tendenzialmente contrario/a',
    '1': 'Tendenzialmente favorevole',
    '2': 'Favorevole',
    '3': 'Molto favorevole'
};

var label_risposte = {
    '-3': 'mc',
    '-2': 'c',
    '-1': 'tc',
    '1': 'tf',
    '2': 'f',
    '3': 'mf'
};


/*
 * places parties' symbols in the generic table
 */
posiziona_distanze_generiche = function(coordinate, partiti){

    // extract user's position
    for (var i in coordinate) {
        if (coordinate[i][0] == 'user') {
            var pos_utente = {'x': coordinate[i][1], 'y': coordinate[i][2]};
        }
    }

    // compute distnaces of user from other parties
    // build both distances (dict) and distance_values (array)
    var distances = {};
    var distance_values = [];
    for (var i in coordinate){
        if ( coordinate[i][0] == 'user' ) continue;
        var pos_partito = {'x': coordinate[i][1], 'y': coordinate[i][2]};
        var distance = Math.sqrt(
            ( pos_utente['x'] - pos_partito['x'] ) * ( pos_utente['x'] - pos_partito['x'] ) +
                ( pos_utente['y'] - pos_partito['y'] ) * ( pos_utente['y'] - pos_partito['y'] ))
        distance_values.push(distance);
        distances[coordinate[i][0]] = distance;
    }

    // compute quantiles for 1-6 range, using D3
    // q(dist) returns the column where to put the party symbol
    var q = d3.scale.quantile().domain(distance_values).range([1,2,3,4,5,6]);

    for (var p in distances) {
        var colonna = q(distances[p]);
        var col_selector = '.tema0 table tr td.verde0'+colonna+'-tab';
        var partito = partiti[p];
        $(col_selector).append(
            '<a href="'+ partito['url']+'">' +
                '<img class="img-circle-coalition img-coalition-'+ partito['coalizione'] +
                ' img-circle-loghi img-circle-normal' + '" ' +
                'src="' + partito['simbolo_url'] + '" ' +
                'alt="' + partito['sigla'] + '"' +
                'title="Distanza: ' + distances[p].toFixed(3)*1000 + '"/>' +
                '</a>'
        );
    }
};

/*
 * places user's answers, with colored labels, in the first column of the thematic tables
 */
posiziona_label_risposte_utente = function(risposte_utente, risposte, label_risposte){
    for (var r in risposte_utente) {
        var risposta_utente = risposte_utente[r];
        var col_selector = '#collapse'+r+' table tr.symbols td.grigio-tab';
        $(col_selector).append(
            '<label class="label label-' + label_risposte[risposta_utente] + '">' +
                risposte[risposta_utente] +
                '</label>'
        );

    }
};

/*
 * places parties' symbols in thematic tables
 */
posiziona_loghi = function(risposte_partiti, risposte_utente, dist, partiti, risposte){
    for (var p in risposte_partiti) {
        var risposte_partito = risposte_partiti[p];
        for (var r in risposte_partito) {
            var risposta_partito = risposte_partito[r];
            var risposta_utente = risposte_utente[r];
            var colonna = dist[String(risposta_utente)][risposta_partito] + 1;
            var col_selector = '#collapse'+r+' table tr.symbols td.verde0'+colonna+'-tab';
            var partito = partiti[p];
            $(col_selector).append(
                '<a href="'+ partito['url']+'">' +
                    '<img class="img-circle-coalition img-coalition-'+ partito['coalizione'] +
                    ' img-circle-loghi img-circle-normal' + '" ' +
                    'src="' + partito['simbolo_url'] + '" ' +
                    'alt="' + partito['sigla'] + '"' +
                    'title="Posizione: ' + risposte[risposta_partito] + '"/>' +
                    '</a>'
            );
        }
    }
};

/*
 * Genera il grafico per l'utente, a partire dalle variabili globali: coordinate
 */
genera_grafico = function(coordinate){
    draw_graph(coordinate,"user", true);
};