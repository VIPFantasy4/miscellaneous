%X_POST=linspace(-10,10,200)
Y_POST1=0.5*y1./(0.5*y1+0.5*y2);
Y_POST2=0.5*y2./(0.5*y1+0.5*y2);
plot(X0,Y_POST1)
hold on
plot(X0,Y_POST2,'r')