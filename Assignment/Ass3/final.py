import pylab

W = [15.69, 5.68, 3.87, 5.79, 13.05, 4.30, 6.45, 8.33, 5.26, 4.36] # Rainfall

def discretize(year,retain):
    x = round(retain)
    return farm(year,x)[0]

def Profit(Yield, apply):      # Annual profit
    if apply > 0:
        return Yield * 0.01 -  apply* 0.10 - 1        
    else:
        return Yield * 0.01
        
def Yield(year,retain,apply):
    return (-476.25 - 5.5042*(retain+apply) + 245.049*W[year] + 0.00433*(retain+apply)**2
            - 9.9584*W[year]**2 + 2.4524*(retain+apply)*W[year] -
            0.00336*(retain+apply)**2*W[year] - 0.03314*(retain+apply)*W[year]**2)

def R(year, retain, apply):
    return 3.9209*(apply + retain)**1.0405*W[year]**-1.1566

farms = {}      
def farm(year,retain):   #  Find application for year to optimise profit by 2016
    if not (year,retain) in farms:
        if year >= 10:
            return (0,"The maximal years have been reached")
        else:
            farms[year,retain] = max((Profit(Yield(year,retain,a), a) 
                                             + discretize(year+1,R(year,retain,a)), 
                                        'Retain ', round(R(year,retain,a)),'Apply ', a) for a in range(300))
    return farms[year,retain]

                                        ############################
                                        ########### Q2 #############
                                        ############################

W2 = [[10.5,13.0,9.0,15.0,6.5,2.0,4.0,4.5,8.0,4.0],   # High rainfall
     [17.5,17.0,10.5,19.0,8.5,4.5,6.0,8.0,9.0,7.5]]   # Low rainfall
     
def discretize2(year,retain):
    x = round(retain)
    return farm2(year,x)[0]

def Yield2(year,retain,apply,lohi):
    return (-476.25 - 5.5042*(retain+apply) + 245.049*W2[lohi][year] + 0.00433*(retain+apply)**2
            - 9.9584*W2[lohi][year]**2 + 2.4524*(retain+apply)*W2[lohi][year] -
            0.00336*(retain+apply)**2*W2[lohi][year] - 0.03314*(retain+apply)*W2[lohi][year]**2)

def R2(year, retain, apply,lohi):
    return 3.9209*(apply + retain)**1.0405*W2[lohi][year]**-1.1566

        
farms2 = {}
def farm2(year,retain): #  Find application for year to optimise profit by 2027
    if not (year,retain) in farms2:
        if year >= 10:
            return (0,"Outside of 2018-2027 projection range")
            
        else:
            farms2[year,retain] = max((0.6*(Profit(Yield2(year,retain,a,0), a) +
                    discretize2(year+1,R2(year,retain,a,0))) + 
                    0.4*(Profit(Yield2(year,retain,a,1), a) +
                    discretize2(year+1,R2(year,retain,a,1))),
                    'apply:', a) for a in range(205))
            
    return farms2[year,retain]

def ApplyThresHold(i,t):
    return farm2(i,t)[2]

def draw(): # To draw all graphs
    i = 0
    while i < 10:   
        thresholds = [ApplyThresHold(i,t) for t in range(205)]
        pylab.plot(range(205), thresholds)
        pylab.xlabel('Retained nitrogen beginning year ' + str(i + 2018))        
        pylab.ylabel ('Optimal application') 
        pylab.title('Year ' + str(i + 2018))
        pylab.show()
        i +=1