xx <- c(0.2196,0.4648)   #  <-- change to alter plot dims
yy <- c(15.9103,20.9087)   #  <-- change to alter plot dims
x <- c(0.2196,0.4648)   #  <-- x-coords for lines
y1 <- c(20.9087,16.7433)
y2 <- c(20.528,17.254)
y3 <- c(19.9591,18.0174)

slope = c(-16.99, -13.35, -7.92)
yintercept = c(24.63, 23.45, 21.68)

# Get the corresponding y coordinates for each line
x1 = 0
x2 = 0.85
y1 = numeric(3)
y2 = numeric(3)
for (i in 1:3) {
  y1[i] = slope[i] * x1 + yintercept[i]
  y2[i] = slope[i] * x2 + yintercept[i]
}


png(file = "c:/Users/jab112/Desktop/Mollaulasher.png",
    width = 7,
    heigh = 7,
    units = "in",
    res = 300
    )
par(mar = c(5, 5, 2, 2),family = "serif")
plot(0,0,type='n',
     xlab = "",
     ylab = "",
     main = "",
     xlim = c(0, 0.85),
     xaxt = "n",
     ylim = c(10.1885, 24.63)
    )
axis(1, at = seq(0.1, 0.7, 0.2), labels = F, tcl = par()$tcl * 0.7)
axis(1, at = seq(0, 0.8, 0.2), labels = c("0", "0.2", "0.4", "0.6", "0.8"))
axis(2, at = seq(12.5, 22.5, 5), labels = F, tcl = par()$tcl * 0.7)
title(ylab = "Loneliness", xlab = "Child-Level Provisions Received (SG)", cex.lab = 1)

for (i in 1:3){
  lines(x = c(x1, x2), y = c(y1[i], y2[i]), lwd = 2, lty = i)
}

#lines(x,y1,lwd=3,lty=1)
#lines(x,y2,lwd=3,lty=2)
#lines(x,y3,lwd=3,lty=3)
legend("bottomleft",
       legend = c(expression(paste("Low-Provisions Class (20"^"th", " Percentile)")),
                  expression(paste("Average-Provisions Class (50"^"th", " Percentile)")),
                  expression(paste("High-Provisions Class (80"^"th", " Percentile)"))
                  ),
       lwd = 3, lty = c(1, 2, 3),
       bty = "n"
      )

dev.off()
