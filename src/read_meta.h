#pragma once

#include <fstream>
#include <sstream>
#include "types.h"
#include <string.h>

using namespace std;

struct ReadMeta{
    string path_meta_file;

    ReadMeta(string _path_meta_file): path_meta_file(_path_meta_file) {};
    ReadMeta(){};

    string search(string filter);
    
    Square getShape();
};


