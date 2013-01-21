var c = 0;
var chosed = 0;
var url="/mockup_answer";


//string-fy an object
function DumpObjectIndented(obj, indent)
{
    var result = "";
    if (indent == null) indent = "";

    for (var property in obj)
    {
        var value = obj[property];
        if (typeof value == 'string')
            value = "'" + value + "'";
        else if (typeof value == 'object')
        {
            if (value instanceof Array)
            {
                // Just let JS convert the Array to a string!
                value = "[ " + value + " ]";
            }
            else
            {
                // Recursive dump
                // (replace "  " by "\t" or something else if you prefer)
                var od = DumpObjectIndented(value, indent + "  ");
                // If you like { on the same line as the key
                //value = "{\n" + od + "\n" + indent + "}";
                // If you prefer { and } to be aligned
                value = "\n" + indent + "{\n" + od + "\n" + indent + "}";
            }
        }
        result += indent + "'" + property + "' : " + value + ",\n";
    }
    return result.replace(/,\n$/, "");
}


function show(id){
    if(!id)
        return;
    var obj = document.getElementById(id);
    if(obj)
        obj.style.display = "block";
}

function hide(id){
    if(!id)
        return;
    var obj = document.getElementById(id);
        if(obj)
            obj.style.display = "none";
}


//function that will visualize the response data
function visualize(object){

//    nasconde il form con nickname e mail e visualizza il grafico
  //  hide('modulo_risposte');

    var m = document.getElementById("messaggio");
//    carica nella pagina i dati relativi alla domanda
    m.innerHTML = DumpObjectIndented(object,'');
    show("grafico");
    draw_graph(object.posizioni);


}


function draw_graph(posizioni){

    var maxvalx, maxvaly,minvalx, minvaly;

    //range di ingresso
    maxvalx= maxvaly=10000;
    minvalx= minvaly=0;

    //dimensioni del grafico sulla pagina html
    var w = 400,
        h = 400,
        p = 2,
        //funzione di scala fra input e output
        x = d3.scale.linear().domain([ minvalx, maxvalx]).range([0, w]),
        y = d3.scale.linear().domain([ minvaly, maxvaly ]).range([h, 0]);

    var sampsize = 0;
    var label_array = new Array();
    var val_array=[];

    //    create an array from the posizioni
    var pos_array = _.toArray(posizioni);
    sampsize = pos_array.length;

    for (var i=0; i < sampsize; i++) {

        val_array[i] = { label: "test", x: pos_array[i][0], y: pos_array[i][1], size: 2, color: "#f0f"  };
    }

    var vis = d3.select("#grafico")
        .data([val_array])
        .append("svg:svg")
        .attr("width", w )
        .attr("height", h );


    // Draw xy scatterplot
    vis.selectAll("circle.line")
        .data(val_array)
        .enter().append("svg:circle")
        .attr("class", "line")
        .attr("fill", function(d) { return d.color; } )
        .attr("cx", function(d) { return x(d.x);  })
        .attr("cy", function(d) { return y(d.y); } )
        .attr("r", function(d) { return d.size; });

//
//    // add bubble labels: in two steps
//    vis.selectAll("g.rule")
//        .data(val_array)
//        .append("svg:text")
//        .attr("text-anchor", "middle")
//        .attr("x", function(d) { return x(d.x); })
//        .attr("y", function(d) { return y(d.y) + Math.sqrt( 5*d.size / Math.PI) + 4; })
//        .attr("dy", ".3em")
//        .attr("fill", "black")
//        .attr("clip", "inherit")
//        .text(function(d) { return d.label; });
//
//    vis.selectAll("g.rule")
//        .data(val_array)
//        .enter().append("svg:text")
//        .attr("text-anchor", "middle")
//        .attr("x", function(d) { return x(d.x); })
//        .attr("y", function(d) { return y(d.y) + Math.sqrt( 5*d.size / Math.PI) + 4; })
//        .attr("dy", ".3em")
//        .attr("fill", "black")
//        .attr("clip", "inherit")
//        .text(function(d) { return d.label; });




}



//function that sends data via AJAX
function send_data(url,data){

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    // fire off the request to /form.php
    var request = $.ajax({
        url: url,
        type: "post",
        data: data

    });

    // callback handler that will be called on success
    request.done(function (response, textStatus, jqXHR){
        visualize(response);
    });


}


//this functions validates the user data, if it's valid then call send_data
function validate_submit(){
    var i;
    var data, response;

    if(validate()==true)
    {
        data=collect_data();
        if(data){
            send_data(url,data);
        }

    }

    return false;
}


function validate() {

    var nick = document.getElementById('nickname')
    var ml_email = document.getElementById('ml_email')
    var firstcheck, secondcheck;
    firstcheck=secondcheck=false;
    firstcheck=checkNick(nick.value);
    secondcheck=echeck(ml_email.value);


    if(firstcheck == false || secondcheck== false){
        if (firstcheck==false){
            nick.value=""
            nick.focus()
        }

        if (secondcheck==false){
            ml_email.value=""
            ml_email.focus()
        }
        return false
    }
    else
        return true;

}

//returns the data struct that will be posted
function collect_data(){
    var data = {};
    var user_data={}
    data.answers = [];
    var answers, questionid;
    var i;

//  retrieves user answers
    for(i=1; i<=questions.length-1; i++)
    {
//        use the questions id as an index
        questionid = questions[i]['id']
        if(document.getElementById("t"+questionid).value!='')
            data.answers[""+questionid+""]=document.getElementById("t"+questionid).value;
    }

//    retrieve user name and email
    user_data.name = document.getElementById('nickname').value;
    user_data.email = document.getElementById('ml_email').value;

    data.user_data = user_data;
    return data
}

askNext = function () {
	c++;

	if( c >= questions.length) {
//        se ho finito il questionario nasconde i div delle domande e mostra
//        la form per inserire nome e mail

        hide("domanda");
        hide("posizioni");
        hide("tema_precedente");
        hide("tema_successivo");
        hide("legend");
        show("modulo_risposte");
        return;
	}
	refreshView();
}

askPrev = function () {

	if( c == 1) {
		return;	
	}
	
	c--;
	
	refreshView();	
}

refreshView = function () {
	var k_cnt = document.getElementById("counter");
	var k_acc = document.getElementById("accompagno");
	var k_txt = document.getElementById("questionTxt");
	var k_inf = document.getElementById("approfondimento");
//    carica nella pagina i dati relativi alla domanda
	k_cnt.innerHTML = c;
	k_acc.innerHTML = questions[c].more ? questions[c].more : "";
	k_txt.innerHTML = questions[c].txt;
	k_inf.innerHTML = questions[c].inf;	

//attiva o disattiva i bottoni precedente/successivo

	if (c <= chosed) {
		show("tema_successivo");
	} else {
		hide("tema_successivo");
	}
	
	if (c <= 1) {
		hide("tema_precedente");
	} else {
		show("tema_precedente");
	}

	hide("approfondimento");
	
	resetImgs();
	
	var cell = document.getElementById("t"+c);

//    nel caso l'utente abbia gia' risposto alla domanda C-esima cambia il colore del bottone della risposta
	if (cell.value != "") {

		hide("ch"+cell.value);
		show("ch"+cell.value+"_dwn");
	}
};




//setta l'input nascosto relativo alla scelta dell'utente
chose = function (n) {
	var k_cho = document.getElementById("t"+c);
	k_cho.value = n;
	
	chosed = Math.max(c, chosed);
	
	askNext();
};

function checkNick(str) {
	if (str.length < 2) {
		alert ("Devi usare almeno 2 caratteri per il nome");
		return false
	}
	if (str.length > 24) {
		alert ("Puoi usare al massimo 24 caratteri per il nome");
		return false
	}
	
	return true
}

function echeck(str) {

	var at="@"
	var dot="."
	var lat=str.indexOf(at)
	var lstr=str.length
	var ldot=str.indexOf(dot)
	var err_msg="Indirizzo email errato"
	
	// il campo non è obbligatorio
	if (str=="") return true
	
	if (str.indexOf(at)==-1){
	   alert(err_msg)
	   return false
	}

	if (str.indexOf(at)==-1 || str.indexOf(at)==0 || str.indexOf(at)==lstr){
	   alert(err_msg)
	   return false
	}

	if (str.indexOf(dot)==-1 || str.indexOf(dot)==0 || str.indexOf(dot)==lstr){
	   alert(err_msg)
	    return false
	}

	 if (str.indexOf(at,(lat+1))!=-1){
	   alert(err_msg)
	    return false
	 }

	 if (str.substring(lat-1,lat)==dot || str.substring(lat+1,lat+2)==dot){
	   alert(err_msg)
	    return false
	 }

	 if (str.indexOf(dot,(lat+2))==-1){
	   alert(err_msg)
	    return false
	 }
	
	 if (str.indexOf(" ")!=-1){
	   alert(err_msg)
	    return false
	 }

	return true					
}

function resetImgs () {
	for (var i = -3; i<=3; i++) {

		show("ch"+i);
		hide("ch"+i+"_dwn");
	}
}

function showhideApprofondimento(){
	b = document.getElementById("approfondimento");  
	if (b.style.display == "none"){
		show("approfondimento");
	} else {
		hide("approfondimento");
	}
}

function firstTime(){

//    set the total n. of question on the page
    document.getElementById('nquestions').innerHTML = questions.length-1;
    askNext();
}
