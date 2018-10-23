#pragma once
  
#include <vector>
#include <tiffio.h>
#include <math.h>
#include <algorithm>

using namespace std;

using ldouble = double;

using Tiff = TIFF*;

const ldouble EPS = 1e-7;
const ldouble NaN = -sqrt(-1.0);
const ldouble pixelWidth = 29.455668511;
const ldouble pixelHeight = 29.996139493;

typedef struct Point{
	ldouble x, y;
}Point;

typedef struct Square{
	Point UL, DR;
}Square;