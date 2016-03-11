clear;
clc;
%% Real solution of 2-point boundary value problem
syms y0(x0)
syms eps0
Dy0 = diff(y0);
y0(x0) = dsolve(diff(y0, 2) == -(2*x0 + 1)/eps0 + y0/eps0, y0(0) == 0, y0(1) == 0);
y0(x0) = simplify(y0);

%% Numerical solution using Thomas algorithm
h = 1/32; % The step is chosen to be 1/32 
n = 1/h - 1;
b = zeros(1,n);
c = zeros(1,n);
a = zeros(1,n);

eps = 10^(-3);
alfa = 0;
beta = 0;
x = zeros(1,n);
for i = 1:n
    x(1,i) = i*h;
end
Q = zeros(1,n);
Q(1,:) = 1/eps;
W = zeros(1,n+2);
W(1,1) = alfa;
W(1,n+2) = beta;
R = zeros(1,n);
R = (2*x+1)/eps;
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
X(1,n+2) = 1;
for k = 1:n
    W(1,k+1) = w(1,k);
    X(1,k+1) = x(1,k);
end

%% Plots for comparison of Real solution and numerical solution
figure;
xsol = 0:0.01:1;
ysol = 2*xsol+1-(sinh((1-xsol)/sqrt(eps))+3*sinh(xsol/sqrt(eps)))/sinh(1/sqrt(eps));
plot(xsol,ysol,'blue');
set(gca,'XTick', 0:0.2:1);
set(gca,'YTick', -1:1:3);
hold on
plot(X,W,'green');
plot(X,W,'O','color','red');
title('Numerical solution for h = 1/32','FontSize',12,'FontWeight','bold')
xlabel('X','FontSize',12,'FontWeight','bold')
ylabel('Y','FontSize',12,'FontWeight','bold')