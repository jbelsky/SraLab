# Set the input parameters
xleft = -0.3
xright = 0.3
ylow = 12
yhigh = 25
plot_type = "Companionship"


param.df = read.table(paste0(plot_type, ".cfg"), sep = "\t", header = T)

# Define the functions
CalculateSlopeAndYinter = function(ARG_X_PAIR, ARG_Y_PAIR){

	# Get the slope
	ydiff = ARG_Y_PAIR[1] - ARG_Y_PAIR[2]
	xdiff = ARG_X_PAIR[1] - ARG_X_PAIR[2]

	m = ydiff / xdiff

	# Get the y-intercept
	b = ARG_Y_PAIR[1] - m * ARG_X_PAIR[1]

	# Return the slope and y-intercept
	return(c(m, b))

}

# Get the y-coordinates at the edge of the graphs
GetYCoords = function(ARG_LINE_PARAMS, ARG_X_PAIR){

	# Unpack the line parameters
	m = ARG_LINE_PARAMS[1]
	b = ARG_LINE_PARAMS[2]

	# Get the y-value at each x-value
	y_pair = m * ARG_X_PAIR + b

	return(y_pair)

}

# Make the plot
MakePlot = function(ARG_CHART, ARG_X_PAIR, ARG_Y_PAIR, ARG_Y_LIST, ARG_SAVE_PNG = F){

	if(ARG_SAVE_PNG){
		png(file = paste0(ARG_CHART, ".png"), width = 7, height = 7, units = "in", res = 300)
	}

	# Initialize the plot
	par(mar = c(5, 5, 2, 2),family = "serif")
	plot(0, 0, type='n',
		 xlab = "", ylab = "", main = "",
		 xlim = ARG_X_PAIR, xaxt = "n",
		 ylim = ARG_Y_PAIR
		)

	# Set the axes
	axis(1, at = seq(-0.95, 0.95, 0.1), labels = F, tcl = par()$tcl * 0.7)
	axis(1, at = seq(-1, 1, 0.1))
	axis(2, at = seq(11, 25, 2), labels = F, tcl = par()$tcl * 0.7)
	axis(2, at = seq(10, 26, 2))
	title(ylab = "Loneliness", xlab = paste0("Child-Level ", ARG_CHART, " Received (SG)"), cex.lab = 1)

	# Draw the lines
	for(i in 1:3){
		lines(ARG_X_PAIR, ARG_Y_LIST[[i]], lwd=3, lty=i)
	}

	legend("bottomleft",
		   legend = sapply(
							c(bquote(paste("Low-", .(ARG_CHART), " Class (", 20^th, " Percentile)")),
		   			  		  bquote(paste("Average-", .(ARG_CHART), " Class (", 50^th, " Percentile)")),
		   			          bquote(paste("High-", .(ARG_CHART), " Class (", 80^th, " Percentile)"))
					         ), 
                            as.expression
                           ),
		   lwd = 3, lty = c(1, 2, 3),
		   bty = "n"
		  )

	if(ARG_SAVE_PNG){
		dev.off()
	}

}

# Initialize the ycoord list
y.l = vector(mode = "list", 3)

# Get the x-coordinates
x = as.numeric(param.df[which(param.df$pts == "x"), 2:3])
xpair = c(xleft, xright)
for(i in 1:3){

	# Get the y coordinates
	ycoords = as.numeric(param.df[(i+1), 2:3])

	# Get the line parameters
	lparam = CalculateSlopeAndYinter(x, ycoords)

	# Get the y-coordinates for the pair
	y.l[[i]] = GetYCoords(lparam, xpair)

}

MakePlot(plot_type, xpair, c(ylow, yhigh), y.l, T)
