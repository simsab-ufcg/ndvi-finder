#pragma once
#include "mergeMeanFunction.h"
#include <unistd.h>

struct MergeTiff{
    Tiff input_base[2];
    string output_base_name, output_read_name;

    Square input_square[2];
    Square output_square;

    MergeMeanFunction intersect;

    MergeTiff(Tiff _input_base[2], string _output_base_name, Square _input_square[2], Square _output_square, string _output_read_name);

    void merge();
};

