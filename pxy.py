import numpy as np
from matplotlib import pyplot as plt
ComponentDataSet={}
def pxy(name01,name02,p01,p02,dx,xd,pd):
    print('Saturation pressure of ' + name01 +' is ' +str(p01)+' bar')
    print('Saturation pressure of ' + name02 +' is ' +str(p02)+' bar')
    #Generacja ciśnień saturacji
    if p01>p02:
        p1=p01
        p2=p02
        name1=name01
        name2=name02
    elif p01<p02:
        p1=p02
        p2=p01
        name1=name02
        name2=name01
    else:
        print('Incorrect data set')
    print(name1 +' is more volatile than ' + name2)
    ComponentDataSet[name1]={}
    ComponentDataSet[name2]={}
    #Generacja ciśnień parcjalnych i całkowitych zgodnie z prawem Raoulta
    x=np.arange(0,1+dx,dx)
    PartialPressure1=np.round(p1*x,3)
    PartialPressure2=np.round(p2*(1-x),3)
    ComponentDataSet[name1].setdefault('partial pressure1',list(PartialPressure1))
    ComponentDataSet[name2].setdefault('partial pressure2',list(PartialPressure2))
     #Ciśnienie całkowite z prawa Raoulta
    RaoultPressure=[]
    for i in range(0,len(x-1)):
      P=0
      P=np.round(PartialPressure1[i]+PartialPressure2[i],3)
      RaoultPressure.append(P)
    DataSet={}
    DataSet.setdefault('Raoult',list(RaoultPressure))
    #Ciśnienie całkowite z prawa Raoulta
    RealPressure=[]
    for i in range(0,len(x-1)):
      P=0
      P=np.round(1/(x[i]/p1+(1-x[i])/p2),3)
      RealPressure.append(P)
    DataSet.setdefault('RealPressure',list(RealPressure))
    #Generacja reguły dźwigni
    # Sprawdzenie czy punkt leży w zakresie równowagi ( obliczenie teoretycznej wartości x i P przy znanych P oraz x i sprawdzenie położenia puktu)
    xgt=np.round((1/pd-1/p2)/(1/p1-1/p2),4)
    xlt=np.round((pd-p2)/(p1-p2),4)
    if xgt>xd and xlt<xd:
      print('We have a VLE')
      VF=round((xd-xlt)/(xgt-xlt),3)
      LF=round((xgt-xd)/(xgt-xlt),3)
      print('Vapour fraction = '+str(VF)+', Liquid Fraction = '+str(LF)+ ', Mole fraction of '+str(name1)+' = '+str(xd)+', Mole fraction of '+str(name2)+' = '+str(round((1-xd),3)))
      print('Fraction of ' +str(name1)+' in vapour is equal to ' +str(xgt))
      print('Fraction of ' +str(name1)+' in liquid is equal to ' +str(xlt))
    elif xgt<xd and xlt<xd:
      print('Vapour fraction = 1, Liquid Fraction = 0, Mole fraction of '+str(name1)+' = '+str(xd)+', Mole fraction of '+str(name2)+' = '+str(round((1-xd),3)))
    elif xd<xlt and xd<xgt:
      print('Liquid Fraction = 1, Vapour fraction = 0 , Mole fraction of '+str(name1)+' = '+str(xd)+', Mole fraction of '+str(name2)+' = '+str(round((1-xd),3)))
    # Wykres fazowy PXY
    plt.title("P-x-y") 
    plt.xlabel("mole fraction of " + str(name1)) 
    plt.ylabel("Pressure") 
    plt.plot(x,RaoultPressure,'r-')
    plt.plot(x,RealPressure,'b--')
    plt.plot(xd,pd,'go')
    plt.plot(xgt,pd,'mo')
    plt.plot(xlt,pd,'mo')
    x2plot=[xlt,xgt]
    y2plot=[pd,pd]
    plt.plot(x2plot,y2plot,'k')
    plt.autoscale(enable=True, axis='both', tight=True)
    plt.show()
pxy('octane','hexane',0.7,2.9,0.001,0.6,1.5)