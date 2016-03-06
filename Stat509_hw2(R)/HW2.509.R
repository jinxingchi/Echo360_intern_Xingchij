library(fExtremes)
##1.(a)
x=seq(0,10,by=0.01)
plot(pgpd(x,xi=0.5,mu=0,beta=1,lower.tail=FALSE),ylim=c(0,1),type="l",col="red",xlab="x",ylab="Tail Probability",main="Tail probability of Pareto Dist.")

xi_seq=c(2,10)
col_seq=c("green","blue")
for (i in 1:2){ 
  F_x<-pgpd(x,xi=xi_seq[i],mu=0,beta=1,lower.tail=FALSE)
  lines(F_x,ylim=c(0,1),type="l",col=col_seq[i])
  }
legend("topright",c("xi=0.5","xi=2","xi=10"),title="Probability",lty=1,lwd=2,col=c("red","green","blue"),bg="grey90",cex=0.7)
##2
##Problem 1,2
data(EuStockMarkets)
mode(EuStockMarkets)
class(EuStockMarkets)
plot(EuStockMarkets)
logR=diff(log(EuStockMarkets))
plot(logR)
##problem3
plot(as.data.frame(logR))
index.names=dimnames(logR)[[2]]
par(mfrow=c(2,2))
for (i in 1:4)
{
  qqnorm(logR[,i],datax=T,main=index.names[i])
  qqline(logR[,i],datax=T)
 print(shapiro.test(logR[,i]))
}

n=dim(logR)[1]
q.grid = (1:n)/(n+1)
df=c(1,4,6,10,20,30)
for(i in 1:4)
{
  windows()
  par(mfrow=c(3,2))
  for(j in 1:6)
  {
    qqplot(logR[,i], qt(q.grid,df=df[j]),
           main=paste(index.names[i], ", df=", df[j]) )
    abline(lm(qt(c(.25,.75),df=df[j])~quantile(logR[,i],c(.25,.75))))
  } }

##Problem 5
library("fGarch")
x=seq(-.1,.1,by=.001)
par(mfrow=c(1,1))
plot(density(logR[,1]),lwd=2,ylim=c(0,60))
lines(x,dstd(x,mean=median(logR[,1]),sd=mad(logR[,1]),nu=5),
      lty=5,lwd=2)
lines(x,dnorm(x,mean=mean(logR[,1]),sd=sd(logR[,1])),
      lty=3,lwd=4)
legend("topleft",c("KDE","t: df=5","normal"),lwd=c(2,2,4),
       lty=c(1,5,3))

##Problem6
library("fGarch")
x=seq(-.1,.1,by=.001)
par(mfrow=c(1,2))
plot(density(logR[,1],adjust=3),lwd=2,ylim=c(0,1),xlim=c(0.02,0.06),main="Right Tail_adjust=3")
lines(x,dstd(x,mean=median(logR[,1]),sd=mad(logR[,1]),nu=5),
      lty=5,lwd=2)
lines(x,dnorm(x,mean=mean(logR[,1]),sd=sd(logR[,1])),
      lty=3,lwd=4)
legend("topright",c("KDE","t: df=5","normal"),lwd=c(2,2,4),cex=0.5,
       lty=c(1,5,3))

plot(density(logR[,1],adjust=3),lwd=2,ylim=c(0,1),xlim=c(-0.1,-0.03),main="Left Tail_adjust=3")
lines(x,dstd(x,mean=median(logR[,1]),sd=mad(logR[,1]),nu=5),
      lty=5,lwd=2)
lines(x,dnorm(x,mean=mean(logR[,1]),sd=sd(logR[,1])),
      lty=3,lwd=4)
legend("topleft",c("KDE","t: df=5","normal"),lwd=c(2,2,4),cex=0.5,
       lty=c(1,5,3))
 

###Problem 3
##(1)
XX=read.csv("~/Documents/Michigan semester2/Stat 509/homework 2/Nasdaq100_dailydata_92-12.csv",header=TRUE)
ND100_day<-rev(X$Adj.Close)
Nasdaq100_day_lreturn <- diff(log(ND100_day))
mean(Nasdaq100_day_lreturn)
median(Nasdaq100_day_lreturn)
var(Nasdaq100_day_lreturn)
skewness(Nasdaq100_day_lreturn)
kurtosis(Nasdaq100_day_lreturn)
##(2)
Dasdaq_latest<-Nasdaq100_day_lreturn[1:1000]
shapiro.test(Dasdaq_latest)
    
##(3)
setwd("~/Documents/Michigan semester2/Stat 509/homework 2")
source("startup.R")
par(mfrow=c(1,1))
qqdexp(Nasdaq100_day_lreturn)
##(4)
qqt <- function(x,y){
  xsort <- sort(x)
  n <- length(x)
  q.grid <- (c(1:n)-.5)/n
  df <- y
  qq <- qt(q.grid,df)
  plot(qq,xsort,xlab='Theoretical Quantiles',ylab='Sample Quantiles',main = paste( "QQ t-plot, df=", df)
  )
  abline(lm(quantile(xsort,c(.05,.95))~qt(c(.05,.95),df)))
}

df_est <- c(2, 3, 4, 10)
par(mfrow=c(2,2))
for (i in 1:length(df_est)){
  qqt(Nasdaq100_day_lreturn,df_est[i])
}

