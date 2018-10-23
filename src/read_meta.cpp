#include "read_meta.h"

string ReadMeta::search(string filter){
    ifstream in(path_meta_file);
    string line;
    bool flag = false;
    while(getline(in, line)){
        stringstream lineReader(line);
        string token;
        vector<string> nline;
        while(lineReader >> token){
            if(token == filter) 
                flag = true;
            if(flag) 
                nline.push_back(token);
        }
        if(flag) 
            return nline[2];
    }
}

Square ReadMeta::getShape(){
    ldouble x1 = atof( search("CORNER_UL_PROJECTION_X_PRODUCT").c_str() );
    ldouble y1 = atof( search("CORNER_UL_PROJECTION_Y_PRODUCT").c_str() );

    ldouble x2 = atof( search("CORNER_LR_PROJECTION_X_PRODUCT").c_str() );
    ldouble y2 = atof( search("CORNER_LR_PROJECTION_Y_PRODUCT").c_str() );

    Square square = {{x1, y1}, {x2, y2}};

    return square;
}