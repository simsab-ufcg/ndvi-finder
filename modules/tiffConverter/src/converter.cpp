#include "tiffio.h"
#include <iostream>
#include "pixelReader.h"

using namespace std;

void setup(TIFF* output, TIFF* base){
    uint32 imageWidth, imageLength;

    TIFFGetField(base, TIFFTAG_IMAGEWIDTH,      &imageWidth);
    TIFFGetField(base, TIFFTAG_IMAGELENGTH,     &imageLength);
    
    TIFFSetField(output, TIFFTAG_IMAGEWIDTH     , imageWidth); 
    TIFFSetField(output, TIFFTAG_IMAGELENGTH    , imageLength);
    TIFFSetField(output, TIFFTAG_BITSPERSAMPLE  , 64);
    TIFFSetField(output, TIFFTAG_SAMPLEFORMAT   , 3);
    TIFFSetField(output, TIFFTAG_COMPRESSION    , 1);
    TIFFSetField(output, TIFFTAG_PHOTOMETRIC    , 1);
    TIFFSetField(output, TIFFTAG_SAMPLESPERPIXEL, 1);
    TIFFSetField(output, TIFFTAG_ROWSPERSTRIP   , 1);
    TIFFSetField(output, TIFFTAG_RESOLUTIONUNIT , 1);
    TIFFSetField(output, TIFFTAG_XRESOLUTION    , 1);
    TIFFSetField(output, TIFFTAG_YRESOLUTION    , 1);
    TIFFSetField(output, TIFFTAG_PLANARCONFIG   , PLANARCONFIG_CONTIG);
}

int main(int argc, char* argv[]){
    TIFF* tif;
    TIFF* outputTiff;

    cerr << "Opening " << string(argv[1]) << endl;
    
    tif = TIFFOpen(argv[1], "rm");
    outputTiff = TIFFOpen(argv[2], "w8m");

    // Could not open tiff file
    if(!tif) return 1;

    uint16 sample_band;
    uint32 width, height, tileWidth, tileLength;

    TIFFGetField(tif, TIFFTAG_TILEWIDTH, &tileWidth);
    TIFFGetField(tif, TIFFTAG_TILELENGTH, &tileLength);

    TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
    TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
    TIFFGetField(tif, TIFFTAG_SAMPLEFORMAT, &sample_band);

    setup(outputTiff, tif);

    cout << "height: " << height << " / width: " << width << endl;
    cout << "tileLength: " << tileLength << " / tileWidth: " << tileWidth << endl;
    cout << "tiffTileSize: " << TIFFTileSize(tif) << endl;

    cout << "yo" << endl;
    tdata_t buf;
    unsigned short byte_size = TIFFTileSize(tif) / (tileWidth * tileLength);
    buf = _TIFFmalloc(TIFFTileSize(tif));
    cout << "yo2" << endl;

    int tileCounter;

    cout << "tileLength: " << tileLength << " / width: " << width << endl;
    double loadedData[tileLength][width];

    cout << "yo3" << endl;
    PixelReader pixelReader = PixelReader(sample_band, byte_size, buf);
    cout << "yo4" << endl;

    for(int i = 0; i < height; i += tileLength) {
        tileCounter = 0;
        for(int j = 0; j < width; j += tileWidth) {
            TIFFReadTile(tif, buf, j, i, 0, 0);
            
            int actualPosition = 0;
            for(int line = 0; line < tileLength; line++) {
                for(int column = 0; column < tileWidth; column++) {
                    double value = pixelReader.readPixel(actualPosition);
                    loadedData[line][column + (tileCounter * tileWidth)] = value;

                    actualPosition++;
                    cout << "actualPosition: " << actualPosition << endl;
                }
            }

            tileCounter++;
        }

        for(int line = 0; line < tileLength; line++) {
            TIFFWriteScanline(outputTiff, loadedData[line], line + i);
        }
    }

    TIFFClose(tif);
    TIFFClose(outputTiff);
    return 0;
}