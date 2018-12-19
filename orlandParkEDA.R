library("readxl")

# Read in the data frame
data.df = read.table("data/Orland_Park/OP_Provs_by_Friend_Type_and_Loneliness_20181213.txt",
					 sep = "\t", header = T, row.names = 1
					)

# Remove lines with a missing lictot
iRmID = which(is.na(data.df[, "lictot"]))
data.df = data.df[-iRmID,]

for(c in 4:ncol(data.df)){

	column = colnames(data.df)[c]

	png(file = paste0("output/", column, "_vs_LonelinessScore.png"),
		width = 7, height = 7, units = "in", res = 300
	   )

	idx = which(data.df[, "lictot"] > 0)

	# Make the plot
	plot(x = data.df[idx, column], y = data.df[idx, "lictot"],
		 xlim = c(0, 10.5), ylim = c(10, 60),
		 pch = 19, cex = 0.5, col = "#00000050",
		 xlab = column, ylab = "Loneliness Score"
		)

	spCor = cor(data.df[idx, column], data.df[idx, "lictot"], method = "spearman") 
	text(x = 10.5, y = 60, adj = c(1, 1), labels = paste("Spearman cor:", format(spCor, digits = 4)))

	dev.off()

	corCol = "ProvsAllClassmates_8items"
	cat(column, " vs. lictot Spearman Correlation:\t", spCor,
		sep = "", end = "\n"
	   )

}

idx = which(data.df$lictot > 20)

linMod = lm(lictot ~ ProvsRecipFriends_8items + ProvsGivenFriends_8items + ProvsReceivedFriends_8items + ProvsNonFriends_8items, data = data.df)
linMod = lm(lictot ~ ProvsAllClassmates_8items, data.df)
linMod = lm(lictot ~ ProvsAllClassmates_8items, data.df)

# glmMod = glm(lictot ~ ProvsAllClassmates_8items, data = data.df, family = gamma)



plot(x = data.df$lictot, y = as.numeric(linMod$fitted.values),
	 pch = 19,
	 xlab = "Loneliness Score (Observed)", ylab = "Loneliness Score (Predicted)"
	)

if(0){

# Get the total class size
data.df[, "TotalClassSize"] = rowSums(data.df[, c("CrossSex", "SameSexNoChild")])




# Scale each provision to a class size of 25
data.df[, "Scaled_ProvsAllClassmates_8items"] = data.df[, "ProvsAllClassmates_8items"] * (data.df[, "TotalClassSize"] / 25)


for(i in c(4:8, 10)){

	corCol = colnames(data.df)[i]
	cat(corCol, " vs. lictot Spearman Correlation:\t", cor(data.df[, corCol], data.df[, "lictot"], method = "spearman"), 
		sep = "", end = "\n"
	   )

}

cat("\n\n")


# Make the plot
plot(x = data.df[, "Scaled_ProvsAllClassmates_8items"], y = data.df[, "lictot"],
	 pch = 19, cex = 0.5, col = "#00000050",
	 xlab = "Average Provisions All Classmates", ylab = "Loneliness Score"
	)
# Check an individual class

class_idx = grep("^15\\d{2}", row.names(data.df))
plot(x = data.df[class_idx, "ProvsAllClassmates_8items"], y = data.df[class_idx, "lictot"],
	 pch = 19, 
	 xlab = "Average Provisions All Classmates", ylab = "Loneliness Score"
	)

# Set the excel file
f_xlsx = "FriendshipPeerProvisionsByItemAnalysis.xlsx"

# Get the Excel sheets
sheet_names = readxl::excel_sheets(f_xlsx)

for(itemNum in sheet_names){

	# Obtain the first sheet as a data frame
	item.df = as.data.frame(readxl::read_excel(f_xlsx, sheet = itemNum), optional = T, stringsAsFactors = F)

	# Make df like data.df
	rownames(item.df) = item.df[,1]
	item.df = item.df[-iRmID,-1]

	png(file = paste0("scaled_plots/", itemNum, "_vs_LonelinessScore.png"),
		width = 7, height = 7, units = "in", res = 300
	   )

	# Scale the peer provisions received to class size
	scaledNumProvRec = item.df[, "NumberPeerProvisionsReceived"] * (data.df[, "TotalClassSize"] / 25)

	plot(x = scaledNumProvRec, y = data.df[, "lictot"],
		 xlim = c(0, 17), ylim = c(10, 60),
		 pch = 19, cex = 0.5, col = "#00000050",
		 main = paste(itemNum, "(scaled to class size)"),
		 xlab = paste(itemNum, "# PeerProvisions Received"), ylab = "Loneliness Score"
		)

	spCor = cor(scaledNumProvRec, data.df[, "lictot"], method = "spearman") 
	text(x = 17, y = 60, adj = c(1, 1), labels = paste("Spearman cor:", format(spCor, digits = 4)))

	dev.off()

	cat(itemNum, " PeerProvisions Received vs. lictot Spearman Correlation:\t", spCor,
		sep = "", end = "\n"
       )

}

}
