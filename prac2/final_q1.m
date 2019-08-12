plot(x2, y2,'+')
%sum_error=[]
for n= 1:9
    p=polyfit(x1,y1,n);
    y_es=polyval(p,x2);
    sum_error(n)=(y2-y_es)'*(y2-y_es);
end

for n= 1:9
    p=polyfit(x1,y1,n);
    y_es=polyval(p,x1);
    sum_error_train(n)=(y1-y_es)'*(y1-y_es);
end

plot(1:9, sum_error)
hold on 
plot (1:9,sum_error_train,'r')