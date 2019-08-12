% create x axis
x=linspace(0,5,100);
plot(x,test(x));
ylim([-5,5]);
xlim([0,5]);
hold on
%create random number on x axis and create random normal distribiution 
%number on the function
x1= 5*rand([20 1]);
y1= test(x1)+randn([20 1]);
plot(x1, y1,'+')
title ('(a)Data and fitted polynomials')
% pop up curve fiting tool
cftool(x1,y1);