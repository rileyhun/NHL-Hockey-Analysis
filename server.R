library(lubridate)
library(plotly)
library(ggplot2)
library(gridExtra)

shinyServer(function(input, output, session) {

hockey_df <- function(x){
  data <- read.csv('Player_Attributes.csv')

  data$Birth_Date <- as.POSIXct(as.character(data$Birth_Date), format="%m/%d/%Y")
  data$Year_Born <- year(data$Birth_Date)
  data$Height <- gsub(" ft", "", data$Height)
  data$Position <- data$Position
  data <- data[ order(data$Birth_Date, decreasing=TRUE), ]
  
  multiple_pos <- data[grepl('/', data$Position),]
  s <- strsplit(as.character(multiple_pos$Position), split='/')
  multiple_pos <- data.frame(Name = rep(multiple_pos$Name, sapply(s, FUN=length)),
                             Position = unlist(s),
                             Birth_Date = rep(multiple_pos$Birth_Date, sapply(s, FUN=length)),
                             Year_Born = rep(multiple_pos$Year_Born, sapply(s, FUN=length)),
                             Height = rep(multiple_pos$Height, sapply(s, FUN=length)),
                             Weight = rep(multiple_pos$Weight, sapply(s, FUN=length)))
  
  data <- data[!grepl('/', data$Position),]
  data <- rbind(data, multiple_pos)
  
  Player_data <- read.csv('NHL_Hockey_Player_Data (1999-2000 to 2015-2016 REGULAR).csv')
  Player_data$Pos <- gsub('L', 'LW', Player_data$Pos)
  Player_data$Pos <- gsub('R', 'RW', Player_data$Pos)
  Player_data$Season_Start <- gsub('-.*', "", Player_data$Season)
  
  
  
  All_data <- merge(Player_data, data, by.x = c("Player", "Pos"), by.y = c("Name", "Position"))
  All_data$Age <- strtoi(All_data$Season_Start) - strtoi(All_data$Year_Born)
  return(All_data)
}


output$trends1 <- renderPlot({
  df <- hockey_df()
  df$Season <- as.character(df$Season)
  df <- df[ which(df$Season_Start == input$season), ]
  df$Height <- factor(df$Height, levels=c('5-5', '5-6', '5-7', '5-8', '5-9', '5-10', '5-11',
                                        '6-0', '6-1', '6-2', '6-3', '6-4', '6-5', '6-6', '6-7', '6-8', '6-9'))
  
  if (input$variable == "Age") {
    ggplot(df, aes(x=Age)) + geom_histogram(aes(y=..density.., fill=..count..), position="dodge") + geom_density(col=2) +
    labs(title="Histogram for Hockey Player Age") + labs(x="Age", y="Count")
  }
  
  else if (input$variable == "Weight") {
    ggplot(df, aes(x=Weight)) + geom_histogram(aes(y=..density.., fill=..count..), position="dodge") + geom_density(col=2) +
      labs(title="Histogram for Hockey Player Weight") + labs(x="Player Weight", y="Count")
  }
  
  else if (input$variable == "Height") {
    ggplot(df, aes(x=Height)) + geom_bar() 
  }
}) 



output$trends2 <- renderPlot({
  df <- hockey_df()
  df$Season <- as.character(df$Season)
  df$Height <- as.numeric(gsub('-.*', "", df$Height))*0.3048 + as.numeric(gsub('.*-', "", df$Height))*0.0254
  
  df <- df[ which(df$Season_Start == input$season), ]
  
  if (input$variable == "Age" & input$variable_y == "P") {
    ggplot(df, aes(Age, P)) + geom_point() + geom_smooth(method= "lm", se = FALSE)
    }
  
  else if (input$variable_y == "P" && input$variable =="Weight") {
    ggplot(df, aes(Weight, P)) + geom_point() + geom_smooth(method= "lm", se = FALSE)
  }
  
  else if (input$variable_y == "P" && input$variable =="Height") {
    ggplot(df, aes(Height, P)) + geom_point() + geom_smooth(method= "lm", se = FALSE)
  }
  
  else if (input$variable_y == "G" && input$variable =="Age") {
    ggplot(df, aes(Age, G)) + geom_point() + geom_smooth(method= "lm", se = FALSE)
  }
  
  else if (input$variable_y == "G" && input$variable =="Weight") {
    ggplot(df, aes(Weight, G)) + geom_point() + geom_smooth(method= "lm", se = FALSE)
  }
  
  else if (input$variable_y == "G" && input$variable =="Height") {
    ggplot(df, aes(Height, G)) + geom_point() + geom_smooth(method= "lm", se = FALSE)
  }
 
  else if (input$variable_y == "GP" && input$variable =="Age") {
    ggplot(df, aes(Age, GP)) + geom_point() + geom_smooth(method= "lm", se = FALSE)
  }
  
  else if (input$variable_y == "GP" && input$variable =="Weight") {
    ggplot(df, aes(Weight, GP)) + geom_point() + geom_smooth(method= "lm", se = FALSE)
  }
  
  else if (input$variable_y == "GP" && input$variable =="Height") {
    ggplot(df, aes(Height, GP)) + geom_point() + geom_smooth(method= "lm", se = FALSE)
  }

  
  
})

})