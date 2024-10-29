
data <- data.frame(
  site=c("VERBOSE","DEBUG","INFO","WARN","ERROR"),
  incid=c(15,231,295,29,40))
head(data)

library(ggplot2)
library(dplyr)
plot <- data %>%
  ggplot(aes(x=reorder(site,+incid), y=incid)) + 
  geom_bar(stat="identity",fill="steelblue", width = 0.60)+ scale_y_continuous(expand = expansion(mult = c(0, .2))) +
  theme(text=element_text(size=24)) + theme(axis.title.x = element_blank()) + theme(axis.title.y = element_blank()) + geom_text(aes(label = incid, vjust = -0.5), size = 10) 
ggsave("plot.png", height = 6)