# Function for generating density function of double exponential
ddexp <- function(x,mu,lambda){dexp <- .5*lambda*exp(-abs(x-mu)*lambda)}

# Function for generating cdf of double exponential
pdexp <- function(x,mu,lambda){
cdf1 <- .5*exp(-abs(x-mu)*lambda)
cdf1[x>mu] <- 1-cdf1[x>mu]
cdf1 
}

# Function for generating quantile of double exponential
qdexp <- function(p,mu,lambda){
quant1 <- qexp(0*p,lambda) + mu
pn <- p[p<.5]
pp <- p[p>.5]
quant1[p>.5] <- qexp(2*pp-1,lambda) + mu
quant1[p<.5] <- -qexp(1-2*pn,lambda) + mu
quant1 
}

# Function for generating random deviates of double exponential
rdexp <- function(n,mu,lambda){
rexp <- rexp(n,lambda)
rbin <- 2*rbinom(n,1,.5)-1
x <- rexp*rbin+mu
}

# Function for generating QQ Plot for double exponential
qqdexp <- function(x){
mu <- median(x)
lambda <- 1/mean(abs(x-mu))
xsort <- sort(x)
n <- length(x)
q <- (c(1:n)-.5)/n
qq <- qdexp(q,0,1)
plot(qq,xsort,xlab='Theoretical Quantiles - unit rate',ylab='Sample Quantiles',main='Double Exponential Q-Q Plot')
lines(qq,((1/lambda)*qq+mu))
}

# Function for generating QQ Plot for exponential
qqexp <- function(x){
lambda <- 1/mean(x)
xsort <- sort(x)
n <- length(x)
q <- (c(1:n)-.5)/n
qq <- qexp(q,1)
plot(qq,xsort,xlab='Theoretical Quantiles - unit rate',ylab='Sample Quantiles',main='Exponential Q-Q Plot')
lines(qq,(1/lambda)*qq)
}

# Function for generating QQ Plot for normal with line
myqqnorm <- function(x){
qqnorm(x)
qqline(x)
}
source("startup.R")
x1=qdexp(0.55,0,3)
x=1/x1
x


