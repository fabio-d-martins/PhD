int apertureRadius = 10;
float gamma = 1 / 2.2;
float lumaM = 100000;

int kernelWidth = (apertureRadius * 2) + 1;
float[][] kernelArr = new float[kernelWidth][kernelWidth];

PImage oImg;
PGraphics borderImg;
float[][] imgArray = new float[1024 + (apertureRadius * 2)][1024 + (apertureRadius * 2)];
float[][] convArray = new float[1024][1024];

PImage convImg;

void setup() {
  size(1024, 1024, P2D);
  surface.setLocation(100, 100);
}

void draw() {
  //loading the image to convolve
  oImg = loadImage("a.png");

  // make the convolution calculations
  makeKernel();
  makeImgArray();
  convolve();

  //display the convolved image
  image(convImg, 0, 0);

  //print benchmark and stop looping
  println(millis());
  noLoop();
}

// calculate the kernel
void makeKernel() {
  for (int y = 0; y < kernelWidth; y++) {
    for (int x = 0; x < kernelWidth; x++) {
      float cDist = dist(x, y, apertureRadius, apertureRadius);
      float distMult = map(cDist, 0, apertureRadius, 1, 0);
      if (distMult < 0) {
        distMult = 0;
      }
      if (cDist > 1) {
        float luma = pow(sinc(cDist * 5), 2) * lumaM;
        if (luma > 1) {
          luma = 1;
        }
        kernelArr[y][x] = luma;
      } else {
        kernelArr[y][x] = 1;
      }
    }
  }
}

// convert the image to an array
void makeImgArray() {
  // create bordered image to accomodate the kernel
  int borderedSize = 1024 + (apertureRadius * 2);
  borderImg = createGraphics(borderedSize, borderedSize);
  borderImg.beginDraw();
  borderImg.background(255, 255, 255);
  borderImg.image(oImg, apertureRadius, apertureRadius);
  borderImg.endDraw();

  // populate the array with the image values, normalized to 1
  for (int i = 0; i < borderImg.width; i++) {
    for (int j = 0; j < borderImg.height; j++) {
      imgArray[i][j] = red(borderImg.pixels[i + j * borderImg.width]) / 255;
    }
  }
}

// convolve the image with the kernel
void convolve() {
  // set the weights for the convolution sum
  float convWeight = kernelWidth * kernelWidth;

  // convolve the kernel with the image
  for (int i = 0; i < convArray.length; i++) {
    for (int j = 0; j < convArray.length; j++) {
      float wParcel = 0.0;

      for (int k = 0; k < kernelArr.length; k++) {
        for (int l = 0; l < kernelArr.length; l++) {
          float imgArrayValue = imgArray[i+k][j+l];
          float kernelArrValue = kernelArr[k][l];
          float convValue = imgArrayValue * kernelArrValue;
          wParcel = wParcel + convValue;
        }
      }
      convArray[i][j] = wParcel / convWeight;
    }
  }

  // convert convolved image from array to image
  convImg = createImage(1024, 1024, RGB);

  convImg.loadPixels();
  for (int x = 0; x < convImg.width; x++) {
    for (int y = 0; y < convImg.height; y++) {
      int loc = x + (y * width);
      float colorFromMatrix = pow(convArray[x][y], gamma);
      convImg.pixels[loc] = color(colorFromMatrix * 255);
    }
  }
  convImg.updatePixels();
}

float sinc(float dist) {
  float result = (sin(dist) / dist) * 1.0;
  return result;
}
