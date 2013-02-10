var c = 0;
var chosed = 0;
var label_font_size = 12;
var url="/mockup_answer";

var graph_div="grafico";

//graph entities
var vis;
var labelBox,link;
var links;

//range di ingresso
var maxvalx, maxvaly,minvalx, minvaly;
maxvalx= maxvaly=1;
minvalx= minvaly=0;

var label_charge = -100;
//lunghezza massima in px dei link fra punti e label
var link_len =25;
//dimensioni del grafico sulla pagina html

var graph_width = 480,
    graph_height = 320;


var max_outputx,min_outputx, max_outputy,min_outputy,max_label_len=0;

//dimensioni del marker utente
var user_marker_w, user_marker_h;
user_marker_h=user_marker_w=100;
//delta x e y per posizionare il punteruolo del marker
//esattamente sul punto highlight
var user_marker_delta_x=30;
var user_marker_delta_y=80;

//fattore_scala_cerchi permette di scalare i cerchi concentrici
//sullo sfondo del grafico
var fattore_scala_cerchi=0.29;
//anchor size
var inner_dotsize=4;
var middle_dotsize=inner_dotsize+1;
var outer_dotsize=inner_dotsize+4;

var default_party_color="#aaaaaa";
//dimensioni e colori dei cerchi concentrici
var circles_sizes=[1000,695,488,336,232,166,112,78,52]
var circles_colors=["f3f9f7","e9f3f0","e0ede8","d6e8e0","cee3d9","c5ddd4","bed8cd","b5d4c8","afcfc2"]
var connection_lines;

function draw_graph(coordinate, highlight, marker){

    var label_array = new Array();
    var val_array=[];
    var max_label_len= 0, longest_label=0;
    var highlight_index=null;

    //trova la label con piu' caratteri
    for(var i=1; i< coordinate.length; i++)
        if(coordinate[i][0].length> longest_label)
            longest_label=coordinate[i][0].length;

    //calcola la lunghezza massima della label in px
    max_label_len=longest_label*label_font_size;

    //calcola xy massime per la viewport
    max_outputx = graph_width-(outer_dotsize+link_len+(max_label_len/2));
    min_outputx = (outer_dotsize+link_len+(max_label_len/2));
    max_outputy = graph_height-(outer_dotsize+link_len+label_font_size);
    min_outputy = (outer_dotsize+link_len+label_font_size);


    //funzione di scala fra input e output
    var x = d3.scale.linear().domain([ minvalx, maxvalx]).range([min_outputx, max_outputx]),
        y = d3.scale.linear().domain([ minvaly, maxvaly]).range([max_outputy, min_outputy]);


    for (var i=0; i < coordinate.length; i++) {

        //se trova l'elemento da evidenziare si salva l'indice nel vettore
        if(highlight && coordinate[i][0].toUpperCase()===highlight.toUpperCase())
            highlight_index=i;

        //se non e' definito un highlight o
        // non e' definito il maker mette un marker normale per i punti
        if(!highlight || highlight && coordinate[i][0].toUpperCase()!==highlight.toUpperCase() || !marker){

            // trova il colore associato al partito analizzato
            for (var sigla in partiti) {

                if(coordinate[i][0] == sigla)
                    var color = partiti[sigla].colore;
            }
            //if party was not found, set a default color
            if(color=="")
                color=default_party_color;

            val_array[i] = {
                label: coordinate[i][0],
                x: parseFloat(coordinate[i][1]),
                y: parseFloat(coordinate[i][2]),
                size: inner_dotsize,
                color:color
            };

            color="";
        }
    }

    vis = d3.select("#"+graph_div+"")
        .data([val_array])
        .append("svg:svg")
        .attr("width", graph_width )
        .attr("height", graph_height );


    // Initialize the label-forces
    var labelForce = d3.force_labels()
        .linkDistance(3.0)
        .gravity(0)
        .nodes([]).links([])
        .charge(label_charge)
        .on("tick",redrawLabels);



    if(highlight && highlight_index){

        //aggiunge i cerchi concentrici
        //e le linee di connessione fra i punti
        var highlight_marker=[];
        connection_lines=[];
        var highlight_x = parseFloat(coordinate[highlight_index][1]),
            highlight_y = parseFloat(coordinate[highlight_index][2]);


        for(var k =0; k< circles_sizes.length; k++){
            highlight_marker[k]= {
                label: "nick",
                x: highlight_x,
                y: highlight_y,
                size:circles_sizes[k]*fattore_scala_cerchi,
                color: "#"+circles_colors[k]

            };
        }

        for(var k=0; k<val_array.length;k++){
            connection_lines[k]={
                x1:highlight_x,
                y1:highlight_y,
                x2:val_array[k].x,
                y2:val_array[k].y
            };
        }

        vis.
        selectAll(".anchor").
        data(highlight_marker).
        enter().
        append("circle").
        attr("r",function(d){
                return d.size;
            }).
        attr("cx",function(d) { return x(d.x)}).
        attr("cy",function(d) { return y(d.y)}).
        attr("fill", function(d){ return d.color;});

        //disegna le linee di connessione fra il punto di highlight e gli altri punti
        vis.selectAll().
            data(connection_lines).
            enter().
            append("line").
            attr("x1",function(d) { return x(d.x1);}).
            attr("y1",function(d) { return y(d.y1);}).
            attr("x2",function(d) { return x(d.x2);}).
            attr("y2",function(d) { return y(d.y2);}).
            attr("class","connection-line");


        if(marker){
            //TODO: determina il verso del marker a seconda della posizione
            // rispetto ai bordi del grafico


            //aggiunge il marker sul punto di interesse
            //calcolando il punto secondo i delta x e y che spostano l'immagine
            //per far coincidere il punteruolo con il punto highlight
            var user_marker_x, user_marker_y;
            user_marker_x = x(highlight_x)-user_marker_delta_x;
            user_marker_y = y(highlight_x)-user_marker_delta_y;

            vis.append("svg:image")
                .attr("xlink:href", "/static/img/grafico/user_marker.png")
                .attr("x",user_marker_x)
                .attr("y",user_marker_y)
                .attr("width", user_marker_w)
                .attr("height", user_marker_h);


        }
    }

    var anchors = vis
        .selectAll(".anchor")
        .data(val_array,function(d,i) { return i});

    //disegna il marker partito fatto da 3 cerchi concentrici
    anchors.enter().
        append("circle").
        attr("r",outer_dotsize).
        attr("cx",function(d) { return x(d.x);}).
        attr("cy",function(d) { return y(d.y);}).
        attr("fill", function(d){
            var new_color=ColorLuminance(d.color,0.6);
            return "rgba("+hexToRgb(new_color).r+","+hexToRgb(new_color).g+","+hexToRgb(new_color).b+","+0.5+")";
        })

    anchors.enter().
        append("circle").
        attr("r",middle_dotsize).
        attr("cx",function(d) { return x(d.x);}).
        attr("cy",function(d) { return y(d.y);}).
        attr("fill", function(d){
            var new_color=ColorLuminance(d.color,-0.6);
            return "rgba("+hexToRgb(new_color).r+","+hexToRgb(new_color).g+","+hexToRgb(new_color).b+","+0.7+")";

        })

    anchors.enter().
        append("circle").
        attr("r",inner_dotsize).
        attr("cx",function(d) { return x(d.x);}).
        attr("cy",function(d) { return y(d.y);}).
        attr("fill", function(d){return d.color;})


    anchors.transition()
        .delay(function(d,i) { return i*10;})
        .duration(10)
        .attr("cx",function(d) { return x(d.x);})
        .attr("cy",function(d) { return y(d.y);})

    // Now for the labels
    anchors.call(labelForce.update)  //  This is the only function call needed, the rest is just drawing the labels

    var labels = vis.selectAll(".labels").data(val_array,function(d,i) { return i})

    // Draw the labelbox, caption and the link
    var newLabels = labels.enter().append("g").attr("class","labels")

    var newLabelBox = newLabels.append("g").attr("class","labelbox")
    newLabelBox.append("text").attr("class","labeltext").attr("y",6)

    newLabels.append("line").attr("class","link")

    labelBox = vis.selectAll(".labels").selectAll(".labelbox")
    links = vis.selectAll(".link")
    labelBox.selectAll("text").text(function(d) { return d.label;;})

}


//funzione che ridisegna le label e i link tra label e punti
function redrawLabels() {
    labelBox
        .attr("transform",function(d) { return "translate("+d.labelPos.x+" "+d.labelPos.y+")"})

    links
        .attr("x1",function(d) { return d.anchorPos.x})
        .attr("y1",function(d) { return d.anchorPos.y})
        .attr("x2",function(d) { return d.labelPos.x})
        .attr("y2",function(d) { return d.labelPos.y})


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
    // fire off the request to the set url
    var request = $.ajax({
        url: url,
        type: "post",
        data: data

    });

    // callback handler that will be called on success
    request.done(function (response, textStatus, jqXHR){
        draw_graph(response);
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
