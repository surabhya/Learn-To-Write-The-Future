// url variables
var video_url_first = "<div id ='video'> <iframe width='1000px' height='500px' src='";
var video_url_last = "?autoplay=1&rel=0&controls=0' frameborder='10px' allowfullscreen> </iframe> </div>";
var playlist_url_last = "&amp;autoplay=1&amp;rel=0&amp;controls=0' frameborder='10px' allowfullscreen> </iframe> </div>"
var image_url_first = "<div class='image'> <img class='currentImage' width='1000px' height='500px' src='";
var image_url_last = "'/> </div>";

// json variables 
var quotes_json = [];
var images_json = [];
var videos_json = []; 
//count variables
var quote_count = 0; 
var playlist_count = 0; 

// function 

function getStarted(){
 	getData("http://www.computerscience-fisk.appspot.com/displayimages.json", "images");
	getData("http://www.computerscience-fisk.appspot.com/displayvideos.json", "videos");
	getData("http://www.computerscience-fisk.appspot.com/displayquotes.json", "quotes");
	setTimeout(function() {
		mainscreen();
	},2000)
}

var getData = function(URL, type){
	$.ajax({
		url: URL,
		dataType: 'json'
	}).done(function(data){
		if (type=="quotes"){
			quotes_json = data;
		} else if (type=="images"){
			images_json = data;
		} else {
			videos_json = data;
		}
	})

}

function time_int(time){
	var time_list = time.split(":");
	time =  ((parseInt(time_list[0]) * 60) + parseInt(time_list[1]))*1000  
	return time; 
}

function mainscreen(){
	var duration = time_int(videos_json[0].time); 
	$("#slideshow").empty().append( image_url_first + images_json[0].URL + image_url_last ); 
	  setTimeout(function() {
		  		$("#slideshow").empty().append(video_url_first + videos_json[0].URL + video_url_last); 
		  		setTimeout(function(){
		  			loadKhan();
		  		},duration); 
	  },5000);
  }


function loadKhan(){
	var duration = time_int(videos_json[1].time);
	$("#slideshow").empty().append( image_url_first + images_json[1].URL + image_url_last ); 
	setTimeout(function() {
		$("#slideshow").empty().append(video_url_first + videos_json[1].URL + video_url_last); 
		setTimeout(function(){
					$("#slideshow").empty().append( image_url_first + images_json[2].URL + image_url_last ); 
					quote_count = 0;
					playlist_count = 0;  
		  			loadQuotes();
		  		},duration); 
	},5000);
}


function slideshow(){
  if (quote_count >= quotes_json.length){
  		playlist_count +=1; 
  		clearInterval(loadQuotes);
  		if (playlist_count == 1){
  			$("#slideshow").empty().append( image_url_first + images_json[3].URL +  image_url_last ); 
  			setTimeout(function(){
  				loadplaylist()
  			},5000);
		}	
  } else {
  		image = quotes_json[quote_count % quotes_json.length].URL;
  		$(".currentImage").attr("src", image);
  		quote_count +=1;
  }
}

function loadQuotes(){
	setInterval(function(){ 
		slideshow();
	},5000); 
}


function loadplaylist(){ 
	var duration = time_int(videos_json[2].time); 
	$("#slideshow").empty().append(video_url_first + videos_json[2].URL + playlist_url_last); 
	setTimeout(function(){
		restart();
	},duration); 
}

function restart(){
	mainscreen()
}
