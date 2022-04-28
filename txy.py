import numpy as np
from matplotlib import pyplot as plt
def txy(name01,name02,T01,T02,a1,b1,c1,a2,b2,c2,P,dx,xd,Td):
    #Przygotowanie setu do obliczeń
    Data={}
    Data.setdefault(name01,{})
    Data[name01].setdefault('Temperature',[T01])
    Data[name01].setdefault('Antoine',[a1,b1,c1])
    Data.setdefault(name02,{})
    Data[name02].setdefault('Temperature',[T02])
    Data[name02].setdefault('Antoine',[a2,b2,c2])
    Calc={}
    if Data[name01]['Temperature']>Data[name02]['Temperature']:
        print(name02 + ' is more volatile than '+ name01)
        MV=name02
        LV=name01
    elif Data[name01]['Temperature']<Data[name02]['Temperature']:
        print(name01 + ' is more volatile than '+ name02)
        MV=name01
        LV=name02
    else:
        print('Incorrect data set')
    Calc={}
    Calc.setdefault(MV,Data[MV])
    Calc.setdefault(LV,Data[LV])
    print(Calc)
    x=np.arange(0,1+dx,dx)
    #Bubble Curve
    Tbubble=[]
    T=Calc[LV]['Temperature'][0]
    for i in range(0,len(x-1)):
        convergence=1
        while convergence>0.01:
            T=T-0.1
            convergence=abs(P-10**(Calc[MV]['Antoine'][0]-Calc[MV]['Antoine'][1]/(Calc[MV]['Antoine'][2]+T))*(1-x[i])-10**(Calc[LV]['Antoine'][0]-Calc[LV]['Antoine'][1]/(Calc[LV]['Antoine'][2]+T))*(x[i]))
        Tbubble.append(round(T,1))
    print(Tbubble)
    ##Dew Curve
    Tdew=[]
    T=Calc[LV]['Temperature'][0]
    for i in range(0,len(x-1)):
        convergence=1
        while convergence>0.01:
            T=T-0.1
            convergence=abs(P-((1-x[i])/(10**(Calc[MV]['Antoine'][0]-Calc[MV]['Antoine'][1]/(Calc[MV]['Antoine'][2]+T)))+(x[i])/(10**(Calc[LV]['Antoine'][0]-Calc[LV]['Antoine'][1]/(Calc[LV]['Antoine'][2]+T))))**(-1))
        Tdew.append(round(T,1))
    print(Tdew)
    ## PointCheck
    xlt=np.round((1/P-1/(10**(Calc[LV]['Antoine'][0]-Calc[LV]['Antoine'][1]/(Calc[LV]['Antoine'][2]+Td))))/(1/(10**(Calc[MV]['Antoine'][0]-Calc[MV]['Antoine'][1]/(Calc[MV]['Antoine'][2]+Td)))-(1/(10**(Calc[LV]['Antoine'][0]-Calc[LV]['Antoine'][1]/(Calc[LV]['Antoine'][2]+Td))))),3)
    xgt=np.round((1-(10**(Calc[LV]['Antoine'][0]-Calc[LV]['Antoine'][1]/(Calc[LV]['Antoine'][2]+Td))/P))/((10**(Calc[MV]['Antoine'][0]-Calc[MV]['Antoine'][1]/(Calc[MV]['Antoine'][2]+Td))/P)-(10**(Calc[LV]['Antoine'][0]-Calc[LV]['Antoine'][1]/(Calc[LV]['Antoine'][2]+Td))/P)),3)
    if xd>xlt and xd<xgt:
        print('We have VLE')
        VF=round((xd-xlt)/(xgt-xlt),3)
        LF=round((xgt-xd)/(xgt-xlt),3)
        print('Vapour fraction = '+str(VF)+', Liquid Fraction = '+str(LF)+ ', Mole fraction of '+str(MV)+' = '+str(xd)+', Mole fraction of '+str(MV)+' = '+str(round((1-xd),3)))
        print('Fraction of ' +str(MV)+' in vapour is equal to ' +str(xgt))
        print('Fraction of ' +str(MV)+' in liquid is equal to ' +str(xlt))
    elif xgt<xd and xlt<xd:
      print('Vapour fraction = 1, Liquid Fraction = 0, Mole fraction of '+str(MV)+' = '+str(xd)+', Mole fraction of '+str(LV)+' = '+str(round((1-xd),3)))
    elif xd<xlt and xd<xgt:
      print('Liquid Fraction = 1, Vapour fraction = 0 , Mole fraction of '+str(MV)+' = '+str(xd)+', Mole fraction of '+str(LV)+' = '+str(round((1-xd),3)))

    ## PointCheck
    # Wykres fazowy TXY
    plt.title("T-x-y") 
    plt.xlabel("mole fraction of " + str(MV)) 
    plt.ylabel("Temperature [*C]") 
    plt.plot(x,Tbubble,'r-')
    plt.plot(x,Tdew,'b--')
    plt.plot(xd,Td,'go')
    plt.plot(xgt,Td,'mo')
    plt.plot(xlt,Td,'mo')
    x2plot=[xlt,xgt]
    y2plot=[Td,Td]
    plt.plot(x2plot,y2plot,'k')
    plt.show()
txy('octane','hexane',79,138,4.04867,1355.13,209.367,4.00266,1171.53,224.216,1.4,0.05,0.37,110)