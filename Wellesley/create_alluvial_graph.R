library("alluvial")

for(j in 1:5){

# Load in the dataset
data.df = read.table("acquaintance_year1.txt", sep = "\t", header = T)

# Remove "0" rows
data.df = data.df[which(data.df[,4] > 0),]

# Transform into single rows
data.l = list()

for(i in 1:nrow(data.df)){

	# Get the current row
	rowVals = data.df[i,]
	rowVals[4] = 1

	# Get the number of values
	numVals = data.df[i,4] / j
	cat(numVals, "\n")

	# Insert into new data frame
	data.l[[i]] = rbind(rowVals[rep(1, numVals),])

}

# Create the master data.df
data.df = rbind.fill(data.l)

png(file = paste0("acquaintance_year1_div_by_", j, ".png"), width = 10, height = 7, units = "in", res = 300)

# Create the graph
alluvial(data.df[,1:3], freq = data.df[,4],
		 col = ifelse(data.df$Winter == "Unilateral", "gray50", "gray")
		)

dev.off()

}
