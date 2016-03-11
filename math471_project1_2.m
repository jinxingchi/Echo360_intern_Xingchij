clear;
clc;

T = 100;
E = 1.3*10^6;
I = 256;
w0 = 20/12;
L = 6*12;
%% Real solution of 1D beam deformation
syms y0(x0)
Dy0 = diff(y0);
y0(x0) = dsolve(diff(y0, 2) == -(w0/(2*E*I))*x0*(L-x0) + y0*T/(E*I), y0(0) == 0, y0(L) == 0);
y0(x0) = simplify(y0);

figure;
xsol = 0:0.5:L;
ysol = zeros(1,length(xsol));
for i = 1:length(xsol)
ysol(i) = (88544371553805857625*xsol(i))/147573952589676412928 - ...
    (9838263505978428625*xsol(i)^2)/1180591620717411303424 + ...
    (15987178197214946515625*exp((130^(1/2)*xsol(i))/20800))/(288230376151711744*(exp((9*130^(1/2))/2600) + 1)) + ...
    (15987178197214946515625*exp((9*130^(1/2))/2600)*exp(-(130^(1/2)*xsol(i))/20800))/(288230376151711744*(exp((9*130^(1/2))/2600) + 1)) - ...
    15987178197214946515625/288230376151711744; % Plot the real solution curve by showing several evaluated points on the curve.
end
plot(xsol,ysol,'blue','LineWidth',6);
set(gca,'XTick', 0:12:L);
hold on
title('Deflection VS X coordinate','FontSize',12,'FontWeight','bold')
xlabel('X coordinate [inch]','FontSize',12,'FontWeight','bold')
ylabel('Deflection, Y component [inch]','FontSize',12,'FontWeight','bold')

%% Numerical solution of 1D beam deformation with mesh size from 1/72 to 1/18 inch.
interval = 1;
h = interval/L;
n = 1/h - 1;
b = zeros(1,n);
c = zeros(1,n);
a = zeros(1,n);

alfa = 0;
beta = 0;
x = zeros(1,n);
for i = 1:n
    x(1,i) = i*h;
end
Q = zeros(1,n);
Q(1,:) = T/(E*I);
W = zeros(1,n+2);
W(1,1) = alfa;
W(1,n+2) = beta;
R = zeros(1,n);
R = (w0/(2*E*I))*(x*L^2-x.*x*L^2);
r = R;
r(1,1) = R(1,1) + alfa/(h^2);
r(1,n) = R(1,n) + beta/(h^2);

b = Q+2/(h^2);
a(1,:) = -1/(h^2);
a(1,1) = 0;
c(1,:) = -1/(h^2);

u = zeros(1,n);
l = zeros(1,n);
u(1,1) = b(1,1);
for k = 2:n
    l(1,k) = a(1,k)/u(1,k-1);
    u(1,k) = b(1,k)-l(1,k)*c(1,k-1);
end

z = zeros(1,n);
z(1,1) = r(1,1);
for k = 2:n
    z(1,k) = r(1,k) - l(1,k)*z(1,k-1);
end

w = zeros(1,n);
w(1,n) = z(1,n)/u(1,n);
for k = (n-1:-1:1)
    w(1,k) = (z(1,k) - c(1,k)*w(1,k+1))/u(1,k);
end

X = zeros(1,n+2);
X(1,1) = 0;
X(1,n+2) = L;
for k = 1:n
    W(1,k+1) = w(1,k)*L^2;
    X(1,k+1) = x(1,k)*L;
end

plot(X,4*W/5,'green','LineWidth',4);

interval = 2;
h = interval/L;
n = 1/h - 1;
b = zeros(1,n);
c = zeros(1,n);
a = zeros(1,n);

alfa = 0;
beta = 0;
x = zeros(1,n);
for i = 1:n
    x(1,i) = i*h;
end
Q = zeros(1,n);
Q(1,:) = T/(E*I);
W = zeros(1,n+2);
W(1,1) = alfa;
W(1,n+2) = beta;
R = zeros(1,n);
R = (w0/(2*E*I))*(x*L^2-x.*x*L^2);
r = R;
r(1,1) = R(1,1) + alfa/(h^2);
r(1,n) = R(1,n) + beta/(h^2);

b = Q+2/(h^2);
a(1,:) = -1/(h^2);
a(1,1) = 0;
c(1,:) = -1/(h^2);

u = zeros(1,n);
l = zeros(1,n);
u(1,1) = b(1,1);
for k = 2:n
    l(1,k) = a(1,k)/u(1,k-1);
    u(1,k) = b(1,k)-l(1,k)*c(1,k-1);
end

z = zeros(1,n);
z(1,1) = r(1,1);
for k = 2:n
    z(1,k) = r(1,k) - l(1,k)*z(1,k-1);
end

w = zeros(1,n);
w(1,n) = z(1,n)/u(1,n);
for k = (n-1:-1:1)
    w(1,k) = (z(1,k) - c(1,k)*w(1,k+1))/u(1,k);
end

X = zeros(1,n+2);
X(1,1) = 0;
X(1,n+2) = L;
for k = 1:n
    W(1,k+1) = w(1,k)*L^2;
    X(1,k+1) = x(1,k)*L;
end

plot(X,2*W/3,'yellow','LineWidth',4);
%plot(X,2*W/3,'O','color','yellow','LineWidth',4);

interval = 4;
h = interval/L;
n = 1/h - 1;
b = zeros(1,n);
c = zeros(1,n);
a = zeros(1,n);

alfa = 0;
beta = 0;
x = zeros(1,n);
for i = 1:n
    x(1,i) = i*h;
end
Q = zeros(1,n);
Q(1,:) = T/(E*I);
W = zeros(1,n+2);
W(1,1) = alfa;
W(1,n+2) = beta;
R = zeros(1,n);
R = (w0/(2*E*I))*(x*L^2-x.*x*L^2);
r = R;
r(1,1) = R(1,1) + alfa/(h^2);
r(1,n) = R(1,n) + beta/(h^2);

b = Q+2/(h^2);
a(1,:) = -1/(h^2);
a(1,1) = 0;
c(1,:) = -1/(h^2);

u = zeros(1,n);
l = zeros(1,n);
u(1,1) = b(1,1);
for k = 2:n
    l(1,k) = a(1,k)/u(1,k-1);
    u(1,k) = b(1,k)-l(1,k)*c(1,k-1);
end

z = zeros(1,n);
z(1,1) = r(1,1);
for k = 2:n
    z(1,k) = r(1,k) - l(1,k)*z(1,k-1);
end

w = zeros(1,n);
w(1,n) = z(1,n)/u(1,n);
for k = (n-1:-1:1)
    w(1,k) = (z(1,k) - c(1,k)*w(1,k+1))/u(1,k);
end

X = zeros(1,n+2);
X(1,1) = 0;
X(1,n+2) = L;
for k = 1:n
    W(1,k+1) = w(1,k)*L^2;
    X(1,k+1) = x(1,k)*L;
end

plot(X,W/2,'red','LineWidth',4);
%plot(X,W/2,'O','color','red','LineWidth',4);
legend ('Real deflection value','0.8*deflection (interval:1 inch)','0.75*deflection (interval:2 inches)','0.5*deflection (interval: 4 inches)')

%% Error analysis
%mod = max(abs(ysol-W));
%modh = max(abs(ysol-W))/h;
%modh2 = max(abs(ysol-W))/h^2;
%modh3 = max(abs(ysol-W))/h^3;