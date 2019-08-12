% plot(x2, y2,'+')
%sum_error=[]


% calculate the sum of error using train setting to test data 
for n= 1:9
    p=polyfit(x1,y1,n);
    y_es=polyval(p,x2);
    sum_error(n)=(y2-y_es)'*(y2-y_es);
end
% calculate the sum of error of the train data
for n= 1:9
    p=polyfit(x1,y1,n);
    y_es=polyval(p,x1);
    sum_error_train(n)=(y1-y_es)'*(y1-y_es);
end

% plot the graph
hold on 
plot (1:9,sum_error_train)
plot(1:9, sum_error,'r')
title('(b)Error vs. polynomial order')
legend('Training','Validation')