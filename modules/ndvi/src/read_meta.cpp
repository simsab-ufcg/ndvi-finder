#include "read_meta.h"
#include <string.h>

string ReadMeta::search(string filter){
    ifstream in(path_meta_file);
    if(!in.is_open() || !in){
        exit(5 << 3);
    }
    string line;
    bool flag = false;
    while(getline(in, line)){
        stringstream lineReader(line);
        string token;
        vector<string> nline;
        while(lineReader >> token){
            if(token == filter) flag = true;
            if(flag) nline.push_back(token);
        }
        if(flag) return nline[2];
    }
}

ldouble ReadMeta::getSunElevation(){
    string resultSearch = search("SUN_ELEVATION");
    return atof(resultSearch.c_str());
}

ldouble ReadMeta::getDistEarthSun(){
    string resultSearch = search("EARTH_SUN_DISTANCE");
    return atof(resultSearch.c_str());
}

int ReadMeta::getNumberSensor(){
    string resultSearch = search("LANDSAT_SCENE_ID");
    char number[1];
    strncpy(number, &resultSearch[3], 1);
    return atoi(number);
}