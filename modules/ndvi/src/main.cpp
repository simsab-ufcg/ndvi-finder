#include <iostream>
#include <time.h>
#include <unistd.h>
#include <string.h>
#include "read_meta.h"
//#include "read_sun_earth.h"
#include "ndvi_generate.h"
#include "utils.h"

using namespace std;

void logger(string description){
    timespec res;
    clock_gettime(CLOCK_REALTIME, &res);
    cout << res.tv_sec << " " << description.c_str() << " " << getpid() << endl;
}

bool analisyShadow(Tiff band_bqa, int number_sensor){   
    int mask = setMask(number_sensor);
    
    uint16 sample_band_bqa;
    uint32 height_tiff_bqa, width_tiff_bqa;

    TIFFGetField(band_bqa, TIFFTAG_IMAGELENGTH, &height_tiff_bqa);
    TIFFGetField(band_bqa, TIFFTAG_IMAGEWIDTH, &width_tiff_bqa);
    TIFFGetField(band_bqa, TIFFTAG_SAMPLEFORMAT, &sample_band_bqa);

    tdata_t buf;
    unsigned short byte_size = TIFFScanlineSize(band_bqa)/width_tiff_bqa;
    buf = _TIFFmalloc(TIFFScanlineSize(band_bqa));

    long long quant_pixels_valid = 0;
    ldouble pixel;
    PixelReader prBqa = PixelReader(sample_band_bqa, byte_size, buf);

    for(int line = 0; line < height_tiff_bqa; line++){
        if(TIFFReadScanline(band_bqa, buf, line) < 0){
            exit(2 << 3);
        }
        for(int row = 0; row < width_tiff_bqa; row++){
            pixel = prBqa.readPixel(row);
            if(fabs(pixel - mask) <= EPS)quant_pixels_valid++;
        }
    }
    _TIFFfree(buf);
    
    return (((ldouble)quant_pixels_valid)/(height_tiff_bqa*width_tiff_bqa)) <= 0.01;
}

void setup(Tiff ndvi, Tiff bandBase){
    uint32 imageWidth, imageLength;

    TIFFGetField(bandBase, TIFFTAG_IMAGEWIDTH,      &imageWidth);
    TIFFGetField(bandBase, TIFFTAG_IMAGELENGTH,     &imageLength);
    
    TIFFSetField(ndvi, TIFFTAG_IMAGEWIDTH     , imageWidth); 
    TIFFSetField(ndvi, TIFFTAG_IMAGELENGTH    , imageLength);
    TIFFSetField(ndvi, TIFFTAG_BITSPERSAMPLE  , 64);
    TIFFSetField(ndvi, TIFFTAG_SAMPLEFORMAT   , 3);
    TIFFSetField(ndvi, TIFFTAG_COMPRESSION    , 1);
    TIFFSetField(ndvi, TIFFTAG_PHOTOMETRIC    , 1);
    TIFFSetField(ndvi, TIFFTAG_SAMPLESPERPIXEL, 1);
    TIFFSetField(ndvi, TIFFTAG_ROWSPERSTRIP   , 1);
    TIFFSetField(ndvi, TIFFTAG_RESOLUTIONUNIT , 1);
    TIFFSetField(ndvi, TIFFTAG_XRESOLUTION    , 1);
    TIFFSetField(ndvi, TIFFTAG_YRESOLUTION    , 1);
    TIFFSetField(ndvi, TIFFTAG_PLANARCONFIG   , PLANARCONFIG_CONTIG);
}

int main(int argc, char *argv[]){

    const int INPUT_BAND_RED_INDEX = 1;
    const int INPUT_BAND_NIR_INDEX = 2;
    const int INPUT_BAND_BQA_INDEX = 3;
    const int INPUT_BAND_MTL_INDEX = 4;
    const int OUTPUT_NAME_INDEX = 5;

    //valid arguments
    if(argc != 6){
        cerr << "Incorrect number of arguments for processing NDVI TIF";
        exit(0);
    }

    //load meta file
    string path_meta_file = argv[INPUT_BAND_MTL_INDEX];
    ReadMeta reader_meta = ReadMeta(path_meta_file);
    ldouble sun_elevation = reader_meta.getSunElevation();
    ldouble dist_sun_earth = reader_meta.getDistEarthSun();
    int number_sensor = reader_meta.getNumberSensor();
    //int julian_day = reader_meta.getJulianDay();
    //int year = reader_meta.getYear();

    //load distance between sun and earth
    //string path_d_sun_earth = "./src/d_sun_earth";
    //ReadSunEarth reader_sun_earth = ReadSunEarth(path_d_sun_earth);
    //ldouble dist_sun_earth = reader_sun_earth.getDistance(julian_day);

    //load band red (tiff)
    string path_tiff_band_red = argv[INPUT_BAND_RED_INDEX];
    Tiff band_red = TIFFOpen(path_tiff_band_red.c_str(), "rm");
    if(!band_red){
        exit(1 << 3);
    }
    //load band nir (tiff)
    string path_tiff_band_nir = argv[INPUT_BAND_NIR_INDEX];
    Tiff band_nir = TIFFOpen(path_tiff_band_nir.c_str(), "rm");
    if(!band_nir){
        exit(1 << 3);
    }

    //load band_bqa (tiff)
    string path_tiff_band_bqa = argv[INPUT_BAND_BQA_INDEX];
    Tiff band_bqa = TIFFOpen(path_tiff_band_bqa.c_str(), "rm");
    if(!band_bqa){
        exit(1 << 3);
    }

    //load tiff ndvi
    string path_output_tiff_ndvi = argv[OUTPUT_NAME_INDEX];
    Tiff ndvi = TIFFOpen(path_output_tiff_ndvi.c_str(), "w8m");
    if(!ndvi){
        exit(1 << 3);
    }
    setup(ndvi, band_red);

    logger("Preprocess");

    NDVIGenerate ndviGen(sun_elevation, band_red, band_nir, band_bqa);
    ndviGen.processNDVI(number_sensor, dist_sun_earth, ndvi);

    logger("NDVICalc");

    TIFFClose(band_red);
    TIFFClose(band_nir);
    TIFFClose(band_bqa);
    TIFFClose(ndvi);

    return 0;
}
