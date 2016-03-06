library(faraway)
# set your fdir =" " to the directory that contains the data.
house.dat= read.csv("~/Documents/Michigan semester2/Stat500/problem set/PS9/house.csv", header=FALSE)
cName<-c("id", "price", "size","bath","halfbath","bed","age","garage","elem");
colnames(house.dat)<-cName;
attach(house.dat)
x=lm(price~bath*size+bed*size+halfbath*size+age+I(age^2)+garage+elem,data=house.dat)
cook=cooks.distance(x)
halfnorm(cook,nlab=5,ylab="cook's distance")
abline(h=4/80)
##
house1=house.dat[-c(31,67,75,22,36),]
y=lm(price~bath*size+bed*size+halfbath*size+age+I(age^2)+garage+elem,data=house1)
step(x)
step(y)
##
house.dat$bath=factor(house.dat$bath)
z=lm(price~bath+size+bed+halfbath+age+elem+bath:size,data=house.dat) 
house.dat$id[z$resid==max(z$resid)]
w=lm(price~bath+size+bed+halfbath+age+elem+bath:size+I(age^2),data=house.dat)
summary(w)
##
wx=lm(price~age+ elem+bed+ factor(bath)+ halfbath+ factor(bath)/size , house1)
confint(wx)
out1=lm(price~size + bed + halfbath + garage + elem + size:halfbath, data = house1)
summary(out1)
summary(wx)
##
out2=lm(price ~ size + bed + halfbath + garage + elem + size:bed + size:halfbath,house1)
out3=lm(price ~ size + bed + halfbath + I(age^2) + garage + elem + size:bed + size:halfbath)
out4=lm(price ~ bath + size + bed + halfbath + I(age^2) + garage + elem + size:bed + size:halfbath)
extractAIC(lm(out2),k=log(75))
extractAIC(lm(out3),k=log(75))
extractAIC(lm(out4),k=log(75))
extractAIC(lm(out1),k=log(75))
##CV
nn=dim(house1)[1]
pred.mat=matrix(NA,nn, 5)
set.seed(7489103)
for (ii in 1:nn){
  test.dat = data.frame(house1[ii,])
  tmp.model = lm(price~ age+ size+ elem+ bed+ factor(bath)+ halfbath+ factor(bath):size, house1, subset=(1:nn)[-ii])
  test.out =predict.lm(tmp.model, test.dat, type="response", se.fit=T)
  pred.mat[ii,1]= test.out$fit
  pred.mat[ii,2]= test.out$se.fit
  pred.mat[ii,3]= test.out$residual.scale
  pred.mat[ii,4]= (test.out$fit - test.dat$price)**2
  pred.mat[ii,5]= abs(test.out$fit - test.dat$price)/test.dat$price
}
locv.all.sum =sum(pred.mat[,4])
locv.all.qq =quantile(pred.mat[,4], c(.1, .25, .5, .75, .9))
locv.all.qq
out1=lm(price~size + bed + halfbath + garage + elem + size:halfbath, data = house1)
#
nn=dim(house1)[1]
pred.mat=matrix(NA,nn, 5)
set.seed(7489103)
for (ii in 1:nn){
  test.dat = data.frame(house1[ii,])
  tmp.model =lm(price ~ size + bed + halfbath + I(age^2) + garage + elem + size:bed + size:halfbath, house1,subset=(1:nn)[-ii])
  test.out =predict.lm(tmp.model, test.dat, type="response", se.fit=T)
  pred.mat[ii,1]= test.out$fit
  pred.mat[ii,2]= test.out$se.fit
  pred.mat[ii,3]= test.out$residual.scale
  pred.mat[ii,4]= (test.out$fit - test.dat$price)**2
  pred.mat[ii,5]= abs(test.out$fit - test.dat$price)/test.dat$price
}
locv.all.sum =sum(pred.mat[,4])
locv.all.qq =quantile(pred.mat[,4], c(.1, .25, .5, .75, .9))
locv.all.qq
locv.all.sum
summary(out2)
summary(out3)
summary(out4)

predict(out1,data.frame(bed=3,size=1.976125,elem="A",bath="2",halfbath=1),level=0.95,interval="predict",sub)
sub=subset(house2,bed=3,bath="2",halfbath=1)
##
house2=house1[,-1,-7]
out_2=lm(price~size + factor(bed) + halfbath + factor(bath)+garage + elem + size:halfbath, data = house2)
summary(out_2)
##
mean(size)
mean(garage)
mean(elem)
house1$elem
house1$bed=relevel(house1$bed,ref="3")
