let img;

// Pareters
let imageFilename = 'chewbacca.jpg';

function calcCanvasSize() {
    let cnvWidth, cnvHeight;
    let aratio = windowWidth / windowHeight;
    if( aratio < origAratio ) {
        cnvWidth  = windowWidth;
        cnvHeight = cnvWidth / origAratio;
    } else {
        cnvHeight = windowHeight;
        cnvWidth  = cnvHeight * origAratio;
    }
    let cnvSize = {width:cnvWidth, height:cnvHeight};
    return cnvSize;
}

function preload() {
    img = loadImage('/imgs/' + imageFilename);
}

function setup() {
    cnvSize = calcCanvasSize();
    let cnv = createCanvas(cnvSize.width, cnvSize.height);
    cnv.parent('myCanvas');
}

function draw() {
    image(img, 0, 0);
    line(0, mouseY, width, mouseY);
    line(mouseX, 0, mouseX, height);
    ellipse(mouseX, mouseY, 5, 5);
}

function initParameters(imageFile) {
    imageFilename = imageFile;
}
