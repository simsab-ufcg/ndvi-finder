# echo "productId,path,row,download_url,cloudCover"   
#                     #  1        2           3              4        5               6                   7                   8          9        10       11     12             13     14          15        16      17          18           
# while IFS=,  read -r SCENE_ID PRODUCT_ID SPACECRAFT_ID SENSOR_ID DATE_ACQUIRED COLLECTION_NUMBER COLLECTION_CATEGORY SENSING_TIME DATA_TYPE WRS_PATH WRS_ROW CLOUD_COVER NORTH_LAT SOUTH_LAT WEST_LON EAST_LON TOTAL_SIZE BASE_URL
# do
#     if [ "$PRODUCT_ID" != "PRODUCT_ID" ]; then
#         if [ "$1" -le "$WRS_PATH" ] && [ "$WRS_PATH" -le  "$2" ]; then
#             if [ "$3" -le "$WRS_ROW" ] && [ "$WRS_ROW" -le "$4" ]; then
#                 echo "$PRODUCT_ID,$WRS_PATH,$WRS_ROW,$BASE_URL,$CLOUD_COVER"
#             fi
#         fi
#     fi
# done < /home/fmota/work_ndvi/xx/ndvi-finder/modules/index.csv

## 214 - 223
## 61 - 74
# 1 = scene_id
# 2 = product_id
# 10 = wrs_path
# 11 = wrs_row
# 12 = cloud_cover
# 18 = download_url
curl 'https://storage.googleapis.com/gcp-public-data-landsat/index.csv.gz' --output index.csv.gz
gunzip index.csv.gz

cut -d, -f1,10,11,12,18 index.csv | sed 's/gs:\/\//http:\/\/storage.googleapis.com\//g' | awk -F','  '{
    if($1 != "SCENE_ID") {
        if(214 <= $2 && $2 <= 223 && 61 <= $3 && $3 <= 74)
            print $1 "," $2 "," $3 "," $4 "," $5;
    } else {
        print "SCENE_ID,PATH,ROW,CLOUD_COVER,DOWNLOAD_URL"
    }
}' > scene_list