# we need to clean this data - let's do it quickly in R

# load libraries
library(tidyverse)

# load data
accounts_raw <- read.csv("/Users/oliverbrown/Desktop/Oli/Programming/Hack/Kaluza/accounts.csv")

accounts_clean <- accounts_raw %>%
    mutate(EV = case_when(f0_ == "" ~ "False",
                          f0_ == "ev" ~ "True")) %>%
    select(hashed_account_no,outcode,EV)

head(accounts_clean)

write.csv(accounts_clean,"/Users/oliverbrown/Desktop/Oli/Programming/Hack/Cleaned Data/cleaned_accounts.csv")