#include "merge.h"

MergeTiff::MergeTiff(Tiff _input_base[2], string _output_base_name, Square _input_square[2], Square _output_square, string _output_read_name){
    input_base[0] = _input_base[0];
    input_base[1] = _input_base[1];
    output_base_name = _output_base_name;
    input_square[0] = _input_square[0];
    input_square[1] = _input_square[1];
    output_square = _output_square;
    output_read_name = _output_read_name;
    
    intersect = MergeMeanFunction();
}

void MergeTiff::merge(){

    for(int i = 0; i < 2; i++){

        Tiff output_read, output_base;

        cout << "";
        if((i%2) == 0){
            output_read = TIFFOpen(output_base_name.c_str(), "rm");
            output_base = TIFFOpen(output_read_name.c_str(), "w8m");
        }else{
            output_read = TIFFOpen(output_read_name.c_str(), "rm");
            output_base = TIFFOpen(output_base_name.c_str(), "w8m");
            
        }

        int imageWidth = fabs( (output_square.DR.x - output_square.UL.x) / pixelWidth ) + 1;

        int imageLength = fabs( (output_square.DR.y - output_square.UL.y) / pixelHeight ) + 1;

        TIFFSetField(output_base, TIFFTAG_IMAGEWIDTH     , imageWidth); 
        TIFFSetField(output_base, TIFFTAG_IMAGELENGTH    , imageLength);
        TIFFSetField(output_base, TIFFTAG_BITSPERSAMPLE  , 64);
        TIFFSetField(output_base, TIFFTAG_SAMPLEFORMAT   , 3);
        TIFFSetField(output_base, TIFFTAG_COMPRESSION    , 1);
        TIFFSetField(output_base, TIFFTAG_PHOTOMETRIC    , 1);
        TIFFSetField(output_base, TIFFTAG_SAMPLESPERPIXEL, 1);
        TIFFSetField(output_base, TIFFTAG_ROWSPERSTRIP   , 1);
        TIFFSetField(output_base, TIFFTAG_RESOLUTIONUNIT , 1);
        TIFFSetField(output_base, TIFFTAG_XRESOLUTION    , 1);
        TIFFSetField(output_base, TIFFTAG_YRESOLUTION    , 1);
        TIFFSetField(output_base, TIFFTAG_PLANARCONFIG   , PLANARCONFIG_CONTIG);
        
        ldouble line[imageWidth];
        for(register int z = 0; z < imageLength; z++){
            TIFFReadScanline(output_read, line, z);
            TIFFWriteScanline(output_base, line, z);
        }

        int output_width = imageWidth;
        int output_length = imageLength;

        int input_width, input_length;
        TIFFGetField(input_base[i], TIFFTAG_IMAGEWIDTH, &input_width);
        TIFFGetField(input_base[i], TIFFTAG_IMAGELENGTH, &input_length);

        uint16 input_byte;

        TIFFGetField(input_base[i], TIFFTAG_SAMPLEFORMAT, &input_byte);
        tdata_t input_line = _TIFFmalloc(TIFFScanlineSize(input_base[i]));

        PixelReader pixel_read_input = PixelReader(input_byte, TIFFScanlineSize(input_base[i]) / input_width, input_line);

        int offsetX = fabs((input_square[i].UL.x - output_square.UL.x) / pixelWidth);   
        int offsetY = fabs((input_square[i].UL.y - output_square.UL.y) / pixelHeight);

        ldouble write_line[output_width];     

        for(register int j = 0; j < input_length; j++){
            
            TIFFReadScanline(output_read, write_line, j + offsetY);
            TIFFReadScanline(input_base[i], input_line, j);

            for(register int k = 0; k < output_width; k++){
                if(k >= offsetX && (k - offsetX) < input_width){
                    ldouble pix = intersect(pixel_read_input.readPixel(k - offsetX), write_line[k]);
                    write_line[k] = pix;
                }
            }

            TIFFWriteScanline(output_base, write_line, j + offsetY);
        }
        TIFFClose(output_read);
        TIFFClose(output_base);
        TIFFClose(input_base[i]);
        _TIFFfree(input_line);
    }

}