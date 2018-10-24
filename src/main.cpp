#include <iostream>
#include <time.h>
#include <unistd.h>
#include <string.h>
#include "utils.h"
#include "merge.h"

using namespace std;

void logger(string description){
    timespec res;
    clock_gettime(CLOCK_REALTIME, &res);
    cout << res.tv_sec << " " << description.c_str() << " " << getpid() << endl;
}

void setup(Square square, Tiff output){
    int imageWidth = fabs( (square.DR.x - square.UL.x) / pixelWidth ) + 1;

    int imageLength = fabs( (square.DR.y - square.UL.y) / pixelHeight ) + 1;

    TIFFSetField(output, TIFFTAG_IMAGEWIDTH     , imageWidth); 
    TIFFSetField(output, TIFFTAG_IMAGELENGTH    , imageLength);
    TIFFSetField(output, TIFFTAG_BITSPERSAMPLE  , 64);
    TIFFSetField(output, TIFFTAG_SAMPLEFORMAT   , 3);
    TIFFSetField(output, TIFFTAG_COMPRESSION    , 1);
    TIFFSetField(output, TIFFTAG_PHOTOMETRIC    , 1);
    TIFFSetField(output, TIFFTAG_SAMPLESPERPIXEL, 1);
    TIFFSetField(output, TIFFTAG_ROWSPERSTRIP   , 8);
    TIFFSetField(output, TIFFTAG_RESOLUTIONUNIT , 1);
    TIFFSetField(output, TIFFTAG_XRESOLUTION    , 1);
    TIFFSetField(output, TIFFTAG_YRESOLUTION    , 1);
    TIFFSetField(output, TIFFTAG_PLANARCONFIG   , PLANARCONFIG_CONTIG);

    ldouble line[imageWidth];
    
    for(register int i = 0; i < imageWidth; i++){
        line[i] = NaN;
    }
    
    for(register int i = 0; i < imageLength; i++){
        TIFFWriteScanline(output, line, i);
    }
}

Square getShape(ldouble x1, ldouble y1, ldouble x2, ldouble y2){
    Square square = {{x1, y1}, {x2, y2}};
    return square;
}

Square joinSquares(Square a, Square b){
    ldouble x_UL = min(a.UL.x, b.UL.x);
    ldouble y_UL = max(a.UL.y, b.UL.y);

    ldouble x_DR = max(a.DR.x, b.DR.x);
    ldouble y_DR = min(a.DR.y, b.DR.y);

    Square square = {{x_UL, y_UL}, {x_DR, y_DR}};
    return square;
}

int main(int argc, char *argv[]){

    // constants

    const int INPUT_BASE_INDEX[2] = {1, 4};
    const int INPUT_COORD_VALUES[2][2] = {{2, 3}, {5, 6}};

    const int OUTPUT_BASE_INDEX = 7;

    const string AUX_TIF = "aux.tif";

    // valid arguments
    
    if(argc != 8){
        cerr << "Arguments insufficients\n";
        exit(0);
    }

    // process input
    logger("process input");

    Tiff bases[2], output_base, output_read;
    Square squares[2], output_square;

    for(int i = 0; i < 2; i++){

        ldouble x1 = atof(argv[INPUT_COORD_VALUES[i][0]]);
        ldouble y1 = atof(argv[INPUT_COORD_VALUES[i][1]]);
        
        string path_tiff_base = argv[INPUT_BASE_INDEX[i]];
        bases[i] = TIFFOpen(path_tiff_base.c_str(), "rm");
        int width, length;

        TIFFGetField(bases[i], TIFFTAG_IMAGEWIDTH     , &width); 
        TIFFGetField(bases[i], TIFFTAG_IMAGELENGTH    , &length);
        
        squares[i] = getShape(x1, y1, x1 + width * pixelWidth, y1 - (length * pixelHeight));
    }

    // create output file
    logger("process output");

    output_base = TIFFOpen( argv[OUTPUT_BASE_INDEX], "w8m" );

    output_square = joinSquares(squares[0], squares[1]);

    setup(output_square, output_base);

    TIFFClose(output_base);

    // start merge

    logger("merge start");

    MergeTiff merge = MergeTiff(bases, argv[OUTPUT_BASE_INDEX], squares, output_square, AUX_TIF);
    merge.merge();
    return 0;
}
