miu_t1=sum(iris(1:50,1))/50;
miu_t2=sum(iris(51:100,1))/50;
sigma_t1= (((iris(1:50,1)-miu_t1)'*(iris(1:50,1)-miu_t1))./50)^0.5;
sigma_t2= (((iris(51:100,1)-miu_t2)'*(iris(51:100,1)-miu_t2))./50)^0.5;

X0=linspace(4,7,200);
prob_t1= 1/(2*pi*sigma_t1)^0.5*exp(-(X0-miu_t1).^2/(2*sigma_t1^2));
prob_t2= 1/(2*pi*sigma_t2)^0.5*exp(-(X0-miu_t2).^2/(2*sigma_t2^2));

figure
subplot(2,1,1)
plot(X0,prob_t1)
hold on
plot (X0,prob_t2)
title('likelihood')

t1_post=0.5*prob_t1./(0.5*prob_t1+0.5*prob_t2)
t2_post=0.5*prob_t2./(0.5*prob_t1+0.5*prob_t2)

subplot(2,1,2)
plot(X0,t1_post)
hold on
plot(X0,t2_post,'r*')
title('posterior')