library(ggvis)
library(shiny)

fluidPage(theme="bootstrap.min.css",
          
          titlePanel("NHL Hockey Analysis"),
          
          sidebarLayout(
            
            sidebarPanel(
              hr(),
              sliderInput("season", "Select Season:", min=2000, max=2015, value = 2000, format="####.00", sep=""),
              selectInput("variable", "Select independent variable:", c("Age" = "Age", "Weight" = "Weight", "Height" = "Height")),
              selectInput("variable_y", "Select dependent variable:", c("Points" = "P", "Goals" = "G", "Games Played" = "GP"))
            ),
            
            mainPanel(
              
              tabsetPanel(
                tabPanel("Distribution of Variables",
                  
                         
                         h4("Trends"),
                         plotOutput("trends1")),
              tabPanel("Analysis of Relationships",
                       h4("ScatterPlots"),
                       plotOutput("trends2"))
              )
            )
          )
)