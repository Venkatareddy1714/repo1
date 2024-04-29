import random
import math
t_b=input("Enter choice of beam\n   1.cantilever \n  2. Simply Suported \n  3. Continuous \n")
l=int(input("Enter clear span length of beam in (m)\n"))
b=input("enter width value in mm\n")
D=input("enter depth value in mm\n")
if (b.isdigit() and D.isdigit()):
    b=float(b)
    D=float(D)
else:
    if (l<10):
        d={1:7,2:20,3:26}
    else:
        d={1:7,2:(20*10)/l,3:(26*10)/l}
    D=(l/d[int(t_b)])*1000
    D=D+dcov+(dia/2)
    b=round(D/1.5)
    if b<250:
        b=250
dcov=input("Enter effective cover value\n")
if (dcov.isdigit()): 
    dcov=float(dcov)
else:
    dcov=50
deff=D-dcov
b1=l+(deff/1000)
b2=l+(D/1000)+(D/1000)
leff=min(b1,b2)
print("Effective length of beam in mm "+str(leff))
print("Width of beam in mm "+str(b))
print("Effective depth of beam in mm "+str(deff))
fck=int(input("Enter fck value in N/mm^2 "))
fy=int(input("Enter fy value in N/mm^2 "))
dfy={250:0.149,415:0.138,500:0.133}
q=dfy[fy]
mulim=(q*fck*b*deff*deff)/10**6
ch=int(input("Enter choice \n  1.load\n  2.moment\n  3.factored moment \n"))
if(ch==1):
    dl=(b/1000)*(D/1000)*25
    ll=int(input("Enter load value in KNm \n"))
    tl=(dl+ll)*1.5
    print("Total load " +str(tl))
    dicl={1:(tl*(leff)*(leff))/2,2:(tl*(leff)*(leff))/8}
    mu=(dicl[int(t_b)])
elif (ch==2):
    mu=1.5*float(input("Enter moment in KNm "))
elif (ch==3):
    mu=float(input("Enter factored moment in KNm "))
print("limiting momemt of resistance "+str(mulim)+"KNm ")
print("factored moment "+str(mu)+"KNm")
if(mulim>mu):
    print("Under reinforced")
elif(mulim<mu):
    print("Over reinforced")
else:
    print("Balanced Section")
if(mulim>mu):
    print("Singly reinforced beam")
    x=(1-math.sqrt(1-((4.6*mu*10**6)/(fck*b*deff*deff))))
    astreq=(0.5*fck*x*b*deff)/fy
    print("area of reinforcement " +str(astreq))
    dia=int(input("Enter dia of bar in mm "))
    aib=(math.pi*dia*dia)/4
    nob=round((astreq/aib))
    asttpro=math.pi*nob*dia*dia/4
    astmin=(0.85*b*deff)/fy
    print("No.of bars "+str(nob))
    print("Min ast in mm^2: "+str(astmin))
    if(astmin<asttpro):
        print("Min ast pro check: ok ")
    else:
        print("Not ok")
    astmax=0.04*b*deff
    if(asttpro<astmax):
        print("Ok")
    else:
        print("Not Ok")
    print("provide "+str(nob)+" no.of "+str (dia)+" mm dia bar" )
elif(mulim<mu):
    print("Doubly reinforced")
    xu=0.48*deff
    mrem=mu-mulim
    x=dcov/deff
    print("dcov/deff: "+str(x))
    fsc=float(input("From code book clause enter fsc value based of dcov/deff in N/mm^2 "))
    asc=(mrem*10**6)/((fsc)*(deff-dcov))
    asc=round(asc) 
    print("compressive stress in compressive steel is "+str(asc) +" mm^2")
    ast1=round((xu*0.36*fck*b)/(0.87*fy))
    print(ast1)
    ast2=round((fsc*asc)/(0.87*fy))
    print(ast2)
    asta=ast1+ast2
    print("Total area in tension "+str(asta)+" mm^2")
    dia=int(input("Enter dia of bar in tension zone in mm : "))
    nofb=round(asta/((3.14*dia*dia)/4))
    asttprov=(nofb*math.pi*dia*dia)/4
    print("no.of bars: "+str(nofb))
    dia2=int(input("Enter dia of bar in compressive zone in mm: "))
    nof=round(asc/((math.pi*dia2*dia2)/4))
    astcprov=nof*math.pi*dia*dia/4
    print("provide "+str(nofb)+" no.of bar @ "+str(dia) +"mm in tension zone")
    print("Provide "+str(nof)+" no.of bar@ "+str(dia2) +"mm in compression zone")
    #check
    asttmin=0.85*b*deff
    if(asttmin<asttprov):
        print("Ok")
    asttmax=0.04*b*deff
    if(asttmax>=asttprov and asttmax>=astcprov):
        print("Ok")
    #check 
else:
    print("Reinforcement details:")
print("For Shear Reinforcement:")
vu=tl*0.5*(leff/1000)
tv=vu/(b*deff)
pt=(100*asttpro)/(b*deff)
print("pt :"+str(pt))
tc=float(input("From code book clause enter tc value based on pt in N/mm^2:"))
if(tv<tc):
    print("Provide Nominal shear reinforcement with 2-legged stirrup");
    dia3=float(input("Enter dia of stirrup "))
    asv=(4*(math.pi*dia3*dia3))/4
    #sv-spacing between Shear Reinforcement
    sv=(0.87*fy*asv*deff)/(0.4*b)  
else:
    vsc=tc*b*deff
    vus=vu-vsc
    print(vus)
    print("Provide shear reinforcement with 2-legged stirrup");
    dia3=float(input("Enter dia of stirrup "))
    asv=(4*(math.pi*dia3*dia3))/4
    sv=(0.87*fy*asv*deff)/(vus*10**3)
a1=0.75*deff
a2=300
a3=sv
spacing=min(a1,a2,a3)
print("Provide "+str(dia3)+" 2-legged stirrup @ "+str(spacing)+"c/c")
# check for deflection
m=0.58*fy*(astreq/asttpro)
print(m)
k1=float(input("From code book figure 4 enter k1 value based on and fy value: "))
n=pt
print(n)
k2=float(input("From code book figure 5 enter k2 value based on and fy value: "))
basic=(k1*k2*dicl[int(t_b)])
prov=(l/deff)
if (prov<basic):
    print("safe in deflection")
else:
    print("Not safe in deflection")
#flexure check
fb= (0.85 * fck * (b * deff**2 - astreq * (deff - astreq / (2 * astreq)))) # bending stress in the concrete
fs = astreq * fy / (0.9 * deff * b) #bending stress in steel
f=fb+fs
if(mu>f):
    print("safe in flexure")
else:
    print("Not safe in flexure")
print("area of reinforcement " +str(astreq))


     

        
