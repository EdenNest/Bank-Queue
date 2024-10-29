import numpy as np
import re
import os
import math
import random
import sys

class ParameterLoader:
    def __init__(self):
        self.localdir ='E:/'
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
        #baraye karmande n om va farayande k om , tozie ehtemal ra mikhanad
        x=(re.findall(r'<%d,%d>=\[\s(.+)\]' % (n,m) , self.a))[0].replace(')' ,'').replace('(' ,'').replace(' ','').split(',')
        
        for i in range(len(x)):
            x[i]=float(x[i])
        return x
       #khoroji :[5.0, 0.4, 7.0, 0.6]
    
    def get_B_Parameter(self): 
        x=(re.findall(r'\[(.+)\]' , self.b))[0].replace(')' ,'').replace('(' ,'').replace(' ','').split(',')
        for i in range(len(x)):
            x[i]=float(x[i])
        return x
        #khoroji :[1.0, 0.02, 2.0, 0.02, 3.0, 0.03, 4.0, 0.04, 5.0, 0.05 , ...] 

    def get_C_Parameter(self):
        #liste ehtemalat farayand ha ra mikhanad va be sorat list ba ozv haye float khoroji mide ,  # c = ج
        x=(re.findall(r'\((.+)\)' , self.c))[0].replace(' ','').split(',')
        for i in range(len(x)):
            x[i]=float(x[i])
        return x
        #khoroji :[0.15, 0.3, 0.3, 0.25]

    def get_D_Parameter(self):
        x=(re.findall(r'\((.+)\)' , self.d))[0].replace(' ','').split(',')
        for i in range(len(x)):
            x[i]=float(x[i])
        return x
        #khoroji :[10000.0, 1.0]


    def find_the_number_of_tellers_and_jobs(self):  #in tabe az roye file txt , teddad faryand ha va karmandan ra tashkhis midahad.
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
    def A(self , n , m): #baraye karmande 'n'  va farayande 'm' : yek zamane random peida mikonad
        x=ParameterLoader().get_A_Parameter(n , m)
        probabilities=[]
        elements=[]
        for i in range(len(x)):
            if i%2!=0:
                probabilities.append(x[i])
            else:
                elements.append(x[i])
        return np.random.choice(elements, p=probabilities)

    def B(self): #yek faseleye zamani vorood entekhab mikonad
        x=ParameterLoader().get_B_Parameter()
        probabilities=[]
        elements=[]
        for i in range(len(x)):
            if i%2!=0:
                probabilities.append(x[i])
            else:
                elements.append(x[i])
        return int(np.random.choice(elements, p=probabilities))

    def C(self): #yek farayand entekhab mikonad
        probabilities=ParameterLoader().get_C_Parameter()
        elements=[i for i in range(len(probabilities))]
        return np.random.choice(elements, p=probabilities)
                
    def D(self , M=ParameterLoader().get_D_Parameter()[0] , D=ParameterLoader().get_D_Parameter()[1] ) : 
        f=lambda x , M , D : (math.exp(-((x-M)**2)/(2*D**2)))/((math.sqrt(2*math.pi))*D)
        i=M           #taghrib khobi baraye karane -infinite      
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
            rand_y = f(M,M,D) * random.random()     #max_y vaghti ast ke x roye miangin bashad
            f_y = f(rand_x , M , D)
            if(rand_y <= f_y ):
                return(rand_x)
                break
            else:
                continue

                
    
class teller:                               #teller=karmand
    def __init__(self , number ):
        self.MeanJobTimes=[]                #listi ke ozve i an , miangin zaman in karmand  baraye farayand i midahad
        self.MinJobTimes=[]                 #listi ke ozve i an , min      zaman in karmand  baraye farayand i midahad
        self.no_work = 0                    #zaman bikari har karmand dar ebteda 0 ast va mitavanad update shavad
        self.free_time=0           #free time : zaman tamam shodan  moshtari ghabli >>> Amadeye paziresh baadi
        self.number=number                  # shomare ye baje

       
        for j in range(jobs):               #ba estefade az class ParameterLoader , "MeanJobTimes" va "MinJobTimes" dorost mishavd.
            x=0
            l=[]
            a=ParameterLoader().get_A_Parameter(number , j)
            for i in range(0,len(a),2):
                x+= (a[i] * a[i+1])
                l.append(a[i])  
            self.MeanJobTimes.append(x)
            self.MinJobTimes.append(min(l))


    def availability(self , time):         #in tebbe yek zaman migirad va ba "free time" moghayese mikonad va check mikond ke...
        if time>=self.free_time:           #                          ... amadeye paziresh hast ya na.
            return True
        else:
            return False
        




class client:                                        #client = moshtari
    def __init__(self , in_time):      #job = Farayand   ,  money : pooli ke midahad (ya barmidarad)
        self.job=RandomGenerator().C()                                 #in_time = time vorood be bank (ya saf) 
        self.money = RandomGenerator().D()
        self.in_queue = in_time
        client.out_queue = in_time
        self.wait=0                                  # zaman entezar = wait
    def __str__(self):                               # baraye rahati dar test sakhte shode
        return 'job=%d money=%d , wait=%d' % ( self.job, self.money,self.wait)
        



class queue:                                #class saf yek list ast.
    def __init__(self ):
        self.q=[]
    def Enqueue(self ,client , time):
        self.q.append(client) 
    def Dequeue(self , time ):
        self.q.pop(0)




class decide:                                                  #decide = takhsis moshtari be karmand
    def __init__(self  , client , possible_tellers):          #in class yek obj client va yek list az chand obj teller migirad.
        self.client=client
        self.job=client.job                                    #faraynad darkhasti obj client ra zakhire mikonad
        self.possible_tellers=possible_tellers

        
    def strategy1(self):                                                   #har strategy ebteda min ra bar asas parameter...
        p=[]                                                               #... mored nazar entekhab mikonad va agar chand ta ...
        a=min(self.possible_tellers , key=lambda x: x.free_time)           #... min dasht , random yeki ra midahad
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




#tabee zir ghesmat asli ast. yek zaman migirad va baraye strategy aval ta vaghti zaman tamam nashode moshtari vared mikonad.
#dar ebteda yek list karmand ham ba random toolid mishavd.
#in do list dar strategy 2 va 3 ham estefade mishavand ke natayej ghabel moghayese bashad.
#yaani dar har 3 strategy , moshakhasate karmand ha va moshtari ha sabet ast.
#be hamin dadil vazeh ast ke miangin pool dade shode dar har se halat yeksan ast

def do(endtime):
    print( '\n' , '     strategy 1..... '  )

    tellers=[]
    for i in range(tellers_no):
        tellers.append(teller(i+1))

    wait=0           #dar har loop in parameter update mishavad va zaman entezare har moshtari be An ezafe mishavad 
    no_work=0        #dar har loop in parameter update mishavad va zaman bikari   har karmand  be An ezafe mishavad  
    time=0
    clients=[]       #client haye vared shode ra negah midarad ta dar strategy 2 , 3 estefade shavad.
    c=0              #tedad loop mishemarad ( teddad moshtari ke vared mishavad)
    d=0              #har daffe moshtari be saf vared mishavad ra mishermarad
    m=0              #har daffe ke yek moshtari pool + midahad ra mishemarad
    times=[]         #zaman haye voorod moshtari ha ra negah midarad ta dar strategy 2 , 3 estefade shavad
    q=queue()

    while time<endtime:
        c+=1
        times.append(time)
        new_client=client(time) #client jadid vared mishavad
        clients.append(new_client)                                              #etelaate client jadid save mishavad
        
        if new_client.money>0:
            m+=1
            

        x=[]           #x=listi az karmandane azad dar in time
        for i in range(tellers_no):
            if tellers[i].availability(time)==True:
                x.append(tellers[i])

           
        if len(x)==0:          #agar hich kodam azad nabodan : be saf miravad >> nazdik tarin karmandi ke azad shod entekhab mishavad
            d+=1               #...>> agar chand karmand ba ham (dar ayande) azad shavand >> strategy stefade mishavad
            q.Enqueue(new_client , time)
            
            nearest_free_time=(min(tellers , key=lambda x : x.free_time)).free_time
            for i in range(tellers_no):
                if nearest_free_time==tellers[i].free_time:
                    x.append(tellers[i])
                    
            chosen_teller=decide(new_client,x).strategy1()
            new_client.out_queue  =  chosen_teller.free_time  #zamane khoroj az saf = zaman azad shodane karmande entekhab shode
            new_client.wait       =  new_client.out_queue - new_client.in_queue  #entezar = khoroj - vorood
            wait += new_client.wait          #meghdare entezare moshtari ezafe mishavad
            q.Dequeue(new_client.out_queue)


      
            
        else:           #chand karmand azad hastan >> strategy ya yek karmand azad ast
            chosen_teller=decide(new_client,x).strategy1()
            new_client.out_queue = new_client.in_queue   #zamane khorroj az saf = zaman voorod (aslan vared nashode!)
        

        chosen_teller.no_work   +=    new_client.out_queue  -   chosen_teller.free_time 
        no_work += new_client.out_queue  -   chosen_teller.free_time  
       
        
        chosen_teller.free_time  =   RandomGenerator().A( chosen_teller.number , new_client.job) + new_client.out_queue 
           #baraye karmand entekhab shode va farayand morede nazar , yek time (randomgenerator) toolid mikonad

        time+=RandomGenerator().B()  #fasele zamani baadi ra toolid mikonad va zaman ra jeloo mibarad
        
    print('مشتريها انتظار زمان ميانگين =' , wait/c) 
    print('کارمندها بيکاري زمان ميانگين =' , no_work/tellers_no)
    print('صف به مشتري شدن وارد احتمال =' , d/c)
    print('بانک به دادن پول احتمال =' , m/c)


 
    print('\n'*2 , '     strategy 2..... ' )  

    tellers=[]
    for i in range(tellers_no):
        tellers.append(teller(i+1))
    for i in range(len(clients)):
        clients[i].out_queue = 0
        clients[i].wait=0

    wait=0 
    no_work=0    #'entezar' va 'bikari'  va 'vared shodan be saf' ra sefr mikonim
    time=0
    d=0
    q=queue()
    for j in range(len(times)): 
        new_client=clients[j]  #client jadid ra az listi ke az ghabl dashtim mikhanim
        


        
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
    print('مشتريها انتظار زمان ميانگين =' , wait/len(clients))    
    print('کارمندها بيکاري زمان ميانگين =' , no_work/len(tellers))
    print('صف به مشتري شدن وارد احتمال =' , d/c)
    print('بانک به دادن پول احتمال =' , m/c)
    print('\n'*2 , '     strategy 3..... ' )
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
    print('مشتريها انتظار زمان ميانگين =' , wait/len(clients))    
    print('کارمندها بيکاري زمان ميانگين =' , no_work/len(tellers))
    print('صف به مشتري شدن وارد احتمال =' , d/c)
    print('بانک به دادن پول احتمال =' , m/c)
    
try:    
    do(int(input()))
except:
    print('somthing went wrong in main process')
    sys.exit(1)
