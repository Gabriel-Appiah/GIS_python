## Suitability Analysis, Using Arcpy Python Library
The study area for this project is the four counties (Cherokee, Plymouth, Ida, and Woodbury County) within the Iowa portion of Siouxland Interstate Metropolitan Planning Council. From Figure 2 the study area is located in the northwestern portion of the State of Iowa. Some of the counties bordering the study area include Union County, SD; Dakota County, NE; Monona, IA; Crawford, IA, Sac County, IA, among others. According to the 2010 decennial census, the total population of the study area was 146,319 in 2010, with 8.5% living in Cherokee County, 4.8% living in Ida County, 17.1% living in Plymouth County, and the remaining 69.8% living in Woodbury County. The estimates from the 2018 American Community Survey show that the population of the study area decreased to 145,962 in 2018, representing a decline of 0.24%. The counties within the study area that experienced a major decline in population between 2010 and 2018 were Cherokee County and Ida County. This trend is partly due to the rural nature of these counties. While Woodbury County and Plymouth County on the other hand experienced population growth from 2010 to 2018 by 0.4% and 0.2% respectively (see Figure 1 below).

![Figure_1](Figure_1.JPG)

![Figure_2](Figure_2.JPG)

## Project Description
The study area, especially Woodbury County, has recently experienced unprecedented industrial growth when compared to other counties within the Tri-State Region (Nebraska, S. Dakota, and Iowa). In light of this, I wanted to assess the most suitable areas within the study area for the establishment of a new industry.  The objective of this research is to identify the most suitable sites within the study area for the establishment of a processing plant. For the region to continue to attract industries, the Economic Development Department of each of the counties must identify potential areas they can develop into shovel ready sites. 

## Methodology
The method deployed in executing this project is quantitative. The python programming language was used in executing this project (check appendix for the code). The arcpy module from ESRI, which is installed along ArcGIS Desktop Software was used for the analysis. The table below shows the type and sources of data used in the study. The data used for this study included parcel, floodplain, wetland, major road, and population density. Four of the data set were nominal data while only one data set was ordinal. All the data set were in vector format.  The majority of the data came from local, state, and federal governments. 

GIS dataset     |   Description     |     Sources     |      Date    |    Data Type  |
-------------   |   ------------    |    ---------    |     ------   |   ----------  |
Parcel data     | Parcel data shows the quantity of land identified for taxation purposes. It contains land use necessary for the suitability analysis. | Woodbury County Assessor, Cherokee County Assessor, Ida County Assessor, Plymouth County Assessor | 2019 | Vector |  
 Floodplain data | This dataset incorporates all Flood Insurance Rate Map (FIRM) databases published by FEMA. This dataset contains information on flood hazards.| [FEMA](https://msc.fema.gov/portal/home) [National Flood Hazard Data set](https://hazards.fema.gov/femaportal/wps/portal/NFHLWMSkmzdownload)| 2011 | Vector |
 Wetland data  | This dataset contains an inventory of wetlands in the country and provides detailed information on the abundance, characteristics, and distribution of wetlands in the nation. | [US Fish and Wildlife Service: National Wetlands Inventory:](https://www.fws.gov/wetlands/data/data-download.html) | 2018 | Vector |
 Major Road Dataset | This dataset contained major roads (Interstate, Other principal arterials, minor arterial, and Major collector) within Cherokee, Plymouth, Ida, and Woodbury County.| [Iowa Dot](https://data.iowadot.gov/) | 2019 | Vector |
 Population density by block group | This dataset contains the population by block group. The population density was obtained by dividing the pop. by the area of the block group. |  [U.S. Census Bureau](https://www.census.gov/acs/www/data/data-tables-and-tools/american-factfinder/) | 2015 | Vector |


Figure 3 below shows that the model used in analyzing the data set is the ordinal combination and pass/fail model. The data set was first prepared by using arcpy functions such as merge. Using the select by attribute function major roads (interstate, minor arterial, other principal arterials, and major collectors) were selected. The selected roads were converted into Euclidean Distance using spatial analytic function – Euclidean Distance. This was necessary to be able to estimate the distance from each of the major roads in the study area. The resulted raster was reclassified as shown in Table 2 below, using the reclassify function. A for loop was then used to loop through the parcel, floodplain, population density, and wetland dataset, and converted from vector to raster. The resulted raster was then reclassified as shown in Table 2 below, using the reclassify function (see Figure 4 below for a map of reclassified rasters). Note that Plymouth County’s floodplain dataset is not available, so I assumed that the entire county was outside the 100-year flood zone. The reclassified rasters were then combined using the raster calculator function and the equation below: 

$$ Suitability = (Dist. from major road + Pop. Density + land use)$ *(flood plain) * (wetland) $$

The suitable areas for establishing a processing plant were then calculated as outlined in the code in the appendix.

![Figure_3](Figure_3.JPG)

Factors|	Data| Ranges| Ratings |
------- |  -----|-------|---------|
Type of land use (parcel) |	Exempt land use (schools, parks, etc.) | 0
                          |--------------------------------------- |
                          | Residential                              |0
                          | Commercial                               |3
                          | Industry                                 |4
                          | Agriculture                              |4
------------------------  | ------------------------------------------|
Floodplain (Flood zones & areas outside flood zones)|	100 years flood zone	0


	Zone outside 100 years flood zone	1
Wetland data (Wetlands & areas outside wetlands)	Wetland Zone	0
	Areas outside wetland zone	1
Distance from a major road (Interstate, Other principal arterials, minor arterial, and major collector)	6000+ m	0
	4501 – 6000 m	1
	3001 – 4500 m	2
	1501 – 3000 m	3
	0 – 1500 m	4
Population density	0 – 100 pop/sqkm	0
	101 – 500 pop/sqkm	1
	501 – 2500 pop/sqkm	2
	2501 – 5,000 pop/sqkm	3
	5,000+ pop/sqkm	4



### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Suitability Analysis for Location of Processing Plant


## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/Gabriel-Appiah/GIS_python/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
