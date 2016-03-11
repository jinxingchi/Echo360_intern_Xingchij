clc;clear;
x=3;
y=0;
nmax=3;
n=0;
while n<=nmax
    fx=2*x;fy=2*y;
    gx=y;gy=x;
    A=[fx fy;gx gy];
    fxy=(x-1)^2+y^2-4;
    gxy=x*y-1;
    fprintf('n = %d   (x,y) = (%1.16e %1.16e)  f(x,y) = %1.16e  g(x,y) = %1.16e\n',n,x,y,fxy,gxy)
    B=[-fxy;-gxy];
    S=linsolve(A,B);
    x=S(1,1)+x;
    y=S(2,1)+y;
    n=n+1;
end