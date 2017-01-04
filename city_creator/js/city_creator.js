var bg;
var places = [];
var size_of_objects = 10;

var opened = false;
var saver_inited = false;
var tmp_x, tmp_y = 0;

var last_len = places.length;

function setup() {
  frameRate(5);
  $('#reset').on('click', function(){
    console.log('xD');
    places = [];
    last_len = places.length;
    localStorage.clear();
    $('#json_file').text('');
});
  bg = loadImage("stare_miasto_krakow.png");
  var canvas = createCanvas(1000, 1422);
  canvas.parent('sketch-holder');
  
  if(localStorage.length > 0){
    for (var n = 0; n < localStorage.length; n++){
      places.push(JSON.parse(localStorage.getItem(n)));
    }
    console.log('READED FROM LOCAL');
  }
}

function draw() { 
  background(bg);
  for(var p = 0; p < places.length; p++){
    fill(0);
    ellipse(places[p].x, places[p].y, size_of_objects, size_of_objects);
  }
  
  if (last_len < places.length){ 
    $('#json_file').text(JSON.stringify(places, null, '\t'));
    last_len = places.length;
  }
}

const opt = {
              autoOpen: false,
              show: {
                  effect: "blind",
                  duration: 100
              },
              hide: {
                  effect: "blind",
                  duration: 100
              },
              close: function(event, ui){
                
                console.log('CLOSEING!');
                opened = false; }
            };

function mouseMoved() {
  $('.toDelete').remove();
  for(var p=0; p<places.length; p++){
    if(abs(places[p].x - mouseX) < size_of_objects && abs(places[p].y - mouseY) < size_of_objects){
              var x = mouseX + 'px';
              var y = mouseY + 'px';
              var tmplace = places[p];
              var span = $('<p>').html('Type: '+tmplace.type+'<br />'+   
                                          'Name: '+tmplace.name+'<br />'+
                                          'Capacity: '+ tmplace.capaticy+'<br />'+
                                          'Popularity: '+ tmplace.popularity+'<br />'+
                                          'x: '+tmplace.x+'<br />'+
                                          'y: '+tmplace.y+'<br />'+
                                          'x_m: '+tmplace.x_m+'<br />'+
                                          'x_y: '+tmplace.y_m+'<br />'+
                                          'Open Form: '+tmplace.open_from+'<br />'+
                                          'Open To: '+tmplace.open_to+'<br />'+
                                          'VisitTime: '+tmplace.visittime+'<br />');
              var div = $('<div>').css({
                  "position": "absolute",                    
                  "left": x,
                  "top": y,
              }).addClass('toDelete').addClass('indialog');
              div.append(span);
              $(document.body).append(div);    
    }
  }
}




function mouseClicked() {
  if(!opened){
    if(mouseX >= 0 && mouseX <= width){
      if(mouseY >= 0 && mouseY <= height){
        tmp_x = mouseX;
        tmp_y = mouseY;
        
        console.log('OPENING');
        $("#dialog").dialog(opt).dialog("open");
        opened = true;
        
        if (!saver_inited){
          saver();
          saver_inited = true;
        }
      }
    }
  }
  return false;
}

function saver() {
  $('.save').on('click', function(){
          console.log('SAVING!');
          places.push({
            type: $( "#myselect option:selected" ).text(),
            x_m: floor((tmp_x*590*2)/1000),
            y_m: floor((tmp_y*590*2)/1000),
            x: floor(tmp_x),
            y: floor(tmp_y),
            name: $('.name').val(),
            capaticy: $('.capacity').val(),
            popularity: $('.popularity').val(),
            open_from: $('.open_from').val(),
            open_to: $('.open_to').val(),
            visittime: $('.visittime').val()
          });
  
          $("#dialog").dialog(opt).dialog("close");
          tmp_x = 0;
          tmp_y = 0;
  });
}

window.onbeforeunload = confirmExit;
function confirmExit(){
    for (var n = 0; n<places.length; n++){
      localStorage.setItem(n, JSON.stringify(places[n]));
    }
    return false;
}