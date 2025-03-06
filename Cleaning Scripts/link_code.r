library(tidyverse)

accounts <- read.csv("/Users/oliverbrown/Desktop/Oli/Programming/Hack/Cleaned Data/cleaned_accounts.csv")
hh_consumption <- read.csv("/Users/oliverbrown/Desktop/Oli/Programming/Hack/Kaluza/hh_consump.csv")

train_data <- merge(x = hh_consumption, y = accounts, by = "hashed_account_no",
                                                      all.x = TRUE, all.y = TRUE)
head(train_data)

write.csv(train_data,"/Users/oliverbrown/Desktop/Oli/Programming/Hack/Cleaned Data/training_data.csv") # nolint