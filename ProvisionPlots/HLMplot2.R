xx <- c(-0.1246,0.1277)   #  <-- change to alter plot dims
yy <- c(17.7012,21.7942)   #  <-- change to alter plot dims
leg <- c(-0.1246,18.2128)   #  <-- change to alter legend location
x <- c(-0.1246,0.1277)   #  <-- x-coords for lines
y1 <- c(21.7942,18.3834)
y2 <- c(20.4462,18.4505)
y3 <- c(19.6286,18.4912)
plot(xx,yy,type='n',font=2,font.lab=2,xlab='x1',ylab='Y',main='HLM 2-Way Interaction Plot')
lines(x,y1,lwd=3,lty=1,col=1)
lines(x,y2,lwd=3,lty=5,col=2)
lines(x,y3,lwd=3,lty=6,col=3)
points(x,y1,col=1,pch=16)
points(x,y2,col=1,pch=16)
points(x,y3,col=1,pch=16)
legend(leg[1],leg[2],legend=c('W1(1)','W1(2)','W1(3)'),lwd=c(3,3,3),lty=c(1,5,6),col=c(1,2,3))
