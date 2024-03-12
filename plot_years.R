
stocking <- read.csv("/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/formatted_years/formatted_years_stocking.csv")
eradication <- read.csv("/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/formatted_years/formatted_years_eradication.csv")
regulation <- read.csv("/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/formatted_years/formatted_years_regulation.csv")
habitat_management <- read.csv("/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/formatted_years/formatted_years_habitat.csv")

plot.matrix <- matrix(c(1, 3, 5, 7, 
                        2, 4, 6, 8), 
                      nrow = 4, ncol = 2)
plot.matrix
cex.axis   <- 1.2
col.bords  <- "gray60"
layout(mat = plot.matrix, widths = c(1,3))
size.point <- 1.2
cols_mat <- c("lightblue", "lightpink", "lightgreen", "lightyellow")
order_graphs <- c(7,3,5)
par(oma = c(6, 4, 0, 2))
mar.left   <-  c(0, 2, 1.5, 2)
mar.right  <-  c(0, 2, 1.5, 4)
axis.cols  <- c("white", "white", "white", "white", "black", "white", "white" ) # show on bottom row
cex.labs <- 1.2
main_labels = c("Stocking", "Eradication", "Regulation", "Habitat Management")
file_paths = c(stocking, eradication, regulation, habitat_management)


for (i in 1:4){
  plot_box(file_paths[i], main_labels[i], cols_mat[i])
}

plot_box <- function(file_path, name, color){
  years <- file_path$DATE
  contains_years <- grepl("[^0-9]", years)
  non_numeric_indices <- !grepl("^[0-9]+$", years)
  years[!grepl("[^0-9]", years)]
  years[non_numeric_indices] <- NA
  years <- na.omit(years)
  years <- as.integer(years)
  years <- years[(years < 2000) & (years > 1900)]
  max(years)
  head(years)
  head(contains_years)
  # title <- name + ' Years'
  boxplot(years,
          main = name, 
          xlab = "Years",         
          ylab = "Years",         
          col = color,
          ylim=c(1900,2000))
  hist(years,
       main = name,  
       xlab = "Values",                   
       ylab = "Frequency",              
       col = color,                 
       border = "black",
       breaks = seq(1900, 2000, by = 5)
  )
}


plot_bar <- function(name){
  hist(years,
       main = name,  
       xlab = "Values",                   
       ylab = "Frequency",              
       col = color,                 
       border = "black",
       breaks = seq(1900, 2000, by = 5)
  )
}


plot_box(stocking, 'Stocking', "lightblue")

plot_box(eradication, 'Eradication', "lightpink")

plot_box(regulation, 'Regulation', "lightgreen")

plot_box(habitat_management, 'Habitat Management', "lightyellow")
