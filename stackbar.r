set.seed(50)

Data <- data.frame(
  Year = c(rep(c("Para","Array","Equa","Stream","Mixed", "URL", "Simple", "JSON"), each = 5)),
  Category = c(rep(c("VERBOSE","DEBUG","INFO","WARN","ERROR"), times = 8)),
  Frequency = c(0,	0,	0,	0,	3,
0,	0,	30,	0,	0,
3,	23,	8,	3,	0,
0,	62,	0,	0,	0,
0,	81,	2,	5,	0,
0,	14,	57,	17,	9,
0,	43,	46,	4,	28,
12,	8,	152,	0,	0)
)

library(ggplot2)

ggplot(Data, aes(Year, Frequency, fill = Category)) + geom_bar(position="fill", stat="identity") + scale_y_continuous(expand = expansion(mult = c(0, .2))) + theme(text=element_text(size=25)) + theme(axis.title.x = element_blank()) + theme(axis.title.y = element_blank())

 
ggsave("plot.png", height = 6)