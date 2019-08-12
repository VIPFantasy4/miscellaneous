Y=housing(:,14);
X=housing(:,6);
for step =1:5
    p=polyfit(X,Y,step);
    Y_cal=polyval(p,X);
    error(step)=(Y-Y_cal)'*(Y-Y_cal);
end

plot(1:5,error)
    