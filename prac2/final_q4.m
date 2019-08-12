%load('iris.csv')

%calculate the mean of the first and second flowers and their variance
miu_t1=sum(iris(1:50,1))/50;
miu_t2=sum(iris(51:100,1))/50;
sigma_t1= (((iris(1:50,1)-miu_t1)'*(iris(1:50,1)-miu_t1))./50)^0.5;
sigma_t2= (((iris(51:100,1)-miu_t2)'*(iris(51:100,1)-miu_t2))./50)^0.5;

%generate a set of x
X0=linspace(4,7,200);
%calculate the likelihood of type 1 and type2 flowers given a fix x
prob_t1= 1/(2*pi*sigma_t1)^0.5*exp(-(X0-miu_t1).^2/(2*sigma_t1^2));
prob_t2= 1/(2*pi*sigma_t2)^0.5*exp(-(X0-miu_t2).^2/(2*sigma_t2^2));

% plot the first plot
figure
subplot(2,1,1)
plot(X0,prob_t1)
hold on
plot (X0,prob_t2)
title('(a)Likelihoods')
xlabel('x')
ylabel('probability of x given certain type')
legend('type1','type2')

% calculate the posterior probability of type1 flower
t1_post=0.5*prob_t1./(0.5*prob_t1+0.5*prob_t2)
% calculate the posterior probability of type2 flower
t2_post=0.5*prob_t2./(0.5*prob_t1+0.5*prob_t2)

% plot the second figure
subplot(2,1,2)
plot(X0,t1_post)
hold on
plot(X0,t2_post,'r*')
title('(b)Posteriors with equal priors')
xlabel('x')
ylabel('prosterior probability given fix x')
legend('type1','type2')