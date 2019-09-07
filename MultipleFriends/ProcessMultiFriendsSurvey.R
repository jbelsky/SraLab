# Set the input path
filesPath = "C:/usr/GoogleDrive/Programming/SraLab/Multiple Friends"

multiF.df = read.table(file.path(filesPath, "Multiple Friends Survey - Fall 2017_June 26, 2019_11.54.txt"), quote = "", 
					   sep = "\t", header = T, stringsAsFactors = F, fill = T, check.names = T
					  )

# Remove columns (rm 9 columns)
columnsToRemove = c("ResponseId", "RecipientLastName", "RecipientFirstName", "RecipientEmail",
					"ExternalReference", "UserLanguage", "LocationLatitude", "LocationLongitude",
					"Status"
				   )
multiF.df = multiF.df[, -which(colnames(multiF.df) %in% columnsToRemove)]

# Rename columns with new variables
newColNames = read.table(file.path(filesPath, "variables_new.csv"), sep = ",", header = T, col.names = c("Index", "ColumnName"))
colnames(multiF.df) = newColNames$ColumnName

# Subset on the rows where "DistributionChannel" is "anonymous" (rm 17 rows)
multiF.df = multiF.df[which(multiF.df$DistributionChannel == "anonymous"),]

# Remove the duplicated id rows (only keep row of first instance of id) (rm 42 rows)
multiF.df = multiF.df[!duplicated(multiF.df$id),]

# Filter on "NA" for CheckItem1 and CheckItem2 == 7 (rm 77 lines)
multiF.df = multiF.df[which(is.na(multiF.df$CheckItem1) & multiF.df$CheckItem2 == 7),]
