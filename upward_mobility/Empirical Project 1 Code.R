# Clara Chen
# Upward Mobility in Hartford

# Install Packages
if (!require(tidyverse)) install.packages("tidyverse"); library(tidyverse)
if (!require(haven)) install.packages("haven"); library(haven)
if (!require(ggplot2)) install.packages("ggplot2"); library(ggplot2)
if (!require(statar)) install.packages("statar"); library(statar)

# Big Picture Analysis

with(subset(atlas, tract == 502100), mean(kfr_pooled_pooled_p25, na.rm=TRUE))
with(subset(atlas, state == 9), mean(kfr_pooled_pooled_p25, na.rm=TRUE))
with(atlas, mean(kfr_pooled_pooled_p25, na.rm=TRUE))

hartford_county$popdensity_rank <- rank(hartford_county$popdensity2010)
hartford_county$popdensity_rank <- 100*hartford_county$popdensity_rank /max(hartford_county$popdensity_rank)

# Education and Upward Mobility
ggplot(hartford_county, aes(x = kfr_pooled_pooled_p25, y = frac_coll_plus2010)) +
  stat_binmean(n = 50, color = "darkblue") + stat_smooth(method = "lm", se = FALSE) +
  labs(x = "Absolute Mobility at the 25th Percentile", y ="Fraction of Residents With at Least \na College Degree (2010)", 
       title = "College Degrees vs. Mobility for Hartford County") +
  theme_linedraw()

ggplot(hartford_county, aes(x = kfr_pooled_pooled_p25, y = gsmn_math_g3_2013)) +
  stat_binmean(n = 50, color = "darkblue") + stat_smooth(method = "lm", se = FALSE) +
  labs(x = "Absolute Mobility at the 25th Percentile", y ="Grade 3 Math Scores (2013)", 
       title = "Grade 3 Math Scores vs. Mobility for Hartford County") +
  theme_linedraw()

ggplot(hartford_county, aes(x = popdensity_rank, y = kfr_pooled_pooled_p25, color = gsmn_math_g3_2013)) +
  stat_binmean(n = 50) +
  labs(x = "Population Density (2010)", y = "Absolute Mobility at the 25th Percentile",
       color = "Grade 3 Math \nScores (2013)", title = "Population Density vs. Mobility by Test Scores") +
  theme_linedraw()
  
ggplot(hartford_county, aes(x = popdensity_rank, y = kfr_pooled_pooled_p25, color = frac_coll_plus2010)) +
  stat_binmean(n = 50)+
  labs(x = "Population Density (2010)", y = "Absolute Mobility at the 25th Percentile",
       color = "Fraction of Residents\nWith At Least a College \nDegree (2010)", title = "Population Density vs. Mobility by College Degrees") +
  theme_linedraw()

cor(hartford_county$gsmn_math_g3_2013, hartford_county$kfr_pooled_pooled_p25, use="pairwise.complete.obs")
cor(hartford_county$frac_coll_plus2010, hartford_county$kfr_pooled_pooled_p25, use="pairwise.complete.obs")

# Role of Income Level
inc1 <- with(subset(hartford_county, popdensity_rank <= 25), mean(hhinc_mean2000, na.rm=TRUE))
poor1 <- with(subset(hartford_county, popdensity_rank <= 25), mean(poor_share2000, na.rm=TRUE))
rent1 <- with(subset(hartford_county, popdensity_rank <= 25), mean(rent_twobed2015, na.rm=TRUE))

inc2 <- with(subset(hartford_county, popdensity_rank > 25 & popdensity_rank <= 50), mean(hhinc_mean2000, na.rm=TRUE))
poor2 <- with(subset(hartford_county, popdensity_rank > 25 & popdensity_rank <= 50), mean(poor_share2000, na.rm=TRUE))
rent2 <- with(subset(hartford_county, popdensity_rank > 25 & popdensity_rank <= 50), mean(rent_twobed2015, na.rm=TRUE))

inc3 <- with(subset(hartford_county, popdensity_rank > 50 & popdensity_rank <= 75), mean(hhinc_mean2000, na.rm=TRUE))
poor3 <- with(subset(hartford_county, popdensity_rank > 50 & popdensity_rank <= 75), mean(poor_share2000, na.rm=TRUE))
rent3 <- with(subset(hartford_county, popdensity_rank > 50 & popdensity_rank <= 75), mean(rent_twobed2015, na.rm=TRUE))

inc4 <- with(subset(hartford_county, popdensity_rank >= 100), mean(hhinc_mean2000, na.rm=TRUE))
poor4 <- with(subset(hartford_county, popdensity_rank >= 100), mean(poor_share2000, na.rm=TRUE))
rent4 <- with(subset(hartford_county, popdensity_rank >= 100), mean(rent_twobed2015, na.rm=TRUE))

income_table <- data.frame(c("Lowest Quartile", "2nd Quartile", "3rd Quartile", "Highest Quartile"),
                           c(inc1, inc2, inc3, inc4),
                           c(poor1, poor2, poor3, poor4),
                           c(rent1, rent2, rent3, rent4))
names(income_table)[1] <- "Population Density"
names(income_table)[2] <- "Mean Income"
names(income_table)[3] <- "Poor Share"
names(income_table)[4] <- "Rent"

cor(hartford_county$rent_twobed2015, hartford_county$kfr_pooled_pooled_p25, use="pairwise.complete.obs")
cor(hartford_county$rent_twobed2015, hartford_county$popdensity2010, use="pairwise.complete.obs")

ggplot(hartford_county, aes(x=kfr_pooled_pooled_p25, y=hhinc_mean2000, color=popdensity_rank)) +
  stat_binmean(n=50) +
  scale_color_gradient(high ="#132B43", low="#56B1F7") +
  labs(y="Mean Household Income (2000)", x="Absolute Mobility at the 25th Percentile",
       color="Population Density \nPercentile Ranking \n(2010)", title = "Mobility vs. Mean Income by Population Density") +
  theme_linedraw()

ggplot(hartford_county, aes(x=kfr_pooled_pooled_p25, y=rent_twobed2015, color=popdensity_rank)) +
  stat_binmean(n=50) +
  scale_color_gradient(high ="#132B43", low="#56B1F7") +
  labs(y="Two Bedroom Rent", x="Absolute Mobility at the 25th Percentile",
       color="Population Density \nPercentile Ranking \n(2010)", title = "Mobility vs. Housing Cost by Population Density") +
  theme_linedraw()

# Role of Race
white1 <- with(subset(hartford_county, popdensity_rank <= 25), mean(kfr_white_pooled_p25, na.rm=TRUE))
black1 <- with(subset(hartford_county, popdensity_rank <= 25), mean(kfr_black_pooled_p25, na.rm=TRUE))
asian1 <- with(subset(hartford_county, popdensity_rank <= 25), mean(kfr_asian_pooled_p25, na.rm=TRUE))
hisp1 <- with(subset(hartford_county, popdensity_rank <= 25), mean(kfr_hisp_pooled_p25, na.rm=TRUE))

white2 <- with(subset(hartford_county, popdensity_rank > 25 & popdensity_rank <= 50), mean(kfr_white_pooled_p25, na.rm=TRUE))
black2 <- with(subset(hartford_county, popdensity_rank > 25 & popdensity_rank <= 50), mean(kfr_black_pooled_p25, na.rm=TRUE))
asian2 <- with(subset(hartford_county, popdensity_rank > 25 & popdensity_rank <= 50), mean(kfr_asian_pooled_p25, na.rm=TRUE))
hisp2 <- with(subset(hartford_county, popdensity_rank > 25 & popdensity_rank <= 50), mean(kfr_hisp_pooled_p25, na.rm=TRUE))

white3 <- with(subset(hartford_county, popdensity_rank > 50 & popdensity_rank <= 75), mean(kfr_white_pooled_p25, na.rm=TRUE))
black3 <- with(subset(hartford_county, popdensity_rank > 50 & popdensity_rank <= 75), mean(kfr_black_pooled_p25, na.rm=TRUE))
asian3 <- with(subset(hartford_county, popdensity_rank > 50 & popdensity_rank <= 75), mean(kfr_asian_pooled_p25, na.rm=TRUE))
hisp3 <- with(subset(hartford_county, popdensity_rank > 50 & popdensity_rank <= 75), mean(kfr_hisp_pooled_p25, na.rm=TRUE))

white4 <- with(subset(hartford_county, popdensity_rank > 75), mean(kfr_white_pooled_p25, na.rm=TRUE))
black4 <- with(subset(hartford_county, popdensity_rank > 75), mean(kfr_black_pooled_p25, na.rm=TRUE))
asian4 <- with(subset(hartford_county, popdensity_rank > 75), mean(kfr_asian_pooled_p25, na.rm=TRUE))
hisp4 <- with(subset(hartford_county, popdensity_rank > 75), mean(kfr_hisp_pooled_p25, na.rm=TRUE))


race <- data.frame(c(rep("1st Quartile",4),rep("2nd Quartile",4),rep("3rd Quartile",4),rep("4th Quartile",4)),
                   rep(c("White", "Black","Asian","Hispanic"), 4),
                   c(white1, black1, asian1, hisp1, white2, black2, asian2, hisp2, white3, black3, asian3, hisp3, white4, black4, asian4, hisp4))
names(race)[1] <- "Population Density (2010) Quartile"
names(race)[2] <- "Race"
names(race)[3] <- "Absolute Mobility at the 25th Percentile"

ggplot(race, aes(x=`Population Density (2010) Quartile`, 
                 y=`Absolute Mobility at the 25th Percentile`, fill = `Race`)) +
  geom_bar(stat="identity", position="dodge") +
  scale_fill_brewer(palette="Set1") +
  labs(title="Mobility vs. Population Density by Racial Groups") +
  theme_linedraw()

cor(hartford_county$kfr_white_pooled_p25, hartford_county$frac_coll_plus2010, use="pairwise.complete.obs")
cor(hartford_county$kfr_black_pooled_p25, hartford_county$frac_coll_plus2010, use="pairwise.complete.obs")

# Role of Gender
f1 <- with(subset(hartford_county, popdensity_rank <= 25), mean(kfr_pooled_female_p25, na.rm=TRUE))
m1 <- with(subset(hartford_county, popdensity_rank <= 25), mean(kfr_pooled_male_p25, na.rm=TRUE))

f2 <- with(subset(hartford_county, popdensity_rank > 25 & popdensity_rank <= 50), mean(kfr_pooled_female_p25, na.rm=TRUE))
m2 <- with(subset(hartford_county, popdensity_rank > 25 & popdensity_rank <= 50), mean(kfr_pooled_male_p25, na.rm=TRUE))

f3 <- with(subset(hartford_county, popdensity_rank > 50 & popdensity_rank <= 75), mean(kfr_pooled_female_p25, na.rm=TRUE))
m3 <- with(subset(hartford_county, popdensity_rank > 50 & popdensity_rank <= 75), mean(kfr_pooled_male_p25, na.rm=TRUE))

f4 <- with(subset(hartford_county, popdensity_rank > 75), mean(kfr_pooled_female_p25, na.rm=TRUE))
m4 <- with(subset(hartford_county, popdensity_rank > 75), mean(kfr_pooled_male_p25, na.rm=TRUE))

gender <- data.frame(c(rep("1st Quartile",2),rep("2nd Quartile",2),rep("3rd Quartile",2),rep("4th Quartile",2)),
                   rep(c("Female", "Male"), 4),
                   c(f1, m1, f2, m2, f3, m3, f4, m4))
names(gender)[1] <- "Population Density (2010) Quartile"
names(gender)[2] <- "Gender"
names(gender)[3] <- "Absolute Mobility at the 25th Percentile"

ggplot(gender, aes(x=`Population Density (2010) Quartile`, 
                   y=`Absolute Mobility at the 25th Percentile`, fill=Gender)) +
  geom_bar(stat="identity", position="dodge") +
  scale_fill_brewer(palette="Set1") +
  labs(title="Mobility vs. Population Density by Gender") +
  theme_linedraw()
