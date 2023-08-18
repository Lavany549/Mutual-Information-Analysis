import csv
import matplotlib.pyplot as plt
import math
import matplotlib.ticker as ticker
import random
import numpy as np
def sbox_simple_op(x,k):
    sbox=[7,6,5,4,3,2,1,0];
    out=sbox[x^k];
    hw_table=[0,1,1,2,1,2,2,3]
    return out

def power_trace_gen():
    key=0;
    power_trace=[0]*1000;
    noise=np.random.normal(0, 0.001, 1000);
    #noise=[0]*1000
    x=[0]*1000
    print len(noise)
    print len(power_trace)
    for i in range(1000):
        x[i]=random.randint(0,7)
        power_trace[i]=sbox_simple_op(x[i],key)+noise[i];

    return x,power_trace


x,O=power_trace_gen();
ntrace=1000
L = []

for i in range(ntrace):
        pt = x[i]        
        lt = [0]*8
        #print "Processing Trace: "+str(i)
        
        for j in range(8):
            b=sbox_simple_op(pt,j)
            lt[j] = b
        
        lt_temp = [O[i], lt]
        L.append(lt_temp)

O_dist = [0]*ntrace

ocount = 0;

for o in O:
    t_o_count = 0;
    for i in range(ntrace):
        temp_o_val = L[i][0]
        if temp_o_val == o:
            t_o_count=t_o_count+1

    O_dist[ocount] = t_o_count/float(ntrace) 
    ocount = ocount+1

Ent_O = 0.0


for p in O_dist:
    Ent_O = Ent_O - (p*math.log(p))

print Ent_O
    




Ent_Kb = [0.0]*8
o_num_val=ntrace
for kb in range(8):
    Prob_HOL = 0.0
    Li_dist = [0.0]*8

    for i in range(ntrace):
        lval = L[i][1][kb]
        Li_dist[lval] = Li_dist[lval]+1
    
    
    for i in range(len(Li_dist)):
        Li_dist[i] = float(Li_dist[i])/float(ntrace)

    print "Processing Key Byte: "+str(kb)
    for ival in range(8):
        temp_L_i_Oxj = [0.0]*o_num_val
        temp_L_i = [0.0]*o_num_val
        temp_P_l = [0.0]*o_num_val
            
        ocount = 0
        for o in O:
            for ni in range(ntrace):
                lval = L[ni][1][kb]
                oval = L[ni][0]
                if(ival == lval):
                    temp_L_i[ocount] = temp_L_i[ocount]+1
                    if(oval == o):
                        temp_L_i_Oxj[ocount] = temp_L_i_Oxj[ocount]+1
            ocount = ocount+1
                
        for i in range(o_num_val):
            if(temp_L_i[i]!=0):
                temp_P_l[i] = float(temp_L_i_Oxj[i])/temp_L_i[i]
            
            
        Sum_P_Oxj = 0.0
            
        for p in temp_P_l:
            if(p!=0):
                Sum_P_Oxj = Sum_P_Oxj - p*math.log(p)
                
        Prob_HOL = Prob_HOL + (Li_dist[ival]*Sum_P_Oxj)
            
    Ent_Kb[kb] = Ent_O - Prob_HOL
    
print max(Ent_Kb)
print Ent_Kb.index(max(Ent_Kb))
print hex(Ent_Kb.index(max(Ent_Kb)))
    
xval = range(8)
fig, ax1 = plt.subplots()
axes = plt.gca()
plt.plot(xval, Ent_Kb, 'k', linewidth=0.2)
plt.locator_params(axis='x', nbins=10)
axes.get_xaxis().set_major_formatter(ticker.FormatStrFormatter("0x%x"))
ax1.set_ylabel('MIA Value')
ax1.set_xlabel('First Key Byte')
plt.title('Mutual Information Analysis')
plt.savefig("MIA_FirstKeyByte.png",dpi=1200,bbox_inches='tight')
plt.show()

#print Li_dist
