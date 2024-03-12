library(dplyr)
library(ggplot2)
library(mapdata)
library(tidyr)
library(stringr)
library(purrr)

plot_map <- function(file_path, label){
  file_path
  label
  df <- read.csv(file_path)
  df <- df[, c("LAKE.NAME","DATE")]
  df <- mutate(df, 
               county = map_chr(str_split(LAKE.NAME, "_"), 1),
               lakename = map_chr(str_split(LAKE.NAME, "_"), 2))
  
  df$county <- trimws(df$county)
  df$county <- tolower(df$county)
  
  df$lakename <- trimws(df$lakename)
  df$lakename <- tolower(df$lakename)
  
  df <- inner_join(df, loc_data, by = c('county', 'lakename'), relationship = "many-to-many")
  
  years <- df$DATE
  years[!grepl("[^0-9]", years)]
  non_numeric_indices <- !grepl("^[0-9]+$", years)
  years[non_numeric_indices] <- NA
  years <- as.integer(years)
  df$DATE <- ifelse(years < 2000 & years > 1900, years, NA)
  
  df$location <- paste(df$county, df$lakename)
  counts <- table(df$location, df$DATE)
  counts <- as.data.frame(counts)
  names(counts) <- c("location", "DATE", "occurrences")
  
  df <- merge(df, counts, by = c("location", "DATE"), all.x = TRUE)
  
  plot <- MI_basemap + 
    geom_point(data=df, aes(x = LONG_DD, y = LAT_DD, colour = c(DATE), size = c(occurrences)), alpha = 0.5) +
    labs(color="Year of Event", size="Number of Events per Lake", xlab = 'Longitude', ylab='Latitude')  + 
    ggtitle(label) + 
    theme_bw()
  
  print(plot)
}
MI<-map_data("state") %>%
  subset(region %in% c("michigan")) # select michigan 
MI_basemap<-ggplot(data = MI) + 
  geom_polygon(aes(x = long, y = lat, group = group), fill = "white", color = "black") + #this fill MI white and outline is black
  coord_fixed(1.3) 

loc_data<-read.csv("/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/MGNT_lake_info.csv") %>%
  distinct(new_key, .keep_all = TRUE) %>%  # select only one row per lake since you only need whole lake information
  drop_na(LONG_DD, LAT_DD) #omit data where you don't have location information
loc_data$county <- trimws(loc_data$county)
loc_data$county <- tolower(loc_data$county)
loc_data$lakename <- trimws(loc_data$lakename)
loc_data$lakename <- tolower(loc_data$lakename)

file_paths = c('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/formatted_years/formatted_years_stocking.csv', "/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/formatted_years/formatted_years_eradication.csv", "/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/formatted_years/formatted_years_habitat.csv", "/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/formatted_years/formatted_years_regulation.csv")

labels = c('Stocking','Eradication', 'Habitat Management', 'Regulation')

plot.matrix <- matrix(c(1, 2, 3, 4),
                      nrow = 2, ncol = 2)
layout(mat = plot.matrix)

#plot_map("/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/formatted_years/formatted_years_eradication.csv", 'Stocking')

for (i in seq(1:4)){
  plot_map(file_paths[i], labels[i])
}