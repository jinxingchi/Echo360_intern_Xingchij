function fixpoint
a = 2; b = 3; maxiter = 10; 
x = 0.5*(a+b); % inital guess
p = sqrt(5);
for iter=1:maxiter
    x=g(x);
    fx=x^2-5;
    err=abs(p-x);
    fprintf('n = %d   x = %1.14e, fx = %1.14e, err = %1.14e\n',iter,x,fx,err)   

end

% function z=g(x)
% z=5/x;
% 
% function fixpoint2
% a = 2; b = 3; maxiter = 10; 
% x = 0.5*(a+b); % inital guess
% p = sqrt(5);
% for iter=1:maxiter
%     x=g(x);
%     fx=x^2-5;
%     err=abs(p-x);
%     fprintf('n = %d   x = %1.14e, fx = %1.14e, err = %1.14e\n',iter,x,fx,err)   
% 
% end
% end
% 
% function z=g(x)
% z=x-(x^2-5)/3;
% end