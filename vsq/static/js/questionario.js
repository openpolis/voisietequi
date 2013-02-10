function Domanda(q, ordine, el) {
    this.questionario = q;
    this.ordine = ordine;
    this.el = $(el);
    this.id = this.el.data('question-id');
    this.risposta = 0;
}
Domanda.prototype.set_risposta = function(v) {
    if (v == 0 || !( -3 <= v <= 3 )) { console.log('Invalid answer to question', this, v); return false }
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

function Questionario(url, election_code, callback, id_questionario, id_userdata, id_navigatore, id_pulsantiera, class_domande) {
    this.url = url;
    this.election_code = election_code;
    this.callback = callback;
    this.box = $(id_questionario || '#domande-questionario');
    this.userbox = $(id_userdata || '#utente-questionario');

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
    this.domande = $.map(
        // for each question
        $(class_domande || '.domanda'),
        // create a Domanda instance with order and id
        function(domanda, ix) {
            return new Domanda( this, ix+1, domanda );
        }.bind(this)
    );
    // add event on button click
    this.pulsantiera.find('button').bind('click',this.on_answer.bind(this));

    // initialize user_data form
    $(this.userbox).find('form').validate({
        submitHandler: this.send.bind(this),
        //debug: true,
        errorElement: 'span',
        errorClass: 'help-inline',
        errorPlacement: function(error, element){
            error.insertAfter(element);
            error.parent().parent().addClass('error');
        },
        highlight: function(element, errorClass, validClass) {
            $(element).parent().addClass('error')
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parent().removeClass('error')
        },
        validClass: "success",
        rules: {
            nickname: {
                required: true,
                maxlength: 25,
                minlength: 3
            },
            email: {
                required: true,
                email: true
            }
        },
        messages: {
            nickname: {
                required: "Specifica un nickname",
                minlength: jQuery.format("Il nickname deve essere almeno {0} caratteri"),
                maxlength: jQuery.format("Il nickname deve essere lungo massimo {0} caratteri")
            },
            email: {
                required: "Scrivi la tua email",
                email: "L'indirizzo email deve essere nel formato name@domain.com"
            }
        }
    });
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
                this.box.hide();
                this.userbox.show();
                console.log('show user data box');
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

    var data_json = {
        'user_data': {},
        'answers': {},
        'election_code': this.election_code
    };
    $.each(this.domande, function(ix,el){ data_json['answers'][el.id] = el.risposta });
    $.each(this.userbox.find('form').serializeArray(), function(ix,input){ data_json['user_data'][input.name] = input.value });

    console.log('send results...', data_json);

    $.ajax
    ({
        type: "POST",
        //the url where you want to sent the userName and password to
        url: this.url,
        dataType: 'json',
        //json object to sent to the authentication url
        data: JSON.stringify(data_json, null, '\t')
    })
    // The jqXHR.success(), jqXHR.error(), and jqXHR.complete() callbacks are deprecated as of jQuery 1.8.
    // To prepare your code for their eventual removal, use jqXHR.done(), jqXHR.fail(), and jqXHR.always() instead.
    .done(function(data, textStatus, jqXHR) { this.callback(data, data_json); })
    .fail(function(data, textStatus, jqXHR) { console.log('Error:', data, textStatus, jqXHR) })
};
Questionario.prototype.build_results = function(results){};