library("alluvial")
library("readxl")
library("plyr")

transform_to_columns = function(ARG_INPUT_DF, ARG_FALL){

	# Set the friendship types
	friendshipTypes = c("Acquaintance", "Rev. Unilateral", "Unilateral", "Reciprocal")

	# Create a new data frame
	out.df = as.data.frame(matrix(0, nrow = 16, ncol = 4))
	colnames(out.df) = c("Fall", "Winter", "Spring", "Number")
	out.df[,1] = ARG_FALL
	out.df[,2] = rep(friendshipTypes, each = 4)
	out.df[,3] = rep(friendshipTypes, 4)

	# Fill out the data frame
	rIndex = 1
	for(i in 1:4){
		for(j in 1:4){
			out.df[rIndex,4] = ARG_INPUT_DF[i,j]
			rIndex = rIndex + 1
		}
	}

	# Remove "0" rows
	out.df = out.df[which(out.df[,4] > 0),]

	return(out.df)

}

transform_to_single_rows = function(ARG_INPUT_DF, ARG_SPLIT){

	# Transform into single rows
	data.l = list()

	for(i in 1:nrow(ARG_INPUT_DF)){

		# Get the current row
		rowVals = ARG_INPUT_DF[i,]
		rowVals[4] = 1

		# Get the number of values
		numVals = ARG_INPUT_DF[i,4] / ARG_SPLIT
		cat(numVals, "\n")

		# Insert into new data frame
		data.l[[i]] = rbind(rowVals[rep(1, numVals),])

	}

	# Create the master data.df
	data.df = rbind.fill(data.l)

	# Reorder the winter columns
	data.df[,2] = factor(data.df[,2], levels = c("Acquaintance", "Rev. Unilateral", "Unilateral", "Reciprocal"))
	data.df[,3] = factor(data.df[,3], levels = c("Acquaintance", "Rev. Unilateral", "Unilateral", "Reciprocal"))
	data.df = data.df[order(data.df[,2], data.df[,3]),]

	# Return the data.df
	return(data.df)

}

create_graph = function(ARG_FILENAME, ARG_INPUT_DF){

	# Set the colors based on winter grouping
	color.v = character(nrow(ARG_INPUT_DF))

	friendshipTypes = c("Acquaintance", "Unilateral", "Rev. Unilateral", "Reciprocal")
	grayCols = grey.colors(4, start = 0.1, end = 0.7)

	for(i in 1:4){
		color.v[which(ARG_INPUT_DF[,2] == friendshipTypes[i])] = grayCols[i]
	}

	png(file = ARG_FILENAME, width = 10, height = 7, units = "in", res = 300)

	# Create the graph
	alluvial(ARG_INPUT_DF[,1:3], freq = ARG_INPUT_DF[,4],
			 col = color.v
			)

	dev.off()


}

DATA_DIR = "C:/Programs/cygwin64/home/jab112/github/SraLab/data/Wellesley"

friends.df = as.data.frame(read_excel(file.path(DATA_DIR, "Two_Step_Transitions.xlsx"), range = "A3:I19"))

# Set the friendship types
friendshipTypes = c("Acquaintance", "Rev. Unilateral", "Unilateral", "Reciprocal")

for(f in 1:4){

	for(y in 1:2){

		# Get the year coordinates
		if(y == 1){
			lYear = 2
			rYear = 5
		}else{
			lYear = 6
			rYear = 9
		}

		# Get the row coordinates
		tRow = 1 + (f - 1) * 4
		bRow = 4 + (f - 1) * 4

		data.df = transform_to_columns(friends.df[tRow:bRow, lYear:rYear], friendshipTypes[f])

		if(empty(data.df)){
			cat("No data for ", friendshipTypes[f], " year ", y, "skipping...\n", sep = "")
			next
		}

		for(j in 1:2){

			single_rows.df = transform_to_single_rows(data.df, j)

			create_graph(paste0("20190807/", friendshipTypes[f], "_year_", y, "_rowN_", j, ".png"), single_rows.df)

		}

	}

}
