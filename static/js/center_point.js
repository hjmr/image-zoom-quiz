let img;
let cnv;
let currPosX, currPosY;

// Pareters
let imageFilename = 'chewbacca.jpg';

function preload() {
    img = loadImage('/imgs/' + imageFilename);
}

function centering() {
    let x = (windowWidth - width) / 2;
    cnv.position(x, 120);
}

function setup() {
    cnv = createCanvas(img.width, img.height);
    cnv.parent('myCanvas');
    centering()
    currPosX = -1;
    currPosY = -1;
}

function draw() {
    let hw = img.width  / 2;
    let hh = img.height / 2;
    image(img, 0, 0);
    stroke(0);
    line(0, hh, width, hh);
    line(hw, 0, hw, height);
    stroke(255, 255, 0);
    line(0, mouseY, width, mouseY);
    line(mouseX, 0, mouseX, height);
    ellipse(mouseX, mouseY, 5, 5);
    if( 0 <= currPosX && 0 <= currPosY ) {
        stroke(0);
        ellipse(currPosX, currPosY, 10, 10);
    }
}

function windowResized() {
    centering();
}

function mouseClicked() {
    if( 0 <= mouseX && mouseX < width && 0 <= mouseY && mouseY < height ) {
        currPosX = mouseX;
        currPosY = mouseY;
        document.getElementById("posx").value = Math.round(currPosX - (img.width  / 2));
        document.getElementById("posy").value = Math.round(currPosY - (img.height / 2));
    }
}

function initParameters(imageFile) {
    imageFilename = imageFile;
}
