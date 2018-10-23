#include <iostream>
#include <time.h>
#include <unistd.h>
#include <string.h>
#include "read_meta.h"
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

    const int INPUT_BASE_INDEX[2] = {1, 3};
    const int INPUT_MTL_INDEX[2] = {2, 4};

    const int OUTPUT_BASE_INDEX = 5;
    const int OUTPUT_MTL_INDEX = 6;

    const string AUX_TIF = "aux.tif";

    // valid arguments
    
    if(argc < 7 || argc > 7){
        cerr << "Arguments insufficients\n";
        exit(0);
    }

    // process input
    logger("process input");

    ReadMeta reader_mtl[2], output_mtl;
    Tiff bases[2], output_base, output_read;
    Square squares[2], output_square;

    for(int i = 0; i < 2; i++){
        string path_meta_file = argv[INPUT_MTL_INDEX[i]];
        reader_mtl[i] = ReadMeta(path_meta_file);
        squares[i] = reader_mtl[i].getShape();
        string path_tiff_base = argv[INPUT_BASE_INDEX[i]];
        bases[i] = TIFFOpen(path_tiff_base.c_str(), "rm");
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
