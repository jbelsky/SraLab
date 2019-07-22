library("alluvial")

# Load in the dataset
data.df = read.table("acquaintance_year1.txt", sep = "\t", header = T)

# Remove "0" rows
data.df = data.df[which(data.df[,4] > 0),]

png(file = "acquaintance_year1.png", width = 10, height = 7, units = "in", res = 300)

# Create the graph
alluvial(data.df[,1:3], freq = data.df[,4],
		 col = ifelse(data.df$Winter == "Unilateral", "gray50", "gray")
		)

dev.off()
