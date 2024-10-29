import numpy as np
import re
import os
import math
import random
import sys
import matplotlib.pyplot as plt
class ParameterLoader:
    def __init__(self):
        self.localdir = 'E:/'
        try:
            a=open(os.path.join(self.localdir, 'parameterA.txt'), 'r')
            b=open(os.path.join(self.localdir, 'parameterB.txt'), 'r')
            c=open(os.path.join(self.localdir, 'parameterC.txt'), 'r')
            d=open(os.path.join(self.localdir, 'parameterD.txt'), 'r')
            self.a = a.read()
            self.b = b.read()
            self.c = c.read()
            self.d = d.read()
            a.close()
            b.close()
            c.close()
            d.close()
            
        except IOError:
            print('null')          
            sys.exit(1)
        except:
            print('Please check the directory of Parameter files')
            sys.exit(1)        
    def get_A_Parameter(self , n , m ):
        x=(re.findall(r'<%d,%d>=\[\s(.+)\]' % (n,m) , self.a))[0].replace(')' ,'').replace('(' ,'').replace(' ','').split(',')
        for i in range(len(x)):
            x[i]=float(x[i])
        return x
    def get_B_Parameter(self): 
        x=(re.findall(r'\[(.+)\]' , self.b))[0].replace(')' ,'').replace('(' ,'').replace(' ','').split(',')
        for i in range(len(x)):
            x[i]=float(x[i])
        return x
    def get_C_Parameter(self):
        x=(re.findall(r'\((.+)\)' , self.c))[0].replace(' ','').split(',')
        for i in range(len(x)):
            x[i]=float(x[i])
        return x
    def get_D_Parameter(self):
        x=(re.findall(r'\((.+)\)' , self.d))[0].replace(' ','').split(',')
        for i in range(len(x)):
            x[i]=float(x[i])
        return x
    def find_the_number_of_tellers_and_jobs(self):  
        y=(re.findall(r'<(\d),(\d)>=' , self.a))
        x=[[] for i in range(len(y))]
        for i in range(len(y)):
            x[i].append(int(y[i][0]))
            x[i].append(int(y[i][1]))
        return ( (max(x , key=lambda x: x[0]))[0] , (max(x , key=lambda x: x[1]))[1]+1 )
x=ParameterLoader().find_the_number_of_tellers_and_jobs()
tellers_no = x[0]
jobs = x[1]
class RandomGenerator:
    def A(self , n , m): 
        x=ParameterLoader().get_A_Parameter(n , m)
        probabilities=[]
        elements=[]
        for i in range(len(x)):
            if i%2!=0:
                probabilities.append(x[i])
            else:
                elements.append(x[i])
        return np.random.choice(elements, p=probabilities)
    def B(self): 
        x=ParameterLoader().get_B_Parameter()
        probabilities=[]
        elements=[]
        for i in range(len(x)):
            if i%2!=0:
                probabilities.append(x[i])
            else:
                elements.append(x[i])
        return int(np.random.choice(elements, p=probabilities))
    def C(self): 
        probabilities=ParameterLoader().get_C_Parameter()
        elements=[i for i in range(len(probabilities))]
        return np.random.choice(elements, p=probabilities)
                
    def D(self , M=ParameterLoader().get_D_Parameter()[0] , D=ParameterLoader().get_D_Parameter()[1] ) : 
        f=lambda x , M , D : (math.exp(-((x-M)**2)/(2*D**2)))/((math.sqrt(2*math.pi))*D)
        i=M                
        while True:
            if f(i,M , D)<0.00000000001:
                min_x=i
                break
            else:
                i-=1
        i=M
        while True:
            if f(i , M , D)<0.0000000001:
                max_x=i
                break
            else:
                i+=1                
        while True:    
            rand_x = (max_x - min_x) * random.random() + min_x
            rand_y = f(M,M,D) * random.random()     
            f_y = f(rand_x , M , D)
            if(rand_y <= f_y ):
                return(rand_x)
                break
            else:
                continue
class teller:                              
    def __init__(self , number ):
        self.MeanJobTimes=[]               
        self.MinJobTimes=[]         
        self.no_work = 0              
        self.free_time=0           
        self.number=number                    
        for j in range(jobs):              
            x=0
            l=[]
            a=ParameterLoader().get_A_Parameter(number , j)
            for i in range(0,len(a),2):
                x+= (a[i] * a[i+1])
                l.append(a[i])  
            self.MeanJobTimes.append(x)
            self.MinJobTimes.append(min(l))
    def availability(self , time):        
        if time>=self.free_time:          
            return True
        else:
            return False
class client:                                    
    def __init__(self , in_time):  
        self.job=RandomGenerator().C()                            
        self.money = RandomGenerator().D()
        self.in_queue = in_time
        client.out_queue = in_time
        self.wait=0                               
    def __str__(self):                             
        return 'job=%d money=%d , wait=%d' % ( self.job, self.money,self.wait)
class queue:                             
    def __init__(self ):
        self.q=[]
    def Enqueue(self ,client , time):
        self.q.append(client) 
    def Dequeue(self , time ):
        self.q.pop(0)
class decide:                                                
    def __init__(self  , client , possible_tellers):        
        self.client=client
        self.job=client.job                               
        self.possible_tellers=possible_tellers 
    def strategy1(self):                                                   
        p=[]                                                               
        a=min(self.possible_tellers , key=lambda x: x.free_time)           
        for i in range(len(self.possible_tellers)):
            if a.free_time==self.possible_tellers[i].free_time:
                p.append(self.possible_tellers[i])       
        return random.choice(p)           
    def strategy2(self):
        p=[]
        a=min(self.possible_tellers , key=lambda x: x.MeanJobTimes)    
        for i in range(len(self.possible_tellers)):
            if a.MeanJobTimes==self.possible_tellers[i].MeanJobTimes:
                p.append(self.possible_tellers[i])
        return random.choice(p)    
    def strategy3(self):
        p=[]
        a=min(self.possible_tellers , key=lambda x: x.MinJobTimes)
        for i in range(len(self.possible_tellers)):
            if a.MinJobTimes==self.possible_tellers[i].MinJobTimes:
                p.append(self.possible_tellers[i])
        return random.choice(p)
data=[ [ [] for i in  range(3) ] for j in range(4)] 
def do(endtime):
    tellers=[]
    for i in range(tellers_no):
        tellers.append(teller(i+1))
    wait=0           
    no_work=0        
    time=0
    clients=[]       
    c=0             
    d=0              
    m=0              
    times=[]        
    q=queue()
    while time<endtime:
        c+=1
        times.append(time)
        new_client=client(time)
        clients.append(new_client)                                        
        if new_client.money>0:
            m+=1
        x=[]         
        for i in range(tellers_no):
            if tellers[i].availability(time)==True:
                x.append(tellers[i])
        if len(x)==0:          
            d+=1               
            q.Enqueue(new_client , time)
            nearest_free_time=(min(tellers , key=lambda x : x.free_time)).free_time
            for i in range(tellers_no):
                if nearest_free_time==tellers[i].free_time:
                    x.append(tellers[i])
            chosen_teller=decide(new_client,x).strategy1()
            new_client.out_queue  =  chosen_teller.free_time  
            new_client.wait       =  new_client.out_queue - new_client.in_queue  
            wait += new_client.wait          
            q.Dequeue(new_client.out_queue)    
        else:          
            chosen_teller=decide(new_client,x).strategy1()
            new_client.out_queue = new_client.in_queue   
        chosen_teller.no_work   +=    new_client.out_queue  -   chosen_teller.free_time 
        no_work += new_client.out_queue  -   chosen_teller.free_time  
        chosen_teller.free_time  =   RandomGenerator().A( chosen_teller.number , new_client.job) + new_client.out_queue 
        time+=RandomGenerator().B()  
    data[0][0].append(wait/len(clients))
    data[1][0].append(no_work/len(tellers))
    data[2][0].append(d/c)
    data[3][0].append(m/c)
    tellers=[]
    for i in range(tellers_no):
        tellers.append(teller(i+1))
    for i in range(len(clients)):
        clients[i].out_queue = 0
        clients[i].wait=0
    wait=0 
    no_work=0    
    time=0
    d=0
    q=queue()
    for j in range(len(times)): 
        new_client=clients[j]  
        x=[]
        for i in range(tellers_no):
            if tellers[i].availability(times[j])==True:
                x.append(tellers[i])
        if len(x)==0:
            d+=1
            q.Enqueue(new_client , time)
            nearest_free_time=(min(tellers , key=lambda x : x.free_time)).free_time
            for i in range(tellers_no):
                if nearest_free_time==tellers[i].free_time:
                    x.append(tellers[i])
            chosen_teller=decide(new_client,x).strategy1()
            new_client.out_queue=chosen_teller.free_time
            q.Dequeue(new_client.out_queue)
            new_client.wait = new_client.out_queue-new_client.in_queue    
        else:
            chosen_teller=decide(new_client,x).strategy1()
            new_client.out_queue=new_client.in_queue
        chosen_teller.no_work+=new_client.out_queue-chosen_teller.free_time
        no_work+=new_client.out_queue  -   chosen_teller.free_time 
        wait+=new_client.wait
        chosen_teller.free_time=RandomGenerator().A( chosen_teller.number , new_client.job) + new_client.out_queue  
    data[0][1].append(wait/len(clients))
    data[1][1].append(no_work/len(tellers))
    data[2][1].append(d/c)
    data[3][1].append(m/c)
    for i in range(len(tellers)):
        tellers[i].no_work = 0
        tellers[i].free_time=0
    for i in range(len(clients)):
        clients[i].out_queue = 0
        clients[i].wait=0
    wait=0 
    no_work=0    
    time=0
    d=0
    q=queue()
    for j in range(len(times)):   
        new_client=clients[j]
        x=[]
        for i in range(tellers_no):
            if tellers[i].availability(times[j])==True:
                x.append(tellers[i])       
        if len(x)==0:
            d+=1
            q.Enqueue(new_client,time)
            nearest_free_time=(min(tellers , key=lambda x : x.free_time)).free_time
            for i in range(tellers_no):
                if nearest_free_time==tellers[i].free_time:
                    x.append(tellers[i])
            chosen_teller=decide(new_client,x).strategy1()
            new_client.out_queue=chosen_teller.free_time
            q.Dequeue(new_client.out_queue)
            new_client.wait = new_client.out_queue-new_client.in_queue   
        else:
            chosen_teller=decide(new_client,x).strategy1()
            new_client.out_queue=new_client.in_queue
        chosen_teller.no_work+=new_client.out_queue-chosen_teller.free_time
        no_work+=new_client.out_queue  -   chosen_teller.free_time 
        wait+=new_client.wait
        chosen_teller.free_time=RandomGenerator().A( chosen_teller.number , new_client.job) + new_client.out_queue   
    data[0][2].append(wait/len(clients))
    data[1][2].append(no_work/len(tellers))
    data[2][2].append(d/c)
    data[3][2].append(m/c)
    

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

t=[10,100,1000,10000,100000]
for i in range(len(t)):
    do(t[i])
X = np.arange(len(t))
def wait():    
    plt.bar(X + 0.85, data[0][0], color = 'b', width = 0.15)
    plt.bar(X + 1.00, data[0][1], color = 'g', width = 0.15)
    plt.bar(X + 1.15, data[0][2], color = 'r', width = 0.15)
    plt.title(' mean clients\' wait time ')
    plt.show()
def free(): 
    plt.bar(X + 0.85, data[1][0], color = 'b', width = 0.15)
    plt.bar(X + 1.00, data[1][1], color = 'g', width = 0.15)
    plt.bar(X + 1.15, data[1][2], color = 'r', width = 0.15)
    plt.title('mean free tellers\' time ')
    plt.show()
def queue():
    plt.bar(X + 0.85, data[2][0], color = 'b', width = 0.15)
    plt.bar(X + 1.00, data[2][1], color = 'g', width = 0.15)
    plt.bar(X + 1.15, data[2][2], color = 'r', width = 0.15)
    plt.title('posibility of getting into queue')
    plt.show()
def money():
    plt.bar(X + 0.85, data[3][0], color = 'b', width = 0.15)
    plt.bar(X + 1.00, data[3][1], color = 'g', width = 0.15)
    plt.bar(X + 1.15, data[3][2], color = 'r', width = 0.15)
    plt.title('posibility of getting money')
    plt.show()
