function Domanda(q, ordine, el) {
    this.questionario = q;
    this.ordine = ordine;
    this.el = $(el);
    this.id = this.el.data('question-id');
    this.risposta = 0;
}
Domanda.prototype.set_risposta = function(v) {
    if (!( -3 <= v <= 3)) { console.log('Invalid answer to question', this, v); return false }
    this.risposta = v;
    return true;
};
Domanda.prototype.sibling = function(v) {
    var position = this.questionario.domande.indexOf(this);
    if (position == -1) { console.log('This question is not registered to survey', this, v, this.questionario); return undefined; }
    return this.questionario.domande[position+v];
};
Domanda.prototype.next = function(n) { return this.sibling(+1 * (n || 1)); };
Domanda.prototype.prev = function(n) { return this.sibling(-1 * (n || 1)); };
Domanda.prototype.is_last = function() { return this.questionario.domande[this.questionario.domande.length-1] == this; };

function Questionario(url, id_navigatore, id_pulsantiera, class_domande) {
    // setup navigation
    this.navigatore = $(id_navigatore || '#navigatore');
    this.indietro = this.navigatore.find('li').first().click(function(){
        var prev = this.get_domanda_corrente().prev();
        if (prev!= undefined) { this.select_domanda( prev.id ); }
    }.bind(this));
    this.avanti = this.navigatore.find('li').last().click(function(){
        var next = this.get_domanda_corrente().next();
        if (next != undefined) { this.select_domanda( next.id ); }
    }.bind(this));

    this.pulsantiera = $(id_pulsantiera || '#pulsantiera');
    this.url = url;
    this.domande = $.map(
        // for each question
        $(class_domande || '.domanda'),
        // create a Domanda instance with order and id
        function(domanda, ix) {
            return new Domanda( this, ix+1, domanda );
        }.bind(this)
    );

    this.pulsantiera.find('button').bind('click',this.on_answer.bind(this));
}
// Event methods
Questionario.prototype.on_answer = function(event) {
    event.preventDefault();
    this.pulsantiera.find('button').unbind('click');

    var el = $(event.target);
    var current = this.get_domanda_corrente();
    if ( current.set_risposta( el.data('value') ) ) {
        var next = current.next();
        if (next) {
            this.select_domanda(next.id);
            this.pulsantiera.find('button').bind('click',this.on_answer.bind(this));
        }
        else {
            if (this.is_completed()) {
                this.send();
            }
            else {
                console.log('Error: survey is not completed and there is not other questions', this, next);
            }
        }
    }
};
// Add methods
Questionario.prototype.is_completed = function(){
    // all question must have an answer (!=0)
    return $.grep(this.domande, function(d){
        return d.risposta != 0;
    }).length == this.domande.length;
};
Questionario.prototype.select_domanda = function(question_id){
    // clean old answer
    this.pulsantiera.find('button').removeClass('selected');

    // retrieve this question
    var question = this.get_domanda(question_id);
    if (question == undefined) { console.log('Cannot select a question', question_id); return false; }

    // hide current question
    this.get_domanda_corrente().el.hide();

    // remove old position
    this.navigatore.find('li.posizione').removeClass('posizione');
    // remove icon ok
    this.pulsantiera.find('button i').remove();

    // move navigator to current question
    this.navigatore.find('li:nth-child('+(question.ordine+1)+')').addClass('posizione').removeClass('disabled');

    // show selected question
    question.el.show();

    // if has answer
    if (question.risposta != 0) {
        // select that
        this.pulsantiera.find('button').each(function(ix, el){
            var $el = $(el);
            if ($el.data('value') == question.risposta) {
                $el.append($('<i class="icon-ok icon-white" />'));
                $el.addClass('selected');
            }
        });
    }

    // enable navigation arrows

    if (question.ordine > 1) { this.indietro.removeClass('hide'); }
    else { this.indietro.addClass('hide'); }

    if (question.is_last()) {
        console.log('last', question);
        this.avanti.addClass('hide');
    }
    else {
        console.log('next',question.next().risposta);

        if (question.risposta == 0 && question.next().risposta == 0) {
            this.avanti.addClass('hide');
        }
        else {
            this.avanti.removeClass('hide');
        }
    }

    console.log('Question selected', question);

    return true;
};
Questionario.prototype.get_ultima_domanda_con_risposta = function() {
    for (var i = 0; i < this.domande.length; i++) {
        if ( this.domande[i].risposta == 0 ) {
            return this.domande[i-1]; // previous
        }
    } return undefined;
};
Questionario.prototype.get_domanda = function(question_id){
    var results = $.grep(this.domande, function(d) { return d.id == question_id});
    if (results.length != 1) { console.log('invalid question id', question_id, results); return undefined; }
    return results[0];
};
Questionario.prototype.get_domanda_corrente = function() {
    // check current position from navigatore
    var question_id = this.navigatore.find('.posizione span').data('question-id') || 0;
    if (question_id == 0) { console.log('question id not found', question_id); return undefined; }
    return this.get_domanda(question_id);
};
Questionario.prototype.show_message = function(msg){};
Questionario.prototype.send = function(){
    console.log('send results', $.map(this.domande, function(el){ return el.risposta }));
};
Questionario.prototype.build_results = function(results){};