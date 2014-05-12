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

var label_charge = -120;
//lunghezza massima in px dei link fra punti e label
var link_len =30;
//dimensioni del contenitore del grafico sulla pagina html
var graph_container_width = 512,
    graph_container_height = 290;
var graph_aspect_ratio = graph_container_width/graph_container_height;

//dimensione del quadrato in cui verranno posizionati i punti
var graph_size=graph_container_height;
var graph_offset_x;
var fattore_scala_offset = 0.6;


//ratio del bordo del grafico relativo alla width del container
var graph_margin_ratio_x = 19.85;
var graph_margin_ratio_y = 24.78;
var graph_margin_bottom = 28.5;
var max_outputx,min_outputx, max_outputy,min_outputy,max_label_len=0;
var max_outputx_square,min_outputx_square, max_outputy_square,min_outputy_square;

//dimensioni del marker utente
var user_marker_size=20;
var user_marker_stroke=10;
var user_marker_color="#8430a6";
var user_marker_transparency=1;
var user_label_font_size="14";

//fattore_scala_cerchi permette di scalare i cerchi concentrici
//sullo sfondo del grafico
var fattore_scala_cerchi=0.29;
//anchor size
var inner_dotsize=4;
var middle_dotsize=inner_dotsize+1;
var outer_dotsize=inner_dotsize+4;

var default_party_color="#aaaaaa";
//dimensioni e colori dei cerchi concentrici
var circles_sizes=[1000,695,488,336,232,166,112,78,52];
var circles_transparency=0.5;
var circles_colors=["f3f9f7","e9f3f0","e0ede8","d6e8e0","cee3d9","c5ddd4","bed8cd","b5d4c8","afcfc2"];
var connection_lines;


//controlla che il browser supporti D3, viceversa mostra un div di errore
function browser_check(){
//    var isIE8 = $.browser.msie && +$.browser.version <= 8;
//
//    if ( isIE8==true ) {
//        $("#browser_issue").show();
//        return false;
//    }
//    else{
//        return true;
//    }

return true;

}

//resize graph, avatar and avatar pos based on browser viewport

function resize(){

    //gets graph size and set graph height

    var chart = $("#"+graph_div+"");
    graph_container_width = chart.width();
    graph_container_height =  Math.floor( graph_container_width / graph_aspect_ratio);

    var graph_style = "height:"+graph_container_height+"px; ";
    graph_style+="padding-top:"+Math.floor(graph_container_width/graph_margin_ratio_x)+"px; ";
    graph_style+="padding-left:"+Math.floor(graph_container_width/graph_margin_ratio_y)+"px; ";
    graph_style+="padding-right:"+Math.floor(graph_container_width/graph_margin_ratio_y)+"px; ";
    graph_style+="padding-bottom:"+Math.floor(graph_container_width/graph_margin_bottom)+"px; ";
    chart.attr("style", graph_style);

    //dimensione del quadrato in cui verranno posizionati i punti
    graph_size=graph_container_height;

    //offset x fra il contenitore del grafico e il grafico stesso
    graph_offset_x=(graph_container_width-graph_size)/2;

    if (graph_container_width < 300) {
        label_charge = -40;
        link_len =10;
        label_font_size = 10;
        user_label_font_size = 12;

    }

}


function draw_graph(coordinate, highlight, marker){

    var label_array = new Array();
    var val_array=[];
    var max_label_len= 0, longest_label=0;
    var highlight_index=null;

    //trova la label con piu' caratteri
    for(var i=1; i< coordinate.length; i++)
        if(coordinate[i][0].length> longest_label)
            {
                longest_label=coordinate[i][0].length;
            }

    //calcola la lunghezza massima della label in px
    max_label_len=longest_label*label_font_size;


    //calcola xy max e min per i cerchi di sfondo
    max_outputx_square = graph_size-(outer_dotsize+link_len+(max_label_len/2))+graph_offset_x;
    min_outputx_square = (outer_dotsize+link_len+(max_label_len/2))+graph_offset_x;
    max_outputy_square = graph_size-(outer_dotsize+link_len+label_font_size);
    min_outputy_square = (outer_dotsize+link_len+label_font_size);


    //funzione di scala fra input e output per i cerchi di sfondo
    var x_square = d3.scale.linear().domain([ minvalx, maxvalx]).range([min_outputx_square, max_outputx_square]),
        y_square = d3.scale.linear().domain([ minvaly, maxvaly]).range([min_outputy_square, max_outputy_square]);


    for (var i=0; i < coordinate.length; i++) {

        //se trova l'elemento da evidenziare si salva l'indice nel vettore
        if(highlight && coordinate[i][0].toUpperCase()===highlight.toUpperCase())
            highlight_index=i;

        // trova il colore associato al partito analizzato
        for (var sigla in partiti) {

            if(coordinate[i][0] == sigla)
                var color = partiti[sigla].colore;
        }
        //if party was not found, set a default color
        if(color=="")
            color=default_party_color;

        if(coordinate[i][0]!="user"){

            val_array[i] = {
                label: coordinate[i][0],
                x: parseFloat(coordinate[i][1]),
                y: parseFloat(coordinate[i][2]),
                size: inner_dotsize,
                fontsize: label_font_size,
                color:color
            };
        }
        else{
            //adds a user marker point, small dot marker of transparent color
            val_array[i] = {
                label: utente.nickname,
                x: parseFloat(coordinate[i][1]),
                y: parseFloat(coordinate[i][2]),
                size: 0.001,
                fontsize: user_label_font_size,
                color:null
            };
        }

        color="";
    }

    vis = d3.select("#"+graph_div+"")
        .data([val_array])
        .append("svg:svg")
        //following lines are for the responsiveness of the graph
        .attr("viewBox", "0 0 " + graph_container_width + " " + graph_container_height)
        .attr("preserveAspectRatio", "xMidYMid meet")
        .attr("id", "grafico_svg");


//    // Initialize the label-forces
    var labelForce = d3.force_labels()
        .linkDistance(3.0)
        .gravity(0)
        .nodes([]).links([])
        .charge(label_charge)
        .on("tick",redrawLabels);


    if(highlight && highlight_index!=null){

        //aggiunge i cerchi concentrici

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

        vis.
            selectAll(".anchor").
            data(highlight_marker).
            enter().
            append("circle").
            attr("r",function(d){
                return d.size;
            }).
            attr("cx",function(d) { return x_square(d.x);}).
            attr("cy",function(d) { return y_square(d.y);}).
            attr("fill", function(d){
                return "rgba("+hexToRgb(d.color).r+","+hexToRgb(d.color).g+","+hexToRgb(d.color).b+","+circles_transparency+")";
            });

        //aggiunge le linee di connessione fra i punti
        for(var k=0; k<val_array.length;k++){
            connection_lines[k]={
                x1:highlight_x,
                y1:highlight_y,
                x2:val_array[k].x,
                y2:val_array[k].y
            };
        }


        //disegna le linee di connessione fra il punto di highlight e gli altri punti
        vis.selectAll().
            data(connection_lines).
            enter().
            append("line").
            attr("x1",function(d) { return x_square(d.x1);}).
            attr("y1",function(d) { return y_square(d.y1);}).
            attr("x2",function(d) { return x_square(d.x2);}).
            attr("y2",function(d) { return y_square(d.y2);}).
            attr("class","connection-line");

    }


        var anchors = vis
        .selectAll(".anchor")
        .data(val_array,function(d,i) { return i});

    //disegna il marker partito fatto da 3 cerchi concentrici
    anchors.enter().
        append("circle").
        attr("r",function(d) { return d.size+4;}).
        attr("cx",function(d) { return x_square(d.x);}).
        attr("cy",function(d) { return y_square(d.y);}).
        attr("fill", function(d){
            if(d.color!=null){
                var new_color=ColorLuminance(d.color,0.6);
                return "rgba("+hexToRgb(new_color).r+","+hexToRgb(new_color).g+","+hexToRgb(new_color).b+","+0.5+")";
            }
        });

    anchors.enter().
        append("circle").
        attr("r",function(d) { return d.size+2;}).
        attr("cx",function(d) { return x_square(d.x);}).
        attr("cy",function(d) { return y_square(d.y);}).
        attr("fill", function(d){
            if(d.color!=null){
                var new_color=ColorLuminance(d.color,-0.6);
                return "rgba("+hexToRgb(new_color).r+","+hexToRgb(new_color).g+","+hexToRgb(new_color).b+","+0.7+")";
            }
        });

    anchors.enter().
        append("circle").
        attr("r",function(d) { return d.size;}).
        attr("cx",function(d) { return x_square(d.x);}).
        attr("cy",function(d) { return y_square(d.y);}).
        attr("fill", function(d){
            if(d.color!=null){
                return d.color;
            }
        });


    if(highlight && highlight_index!=null && marker){

        //aggiunge il marker sul punto di interesse

        var user_marker_x, user_marker_y;
        var padding = Math.floor(user_marker_size / 2);
        user_marker_x = x_square(highlight_x);
        user_marker_y = y_square(highlight_y);

        vis.append("image")
        .attr("xlink:href", "../img/omino.png")
        .attr("width", 16)
        .attr("height", 21)
        .attr("x",user_marker_x+10)
        .attr("y",user_marker_y+8);


        //disegna la croce
        vis.append("line")
            .attr("x1",user_marker_x+padding)
            .attr("y1",user_marker_y+padding)
            .attr("x2",user_marker_x-padding)
            .attr("y2",user_marker_y-padding)
            .style("stroke-miterlimit","10")
            .style("stroke", function(d){
                var new_color=user_marker_color;
                return "rgba("+hexToRgb(new_color).r+","+hexToRgb(new_color).g+","+hexToRgb(new_color).b+","+user_marker_transparency+")";
            })
            .style("stroke-width",user_marker_stroke+"px");

        vis.append("line")
            .attr("x1",user_marker_x-padding)
            .attr("y1",user_marker_y+padding)
            .attr("x2",user_marker_x+padding)
            .attr("y2",user_marker_y-padding)
            .style("stroke-miterlimit","10")
            .style("stroke", function(d){
                var new_color=user_marker_color;
                return "rgba("+hexToRgb(new_color).r+","+hexToRgb(new_color).g+","+hexToRgb(new_color).b+","+user_marker_transparency+")";
            })
            .style("stroke-width",user_marker_stroke+"px");

    }

    anchors.transition()
        .delay(function(d,i) { return i*10;})
        .duration(10)
        .attr("cx",function(d) { return x_square(d.x);})
        .attr("cy",function(d) { return y_square(d.y);});


    // Now for the labels
    anchors.call(labelForce.update);  //  This is the only function call needed, the rest is just drawing the labels

    var labels = vis.selectAll(".labels").data(val_array,function(d,i) { return i;});

    // Draw the labelbox, caption and the link
    var newLabels = labels.enter().append("g").attr("class","labels");

    var newLabelBox = newLabels.append("g").attr("class","labelbox");
    newLabels.append("line").attr("class","link");
    newLabelBox.append("text")
        .attr("class","labeltext")
        .attr("y",6)
        .style("font-size",function(d) { return ""+d['fontsize']+"px";})
        .text(function(d) { return d.label;});


    labelBox = vis.selectAll(".labels").selectAll(".labelbox");
    links = vis.selectAll(".link");

}


//funzione che ridisegna le label e i link tra label e punti
function redrawLabels() {


    labelBox
        .attr("transform",function(d) { return "translate("+d.labelPos.x+" "+d.labelPos.y+")";});

    links
        .attr("x1",function(d) { return d.anchorPos.x;})
        .attr("y1",function(d) { return d.anchorPos.y;})
        .attr("x2",function(d) { return d.labelPos.x;})
        .attr("y2",function(d) { return d.labelPos.y;});


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

    var nick = document.getElementById('nickname');
    var ml_email = document.getElementById('ml_email');
    var firstcheck, secondcheck;
    firstcheck=secondcheck=false;
    firstcheck=checkNick(nick.value);
    secondcheck=echeck(ml_email.value);


    if(firstcheck == false || secondcheck== false){
        if (firstcheck==false){
            nick.value="";
            nick.focus();
        }

        if (secondcheck==false){
            ml_email.value="";
            ml_email.focus();
        }
        return false;
    }
    else
    {
        return true;
    }


}

//returns the data struct that will be posted
function collect_data(){
    var data = {};
    var user_data={};
    data.answers = [];
    var answers, questionid;
    var i;

//  retrieves user answers
    for(i=1; i<=questions.length-1; i++)
    {
//        use the questions id as an index
        questionid = questions[i]['id'];
        if(document.getElementById("t"+questionid).value!='')
        {
            data.answers[""+questionid+""]=document.getElementById("t"+questionid).value;
        }

    }

//    retrieve user name and email
    user_data.name = document.getElementById('nickname').value;
    user_data.email = document.getElementById('ml_email').value;

    data.user_data = user_data;
    return data;
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
};

askPrev = function () {

	if( c == 1) {
		return;	
	}
	
	c--;
	
	refreshView();	
};

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
		return false;
	}
	if (str.length > 24) {
		alert ("Puoi usare al massimo 24 caratteri per il nome");
		return false;
	}
	
	return true;
}

function echeck(str) {

	var at="@";
	var dot=".";
	var lat=str.indexOf(at);
	var lstr=str.length;
	var ldot=str.indexOf(dot);
	var err_msg="Indirizzo email errato";
	
	// il campo non è obbligatorio
	if (str=="") return true
	
	if (str.indexOf(at)==-1){
	   alert(err_msg);
	   return false;
	}

	if (str.indexOf(at)==-1 || str.indexOf(at)==0 || str.indexOf(at)==lstr){
	   alert(err_msg);
	   return false;
	}

	if (str.indexOf(dot)==-1 || str.indexOf(dot)==0 || str.indexOf(dot)==lstr){
	   alert(err_msg);
	    return false;
	}

	 if (str.indexOf(at,(lat+1))!=-1){
	   alert(err_msg);
	    return false;
	 }

	 if (str.substring(lat-1,lat)==dot || str.substring(lat+1,lat+2)==dot){
	   alert(err_msg);
	    return false;
	 }

	 if (str.indexOf(dot,(lat+2))==-1){
	   alert(err_msg);
	    return false;
	 }
	
	 if (str.indexOf(" ")!=-1){
	   alert(err_msg);
	    return false;
	 }

	return true;
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
