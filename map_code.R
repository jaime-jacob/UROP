### Map figures #### 

#load libraries (you will need to first install packages if you don't have them using the install.packages function)

library(dplyr)
library(ggplot2)
library(mapdata)

#read in your data 
data<-read.csv("/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/MGNT_lake_info.csv") %>%
  distinct(new_key, .keep_all = TRUE) %>%  # select only one row per lake since you only need whole lake information
  drop_na(LONG_DD, LAT_DD) #omit data where you don't have location information 
 
#get MI basemap 
MI<-map_data("state") %>%
  subset(region %in% c("michigan")) # select michigan 
MI_basemap<-ggplot(data = MI) + 
  geom_polygon(aes(x = long, y = lat, group = group), fill = "white", color = "black") + #this fill MI white and outline is black
  coord_fixed(1.3) 

#create a map #you can change the color based on the variable by changing "colour" part
MI_basemap + 
  geom_point(data=data, aes(x = LONG_DD, y = LAT_DD, colour = c(max_depth_m))) +  #
  labs(color="maximum depth (m)")  + #changes the labels on the legend 
  theme_bw() #this removes the gray background 

#you can also change the size of dots based on a variable by changing "size" part 
MI_basemap + 
  geom_point(data=data, aes(x = LONG_DD, y = LAT_DD, size = c(lake_area_ha))) +  #
  labs(size="lake area (ha)")  + #changes the labels on the legend 
  theme_bw() #this removes the gray background 

#or do both at the same time 
MI_basemap + 
  geom_point(data=data, aes(x = LONG_DD, y = LAT_DD, colour = c(max_depth_m), size = c(lake_area_ha))) +  #
  labs(color="maximum depth (m)", size="lake area (ha)")  + #changes the labels on the legend 
  theme_bw()

