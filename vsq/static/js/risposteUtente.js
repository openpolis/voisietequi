var c = 0;
var chosed = 0;
var url="/mockup_answer";


//function that will visualize the response data
function visualize(response){

    alert(response);
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
    data.answers = [];
    data.user_data = [];
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
    var name = document.getElementById('nickname');
    var email = document.getElementById('ml_email');
//    data.user_data["name"]=name.value;
//    data.user_data["email"]=email.value;


    return data
}



askNext = function () {
	c++;

	if( c >= questions.length) {
//        se ho finito il questionario nasconde i div delle domande e mostra
//        la form per inserire nome e mail
		var askname = document.getElementById("modulo_risposte");
		var quests = document.getElementById("domanda");
		var pos = document.getElementById("posizioni");
		var pre = document.getElementById("tema_precedente");
		var suc = document.getElementById("tema_successivo");
		var leg = document.getElementById("legend");		
		askname.style.display = "block";
		quests.style.display = pos.style.display = pre.style.display = suc.style.display = leg.style.display = "none";		
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
    var next = document.getElementById("tema_successivo");
    var prev = document.getElementById("tema_precedente");

	if (c <= chosed) {
		next.style.display = "block";
	} else {
		next.style.display = "none";
	}
	
	if (c <= 1) {
		prev.style.display = "none";
	} else {
		prev.style.display = "block";		
	}
	
	b = document.getElementById("approfondimento");  
	b.style.display = "none";
	
	resetImgs();
	
	var cell = document.getElementById("t"+c);

//    nel caso l'utente abbia gia' risposto alla domanda C-esima cambia il colore del bottone della risposta
	if (cell.value != "") {
		var img1 = document.getElementById("ch"+cell.value);
		var img2 = document.getElementById("ch"+cell.value+"_dwn");		
		img1.style.display = "none";
		img2.style.display = "block";			
	}

//    cambia il colore dei quadratini che guidano il questionario
//  for (var i = 1; i < questions.length; i++) {
//    var led = document.getElementById('s'+i);
//    if (i == c) {
//      led.className = 'current';
//    } else if (i > chosed) {
//      led.className = 'to_do';
//    } else {
//      led.className = 'done';
//    }
//  }
	
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
		var img1 = document.getElementById("ch"+i);
		var img2 = document.getElementById("ch"+i+"_dwn");
		img1.style.display = "block";
		img2.style.display = "none";		
	}
}

function showhideApprofondimento(){
	b = document.getElementById("approfondimento");  
	if (b.style.display == "none"){
		b.style.display = "block";
	} else {
		b.style.display = "none";
	}
}

function firstTime(){

//    set the total n. of question on the page
    document.getElementById('nquestions').innerHTML = questions.length-1;
    askNext();
}
