let origImage;
let origAratio;

// timeout control
let running;
let wating_timeout;
let finished;

// Animation Speed
let interval = 0.05 * 1000; // 0.05sec

// Parameters
let sizeRatio = 50;
let sizeRatioStep = 1;
let centerOffset = {x:0, y:0};
let centerOffsetStep = {x:0, y:0};
let imageFilename = 'chewbacca.jpg';

function calcCanvasSize() {
    let cnvWidth, cnvHeight;
    let aratio = windowWidth / windowHeight;
    if( aratio < origAratio ) {
        cnvWidth  = windowWidth;
        cnvHeight = cnvWidth * origImage.height / origImage.width;
    } else {
        cnvHeight = windowHeight;
        cnvWidth  = cnvHeight * origImage.width / origImage.height;
    }
    let cnvSize = {width:cnvWidth, height:cnvHeight};
    return cnvSize;
}

function preload() {
    origImage = loadImage('/imgs/' + imageFilename);
    origAratio = origImage.width / origImage.height;
}

function setup() {
    cnvSize = calcCanvasSize();
    let cnv = createCanvas(cnvSize.width, cnvSize.height);
    cnv.parent("myCanvas")
    running = false;
    waiting_timeout = false;
    finished = false;
}

function windowResized() {
    cnvSize = calcCanvasSize();
    resizeCanvas(cnvSize.width, cnvSize.height);
}

function draw() {
    let w = origImage.width / sizeRatio;
    let h = origImage.height / sizeRatio;
    let x = (origImage.width  - w) / 2 + centerOffset.x;
    let y = (origImage.height - h) / 2 + centerOffset.y;
    image(origImage, 0, 0, width, height, x, y, w, h);
}

function mouseClicked() {
    if( finished ) {
        location.href="/";
    } else {
        if( running ) {
            running = false;
        } else {
            running = true;
        }

        if( running && !waiting_timeout ) {
            setTimeout(timed_zoom, interval);
            waiting_timeout = true;
        }
    }
}

function toggleRunning() {
    running = (running == true) ? false : true;
}

function timed_zoom() {
    if( 1 < sizeRatio ) {
        sizeRatio *= sizeRatioStep;
        centerOffset.x -= centerOffsetStep.x;
        centerOffset.y -= centerOffsetStep.y;
    } else if( sizeRatio < 1 ) {
        sizeRatio = 1;
        centerOffset.x = centerOffset.y = 0;
        finished = true;
    }

    if( running ) {
        setTimeout(timed_zoom, interval);
    } else {
        waiting_timeout = false;
    }
}

function initParameters(imageFile, duration, initialSizeRatio, initialCenterOffset) {
    let n = duration / interval;
    sizeRatio = initialSizeRatio;
    sizeRatioStep = 1 / Math.pow(initialSizeRatio, 1.0 / n);
    centerOffset.x = initialCenterOffset.x;
    centerOffset.y = initialCenterOffset.y;
    centerOffsetStep.x = initialCenterOffset.x / n;
    centerOffsetStep.y = initialCenterOffset.y / n;
    imageFilename = imageFile;
}
