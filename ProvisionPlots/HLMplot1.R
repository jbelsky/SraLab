xx <- c(-0.1419,0.1376)   #  <-- change to alter plot dims
yy <- c(16.8282,22.2647)   #  <-- change to alter plot dims
leg <- c(-0.1419,17.5078)   #  <-- change to alter legend location
x <- c(-0.1419,0.1376)   #  <-- x-coords for lines
y1 <- c(22.2647,18.0191)
y2 <- c(21.2009,17.8859)
y3 <- c(19.9898,17.7343)
plot(xx,yy,type='n',font=2,font.lab=2,xlab='x1',ylab='Y',main='HLM 2-Way Interaction Plot')
lines(x,y1,lwd=3,lty=1,col=1)
lines(x,y2,lwd=3,lty=5,col=2)
lines(x,y3,lwd=3,lty=6,col=3)
points(x,y1,col=1,pch=16)
points(x,y2,col=1,pch=16)
points(x,y3,col=1,pch=16)
legend(leg[1],leg[2],legend=c('W1(1)','W1(2)','W1(3)'),lwd=c(3,3,3),lty=c(1,5,6),col=c(1,2,3))
