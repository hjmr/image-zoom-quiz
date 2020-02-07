let img;

// Pareters
let imageFilename = 'chewbacca.jpg';

function preload() {
    img = loadImage('/imgs/' + imageFilename);
}

function setup() {
    let cnv = createCanvas(img.width, img.height);
    cnv.parent('myCanvas');
}

function draw() {
    image(img, 0, 0);
    line(0, mouseY, width, mouseY);
    line(mouseX, 0, mouseX, height);
    ellipse(mouseX, mouseY, 5, 5);
}

function mouseClicked() {

}

function initParameters(imageFile) {
    imageFilename = imageFile;
}
