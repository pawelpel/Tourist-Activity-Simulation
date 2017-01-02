var bg;
var places = [];
var size_of_objects = 15;

var opened = false;
var saver_inited = false;
var tmp_x, tmp_y = 0;

var last_len = places.length;


function setup() {
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
            x_m: floor((tmp_x*590)/1000),
            y_m: floor((tmp_y*590)/1000),
            x: tmp_x,
            y: tmp_y,
            name: $('.name').val(),
            capaticy: $('.capaticy').val(),
            popularity: $('.popularity').val(),
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