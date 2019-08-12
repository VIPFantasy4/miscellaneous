%sigma=0
%miu=0
%p=1/(2*pi*sigma)^0.5*exp(-(x-miu)^2/2*sigma^2);

%likelihood= -100/2*log(2*pi)-100*log(sigma)-((X1-miu)'*(X1-miu))./(2*sigma^2);




% mean of the 2 random sets of data, and their variance
miu1=sum(X1)./100
sigma1=(((X1-miu1)'*(X1-miu1))./100)^0.5
miu2=sum(X2)./100
sigma2=(((X2-miu2)'*(X2-miu2))./100)^0.5

%set 200 points between -10 and 10
X0=linspace(-10,10,200)
%calculate the likelihood of the first set of points
y1=1/(2*pi*sigma1^2)^0.5*exp(-(X0-miu1).^2./2*sigma1^2);
%calculate the likelihood of the first set of points
y2=1/(2*pi*sigma2^2)^0.5*exp(-(X0-miu2).^2./2*sigma2^2);
% plot the likihood of both set of data
plot(X0,y1); 
xlim([-10 10])
ylim([0 0.4])
hold on
plot(X0,y2)
title('(a)Likelihoods')
xlabel('x')
ylabel('probability of x given Ci')
legend('C1','C2')

