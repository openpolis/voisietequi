var c = 0;
var chosed = 0;

askNext = function () {
	c++;

	if( c >= questions.length) {
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
	k_cnt.innerHTML = c;
	k_acc.innerHTML = questions[c].more ? questions[c].more : "";
	k_txt.innerHTML = questions[c].txt;
	k_inf.innerHTML = questions[c].inf;	


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
	b.style.display = "none"	;
	
	resetImgs();
	
	var cell = document.getElementById("t"+c);
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

chose = function (n) {
	var k_cho = document.getElementById("t"+c);
	k_cho.value = n;
	
	chosed = Math.max(c, chosed);
	
	askNext();
}

function validate() {

  var nick = document.getElementById('nickname')
  if (checkNick(nick.value)==false){
		nick.value=""
		nick.focus()
		return false    
  }

	var ml_email = document.getElementById('ml_email')
  if (echeck(ml_email.value)==false){
		ml_email.value=""
		ml_email.focus()
		return false;
	}
	
}

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
