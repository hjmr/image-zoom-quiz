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
    cnv.position(x, 50);
}

function setup() {
    cnv = createCanvas(img.width, img.height);
    cnv.parent('myCanvas');
    centering()
    currPosX = -1;
    currPosY = -1;
}

function draw() {
    image(img, 0, 0);
    line(0, mouseY, width, mouseY);
    line(mouseX, 0, mouseX, height);
    ellipse(mouseX, mouseY, 5, 5);
    if( 0 <= currPosX && 0 <= currPosY ) {
        ellipse(currPosX, currPosY, 10, 10);
    }
}

function windowResized() {
    centering();
}

function mouseClicked() {
    if( 0 <= mouseX && mouseX < width && 0 <= mouseY && mouseY < height ) {
        document.getElementById("posx").value = currPosX = Math.round(mouseX);
        document.getElementById("posy").value = currPosY = Math.round(mouseY);
    }
}

function initParameters(imageFile) {
    imageFilename = imageFile;
}
