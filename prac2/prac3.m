% plot the polynomial fitting graph
plot(x,test(x));
ylim([-5,5]);
xlim([0,5]);
hold on
plot(x1, y1,'+')
fit1(x1,y1)
fit2(x1,y1)
fit3(x1,y1)
fit4(x1,y1)
fit5(x1,y1)
fit6(x1,y1)
fit7(x1,y1)
fit8(x1,y1)
fit9(x1,y1)
title('(a)Data and fitted polynomials')
