int lumaPower = 2500;
float gamma = 1 / 1;

float bgColor = 0;

int kernelWidth = 151;
float[][] kernelArr = new float[kernelWidth][kernelWidth];

PImage oImg;
PGraphics borderImg;
float[][] imgArray = new float[1024 + (kernelWidth - 1)][1024 + (kernelWidth - 1)];
float[][] convArray = new float[1024][1024];

PImage convImg;

void setup() {
  size(1024, 1024, P2D);
  surface.setLocation(100, 100);
  
  //loading the image to convolve
  oImg = loadImage("line-chart.png");
}

void draw() {
  // make the convolution calculations
  makeKernel();
  makeImgArray();
  convolve();

  //display the convolved image
  image(convImg, 0, 0);

  //print benchmark and stop looping
  println("Calculation time: " + millis() + " ms");
  noLoop();
  
  // save the image
  save("img/halation-.png");
}

// calculate the kernel
void makeKernel() {
  for (int y = 0; y < kernelWidth; y++) {
    for (int x = 0; x < kernelWidth; x++) {
      float kernelC = (kernelWidth - 1) / 2;
      float distC = dist(x, y, kernelC, kernelC);
      if (distC <= 1) {
        kernelArr[x][y] = lumaPower;
      } else {
        kernelArr[x][y] = lumaPower / pow(distC, 2);
      }
    }
  }
}

// convert the image to an array
void makeImgArray() {
  // create bordered image to accomodate the kernel
  int borderedSize = 1024 + (kernelWidth - 1);
  borderImg = createGraphics(borderedSize, borderedSize);
  borderImg.beginDraw();
  borderImg.background(bgColor);
  borderImg.image(oImg, (kernelWidth - 1) / 2, (kernelWidth - 1) / 2);
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
      float wParcel = 0;

      for (int k = 0; k < kernelArr.length; k++) {
        for (int l = 0; l < kernelArr.length; l++) {
          wParcel += imgArray[i+k][j+l] * kernelArr[k][l];
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
