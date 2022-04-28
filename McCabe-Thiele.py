import numpy as np
import matplotlib.pyplot as plt
import math as mt
## MC_CABE-THIELE METHOD
def McCabeThiele(zf,xd,xw,R,q,alfa,eta,nx,name):
    ## Define input for plot
    plt.title("McCabe-Thiele method for " +str(name)+' fractional distillation') 
    plt.xlabel("x of " + str(name)) 
    plt.ylabel("y of " + str(name))
    print('We consider the process for: ' + name)
    ### DEFINE X=Y LINE
    y=[]
    x=np.linspace(0,1,nx)
    for i in range(0,len(x)):
        y.append(x[i])
    ## DEFINE VLE
    vle=[]
    for i in range(0,len(x)):
        vle.append((alfa*x[i])/(1+x[i]*(alfa-1)))
    ## DEFINE UPPER OPERATING LINE (UOL)
    uol=[]
    x_uol=np.linspace(0,xd,nx)
    for i in range(0,len(x_uol)):
        uol.append(R*x_uol[i]/(R+1)+xd/(R+1))   
    ## Q LINE VS UOL INTERSECTING
    if q==1:
        xins=zf
        yins=R*xins/(R+1)+xd/(R+1)
        xq=zf
        yq=zf
    elif q==0:
        yins=zf
        xins=(yins*(R+1)-xd)/R
        xq=zf
        yq=zf
    else:
        xins=(xd/(R+1)+zf/(q-1))*1/(q/(q-1)-R/(R+1))
        yins=R*xins/(R+1)+xd/(R+1)
        xq=zf
        yq=zf
    ## DEFINE LOWER OPERATING LINE (LOL)
    xdis=xins-xw
    xstrip=np.linspace(xw,xins)
    xcalc=np.linspace(0,xdis)
    lol=[]
    a=(yins-xw)/(xins-xw)
    for i in range(0,len(xcalc)):
        lol.append(a*xcalc[i]+xw)
    plt.plot(xstrip,lol)
    ## Stages
    yst=[xd,xd]
    xst=[xd]
    xc=xd
    yc=xd
    while yc>xw:
        xc=1/(alfa/yc-(alfa-1))
        xc=np.round(xc,decimals=3,out=None)
        xst.append(xc)
        if xc>=xins and xc>xw and xc<xd:
            xst.append(xc)
            yc=R*xc/(R+1)+xd/(R+1)
            yc=np.round(yc,decimals=3,out=None)
            yst.append(yc)
            yst.append(yc)
        elif xc<xins and xc>xw:
            xst.append(xc)
            xdis2=xc-xw
            yc=a*xdis2+xw
            yc=np.round(yc,decimals=3,out=None)
            yst.append(yc)
            yst.append(yc)
        elif xc<xw:
            yc=xc
            yc=np.round(yc,decimals=3,out=None)
    ## THEORETICAL STAGES AND PHYSICAL STAGES
    N=np.round(len(yst)/2,decimals=2,out=None)
    print('We have ' +str(N) + ' stages')
    ## FEED
    xunique=list(set(xst))
    print(xunique)
    for i in range(0,len(xunique),1):
        if xunique[i]<xq:
            xminimum=xunique[i]
            aa=abs(xq-xunique[i])
            AA=abs(xunique[i]-xunique[i-1])
            stage=i
            break
        else:
            continue
    Nf=np.round(stage+aa/AA-1,decimals=2,out=None)
    Nfl=mt.ceil(Nf/eta)
    print('Feed location: ' + str(Nfl)+' stage')
    ## RESIDUE
    xres=xunique[-1]
    bb=abs(xres-xw)
    BB=abs(xres-xunique[-2])
    stageres=len(xunique)-2
    Nres=np.round(stageres+bb/BB,decimals=2,out=None)
    print('Residue location: ' + str(Nres)+' stage')
    ## STAGES IN COLUMN AND PHYSICAL STAGES
    Nincol=Nres-2
    print('Stages in column: ' + str(Nincol)+' stages')
    Nphys=mt.ceil(Nincol/eta)
    print('Physical stages: ' + str(Nphys)+' stages')
    ## PLOT DISPLAY
    plt.plot(x,y)
    plt.plot(x,vle)
    plt.plot(xd,xd,'-or')
    plt.plot(xw,xw,'-ob')
    plt.plot(zf,zf,'-ok')
    ## uol plot correction
    uol=[]
    x_uol=np.linspace(xins,xd,nx)
    for i in range(0,len(x_uol)):
        uol.append(R*x_uol[i]/(R+1)+xd/(R+1))
    plt.plot(x_uol,uol)
    plt.plot([xins,xq],[yins,yq])
    plt.plot(xins,yins,'-og')
    plt.plot(xstrip,lol)
    for i in range(1,len(xst)):
        plt.plot([xst[i-1],xst[i]],[yst[i-1],yst[i]],'-k')
    plt.autoscale(enable=True, axis='both', tight=True)
    plt.show()
McCabeThiele(0.42,0.7,0.1,1.5,0.8,2,0.4,20,'benzene')
