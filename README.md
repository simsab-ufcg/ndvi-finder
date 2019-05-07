# Ndvi Finder
This project aims to produce a product of ndvi composed of several landsat scenes that can be separated in regions with their study periods considering the Brazilian semi-arid.

Note: It is possible to make modifications so that you can generate ndvi for areas outside the semi-arid territory.

# Build
For build this project execute script build using following code.

```
    sh build
```

# Configuration
To configure the project, you need to edit the `samples/semi-arid/time_range.csv` and `samples/semi-arid/path_row.txt` files. In `time_range.csv`, changing for each region its respective year and Julian day of the beginning and end of the study (rainy period + post rain) and the beginning of post-rain (for the algorithm to prioritize the best vegetation index pixels). For example, we have the following configuration:

```
REGION_NAME,START_DATE,END_DATE,START_POST_RAIN
MYREGION,2018 001,2018 091, 2018 070
```

In `path_row.txt`, you need to have the same regions added in` time_range.csv`, but now describing the path/rows of each landsat scene that makes up the region. For example, we have the following configuration:
```
MYREGION PATH01 ROW01 PATH02 ROW02 PATH03 ROW03 ...
```

Note: The configurations present in the code are correct to calculate the ndvi of the year 1986 of the Brazilian semi-arid.

# Run
To run the project use the following command:

```
python main.py run
```

# Additional Information
### Download landsat images

```
    python downloader.py download samples/semi-arid/path_row.txt samples/semi-arid/time_range.csv output/
```