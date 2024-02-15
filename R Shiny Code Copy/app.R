library(shiny)
library(shinyBS)
library(ggplot2)
library(plotly)
library(tidyr)
library(rsconnect)
p <- shiny::p


ui <- fluidPage(
  
  # App title
  titlePanel("Comparing Fuzzy Matching Ratios"),
  
  fluidRow(
    column(
      width = 2,
      
      selectInput(
        inputId = "ratio", 
        label = "Ratio Threshold",
        choices = c('0','25','50','75','85','95','100'),
        selected = '0',
        
      ),
    ),
    column(
      width = 2,
      selectInput(
        inputId = "included",
        label = "Included",
        choices = c("All", "Recorded", "Not Recorded"),
        selected = "All",
        
      ),
    ),
    column (
      width = 2,
      selectInput(
        inputId = "category",
        label = "Category",
        choices = c("All", "Eradication", "Habitat Management", "Regulation", "Stocking"),
        selected = "All",
        
      ),
    ),
    column(
      width = 3,
      # Input: Slider for the number of bins
      sliderInput(inputId = "bins",
                  label = "Number of Bins",
                  min = 1,
                  max = 50,
                  value = 30),
      bsTooltip("bins", "The wait times will be broken into this many equally spaced bins",
                "right", options = list(container = "body")),
    )  ,
    
    column(
      width = 3,
      sliderInput(inputId = "xRange", label = "X Range", min=0,max=100,value=c(0, 100),step=1),
      br(),
      sliderInput(inputId = "yRange", label = "Y Range", min=0,max=4000,value=c(0, 4000),step=1),
    )  ,
    
    
  ),
  
  br(),
  hr(), 
  br(),
  plotlyOutput(outputId = "distPlot"),
  plotOutput(outputId = "add"),
  uiOutput(outputId = "dynamic"),
  
  
)






server <- function(input, output, session) {
  
  
  output$add <- renderPlot(
    {
      addTooltip(session = session , id = "ratio", title = "The threshold for which the fuzzy matches are recorded", 
                 placement = "right", options = list(container = "body"))
      addTooltip(session = session, id = "category", title = "The ratios will be filtered based upon which management strategy is chosen",
                 placement = "right", options = list(container = "body"))
      addTooltip(session = session, id = "included",title =  "The ratios will be filtered based upon whether the contents was included in CSV or not",
                 placement = "right", options = list(container = "body"))
      
      
      addPopover(session = session, id = "distPlot", title = "Data", 
                 content = paste0(
                   "Each ratio in the histogram is calculated using Fuzzy Matching - Simple Ratio. More information can be found here: https://docs.python.org/2/library/difflib.html#difflib.SequenceMatcher.ratio
   " ), trigger = 'click', options = list(container = "body"))
      
      
      
      
    }
  )
  
  output$distPlot <- renderPlotly({
    
    path <- paste0("data/ratio_", input$ratio , ".csv")
    
    
    validate(
      need(!(input$category != "All" && input$included == "Not Recorded"), "Cannot sort 'Not Recorded' data, please either select 'All'/'Recorded' from the included dropdown or 'All' from the Category dropdowns")
    )
    
    validate(
      need(!((input$ratio == "95" || input$ratio == "100") && (input$included == "Recorded" || input$category != 'All')), "No data recorded for Ratio this high. Select a lower ratio, OR 'All'/'Not Recorded' from Included dropdown, OR 'All' from the Category dropdown")
    )
    
    # In your Shiny app code (app.R)
    # file_path <- "data/your_file.csv"
    #data <- read.csv(file_path)
    
    
    
    
    
    ratios <- read.csv(path, header=TRUE)
    #  ratios <- read_sheet(path)
    
    colnames(ratios) <- c("Ratio", "Included", "Sheet", "Line")
    
    
    
    
    
    
    
    if (input$included == "Recorded"){
      ratios <- ratios[ratios$Included == 1,]
    } else if (input$included == "Not Recorded"){
      ratios <- ratios[ratios$Included == 0,]
    }
    
    
    
    
    # ratios <- na.omit(ratios)
    ratios$Sheet[ratios$Sheet == ""] <- "Not Included"
    ratios$Sheet[ratios$Sheet == "NA"] <- "Not Included"
    
    #   ratios$Sheet[ratios$Sheet == NA] <- "Not Included", 
    ratios["Sheet"][is.na(ratios["Sheet"])] <- "Not Included"
    
    ratios$Sheet[ratios$Sheet == "eradication"] <- "Eradication"
    ratios$Sheet[ratios$Sheet == "habitat"] <- "Habitat Management"
    ratios$Sheet[ratios$Sheet == "regulation"] <- "Regulation"
    ratios$Sheet[ratios$Sheet == "stocking"] <- "Stocking"
    
    if (input$category != "All"){
      ratios <- ratios[ratios$Sheet == input$category,]
      #   if (input$category == "Habitat Management") {
      #         ratios <- ratios[ratios$Sheet == 'Habitat Manageme',]
      #     } else {
      #         ratios <- ratios[ratios$Sheet == input$category,]
      
      #     }
    }
    
    # ratios <- ratios[ratios$Sheet == "Eradication",]
    x1    <- ratios$Ratio
    
    main_title = paste("Fuzzy Matching Ratios:", input$category)
    
    bins <- seq(min(x1), max(x1), length.out = input$bins + 1)
    #print(head(ratios))
    main_title = paste("Fuzzy Matching Ratios:", input$category)
    
    ggplot(data = ratios, aes( x = Ratio, fill = Sheet ) ) + 
      geom_histogram( bins=length(bins), color = 'black' ) +
      scale_fill_manual(values = c("plum1", 'indianred1','aquamarine','forestgreen', 'steelblue1')) +
      theme(legend.text = element_text(size = 8, colour = "black"), panel.background = element_rect(fill = 'white'), panel.grid.major = element_line(color = 'gray'), panel.grid.minor = element_line(color = 'gray', linetype = 'dotted')) +
      ggtitle(main_title) +
      labs(y = "Count", x = "Ratio")+
      scale_x_continuous(limits = c((input$xRange[1] - 1), (input$xRange[2] +1 )))+
      scale_y_continuous(limits = c(input$yRange[1], input$yRange[2]))
    
    
  })
  
  
}


shinyApp(ui = ui, server = server)
# In your Shiny app script (app.R)
#rsconnect::deployOptions(files = c("data/your_file.csv", "data/other_file.csv"))
#rsconnect::setAccountInfo(name='9emauh-jaime-jacob', token='93C3EA00FDC0C016AFB3782291FDBB16', secret='WmGKmOAAiNbYcdfPHCbzpyVIYKsQ8ibQ9dloae7H')
#rsconnect::deployApp(forceUpdate = TRUE)




