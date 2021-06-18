# -*- coding: utf-8 -*-


import random
import math
import sys
from sheets import GetData


class OptimalPath:

  def __init__(self):
    self.N_V = 2
    self.V_C = 8
    self.Cost=0
    self.setValues()
    self.setNode()
    self.setVehical()

  def setValues(self):
    obj = GetData()
    data = obj.dist
    self.N_C = len(data[0])
    self.Node = []*(self.N_C+1)
    self.V = []*(self.N_V+1)
    self.VR = [[] for k in range(self.N_C+1)]
    self.VR1 = [[] for k in range(self.N_C+1)]
    self.dist = [[0 for x in range(self.N_C+1)] for y in range(self.N_C+1)]
    for i in range(0,self.N_C):
      for j in range(0,self.N_C):
        D = int(data[i][j])
        self.dist[i][j] = D
        self.dist[j][i] =D


  def setNode(self):
    D = {
      "id": 0,
      "x": 0,
      "y": 0,
      "ID": True,
      "IR": False,
      "demand": 0
    }
    dcopy = D.copy()
    self.Node.append(dcopy)
    for i in range(1,self.N_C):
      x = int(random.random()*100)
      y = int(random.random()*100)
      demand = i
      D = {
        "id": i,
        "x": x,
        "y": y,
        "ID": False,
        "IR": False,
        "demand": demand
      }
      dcopy = D.copy()
      self.Node.append(dcopy)

  def setVehical(self):
    for i in range(self.N_V):
      D = {
      "vid":i,
      "cap":self.V_C,
      "load":0,
      "curloc":0,
      "closed":0,
    }
    dcopy = D.copy()
    self.V.append(dcopy)


  def check_if_fits(self, Vid,val):
    if self.V[Vid]["load"]+val<=self.V_C:
      return True
    else:
      return False

  def UCE(self):
    for i in range(1,self.N_C):
      if self.Node[i]["IR"]==False:
        return True
    return False

  def greedy_sol(self):
    global MinCost
    global Candcost
    Vid = 0  #vehical index
    Candidate = -1
    Cost = 0
    EndCost = 0
    CustIndex = 0
    while(self.UCE()):
      F = 0
      CI = 0      # current index
      Candidate = -1
      MinCost = 100000000000
      if(len(self.VR[Vid]) == 0):   #if length of any route is 0, vehicle will start from depot
        self.V[Vid]["load"] += self.Node[0]["demand"]
        self.V[Vid]["curloc"] = self.Node[0]["id"]
        self.VR[Vid].append(self.Node[0]["id"])
        self.VR1[Vid].append(self.Node[0]["id"])
      for i in range(1,self.N_C):
        if(self.Node[i]["IR"] == False):
          if(self.check_if_fits(Vid,self.Node[i]["demand"])):
            CandCost = self.dist[self.V[Vid]["curloc"]][i]
            if(MinCost  > CandCost):
              MinCost = CandCost
              CustIndex = i
              Candidate = i

      if Candidate == -1:  #not able to satisfy any vehicle
        if Vid+1<self.N_V:   #not the last vehicle
          if self.V[Vid]["curloc"] != 0:       #if wherever it is present, bring it back to depo, as it won't satisfy any more customers
            EndCost = self.dist[self.V[Vid]["curloc"]][0]
            self.VR[Vid].append(self.Node[0]["id"])
            self.VR1[Vid].append(self.Node[0]["id"])
            self.V[Vid]["load"] += self.Node[0]["demand"]
            self.V[Vid]["curloc"] = self.Node[0]["id"]
            Cost+=EndCost
          Vid=Vid+1
        else:           #all vehicles exhausted
          #print("vechile id is : ", Vid)
          #print("Something strange happend")
          sys.exit()

      else:       #wherever it went, update the location, and load of the vehicle and update the router-path of the vehicle
        self.VR[Vid].append(Candidate)
        self.VR1[Vid].append(Candidate)
        self.V[Vid]["load"] += self.Node[Candidate]["demand"]
        self.V[Vid]["curloc"] = self.Node[Candidate]["id"]
        self.Node[Candidate]["IR"] = True
        #Cost = Cost+MinCost

    EndCost = self.dist[self.V[Vid]["curloc"]][0]  #finally all vehicles go back to depo
    self.VR[Vid].append(0)
    self.VR1[Vid].append(0)
    self.Cost = self.Cost+EndCost

    return self.Printans(" Greedy ", self.Calculate())




  def IntraLocalSearch(self):
    global rt
    global MovingNodeDemand
    global VehIndexFrom
    global VehIndexTo
    global BestNCost
    global NeightboorCost
    global Ans
    rt = []
    Ans=self.Cost
    swapIndexA=-1
    swapIndexB=-1
    swapRoute=-1

    MaxIteration=50
    iteration_number=0
    Termination=False
    while(Termination == False):
      iteration_number+=1
      BestNCost=10000
      for VehIndex in range(0,self.N_V):
        RouteLength = len(self.VR1[VehIndex])
        for i in range(1,RouteLength-1):
          for j in range(0,RouteLength-1):
            if((j!=i) and (j!=i-1)):
              a=VehIndex
              MCst1 = self.dist[self.VR1[a][i-1]][self.VR1[a][i]]
              MCst2 = self.dist[self.VR1[a][i]][self.VR1[a][i+1]]
              MCst3 = self.dist[self.VR1[a][j]][self.VR1[a][j+1]]
              ACst1 = self.dist[self.VR1[a][i-1]][self.VR1[a][i+1]]
              ACst2 = self.dist[self.VR1[a][j]][self.VR1[a][i]]
              ACst3 = self.dist[self.VR1[a][i]][self.VR1[a][j+1]]

              M = (MCst1+MCst2+MCst3)
              S = (ACst1+ACst2+ACst3)

              NeightboorCost=S-M
              if(NeightboorCost<BestNCost):
                BestNCost=NeightboorCost
                swapIndexA=i
                swapIndexB=j
                swapRoute=VehIndex
      #print("in intra ",swapIndexA,' ',swapIndexB, swapRoute)
      if(BestNCost<0):
        rt.clear()
        rt=self.VR1[swapRoute].copy()
        #print(rt)
        swapNode = rt[swapIndexA]
        del rt[swapIndexA]
        if(swapIndexA<swapIndexB):
          rt.insert(swapIndexB,swapNode)
        else:
          rt.insert(swapIndexB+1,swapNode)
        Ans +=BestNCost
        self.VR1[swapRoute] = rt.copy()
      else:
        Termination=True
      if(iteration_number == MaxIteration):
        Termination = True

    return self.Printans1("IntraLocal",self.Calculate1())


  def InterLocalSearch(self):
    global ans
    global RouteFrom
    global RouteTo
    global MovingNodeDemand
    global VehIndexFrom
    global VehIndexTo
    global BestNCost
    global NeightboorCost
    global Cost
    ans = 0
    RouteFrom = []
    RouteTo = []
    swapIndexA=-1
    swapIndexB=-1
    swapRouteFrom=-1
    swapRouteTo=-1

    MaxIteration = 50
    iteration_number = 0
    #for i in range(N_V+1):
      #print(i,' ',len(VR[i]))
    Termination =False
    while(Termination==False):
      iteration_number+=1
      BestNCost = 100000
      for VehIndexFrom in range(0,self.N_V):
        #RouteFrom = VR[VehIndexFrom][:]
        RouteFromLength = len(self.VR[VehIndexFrom])
        for i in range(1,RouteFromLength-1):
          for VehIndexTo in range(0,self.N_V):
            #RouteTo = VR[VehIndexTo][:]
            RouteToLength = len(self.VR[VehIndexTo])
            for j in range(0,RouteToLength-1):
              a=VehIndexFrom
              b=VehIndexTo
              Node_idx = self.VR[a][i]
              MovingNodeDemand=self.Node[Node_idx]["demand"]
              if((VehIndexFrom==VehIndexTo) or self.check_if_fits(VehIndexTo,MovingNodeDemand)):
                if(( (VehIndexFrom == VehIndexTo) and ((j==i)or(j==i-1))) == False):
                  MinusCst1 = self.dist[self.VR[a][i-1]][self.VR[a][i]]
                  MinusCst2 = self.dist[self.VR[a][i]][self.VR[a][i+1]]
                  MinusCst3 = self.dist[self.VR[b][j]][self.VR[b][j+1]]
                  AddCst1 = self.dist[self.VR[a][i-1]][self.VR[a][i+1]]
                  AddCst2 = self.dist[self.VR[b][j]][self.VR[a][i]]
                  AddCst3 = self.dist[self.VR[a][i]][self.VR[b][j+1]]
                  S = AddCst1+AddCst2+AddCst3
                  M = MinusCst1+MinusCst2+MinusCst3
                  #print(S,' ',M)
                  NeightboorCost = (S)-(M)

                  if(NeightboorCost<BestNCost):
                    #print(swapIndexA,' inf cond ',swapIndexB)
                    BestNCost = NeightboorCost
                    swapIndexA = i
                    swapIndexB = j
                    swapRouteFrom = VehIndexFrom
                    swapRouteTo = VehIndexTo

      #print("out of loop ", swapIndexA,' ',swapIndexB,' ', swapRouteFrom,' ',swapRouteTo)

      if(BestNCost<0):
        #print("in bestncost")
        RouteFrom.clear()
        RouteFrom = self.VR[swapRouteFrom].copy()
        #print(swapRouteFrom,' printing swap idx ',swapRouteTo)
        #print(swapIndexA,'print idx ',swapIndexB)
        RouteTo.clear()
        RouteTo = self.VR[swapRouteTo].copy()
        #print(VR[swapRouteFrom],' printing VR ',VR[swapRouteTo])
        self.VR[swapRouteFrom].clear()
        self.VR[swapRouteTo].clear()
        #print("in index ", swapIndexA,' ',RouteFrom)
        swapNode = RouteFrom[swapIndexA]
        #print(RouteFrom)
        del RouteFrom[swapIndexA]
        #print(RouteFrom)
        if(swapRouteFrom == swapRouteTo):
          del RouteTo[swapIndexA]
          #print("in equal")
          if(swapIndexA<swapIndexB):
            RouteTo.insert(swapIndexB,swapNode)
            #print(RouteTo)
          else:
            RouteTo.insert(swapIndexB+1,swapNode)
        else:
          RouteTo.insert(swapIndexB+1,swapNode)
        self.VR[swapRouteFrom] = RouteFrom.copy()
        self.V[swapRouteFrom]["load"] -= MovingNodeDemand
        self.VR[swapRouteTo] = RouteTo.copy()
        self.V[swapRouteTo]["load"] += MovingNodeDemand
        #ans=Cost+BestNCost
        RouteFrom.clear()
        RouteTo.clear()
      else:
        #print(iteration_number,' ',"end")
        Termination = True
      if iteration_number == MaxIteration:
        Termination = True
    #print("INTER",' ',ans)

    return self.Printans("InterLocal Search ",self.Calculate())

  def Calculate(self):
    Res = 0
    for i in range(self.N_V+1):
      if(len(self.VR[i])):
        for j in range(1,len(self.VR[i])):
          Res += self.dist[self.VR[i][j-1]][self.VR[i][j]]
    return Res

  def Calculate1(self):
    Res = 0
    for i in range(self.N_V+1):
      if(len(self.VR1[i])):
        for j in range(1,len(self.VR1[i])):
          Res += self.dist[self.VR1[i][j-1]][self.VR1[i][j]]
    return Res


  def Printans(self, s, x):
    path = []
    for i in range(0,self.N_V):
      if(len(self.VR[i]) != 0):
        path = self.VR[i]
    ans = {
            "name": s,
            "cost": x,
            "path": path
        }
    return ans

  def Printans1(self, s, x):
    for i in range(0,self.N_V):
      if(len(self.VR1[i]) != 0):
          path = self.VR1[i]
    ans = {
            "name": s,
            "cost": x,
            "path": path
        }
    return ans



# sm = OptimalPath()
# sm.greedy_sol()
# sm.InterLocalSearch()
# sm.IntraLocalSearch()


def main():
  sm = OptimalPath()
  sm.greedy_sol()
  sm.IntraLocalSearch()
  sm.InterLocalSearch()

if __name__ == "__main__":
  main()
