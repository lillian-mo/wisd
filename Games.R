# Cleaning game data

# set working directory
setwd("~/WISD NBA Project 2023/games")

#load libraries
library(dplyr)
library(jsonlite)

#read games
game1 <- fromJSON("0042100301_events.jsonl")  %>% 
  as.data.frame(headers = TRUE)
