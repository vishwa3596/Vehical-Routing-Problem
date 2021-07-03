import numpy as np
import argparse
import pandas as pd
import math
import itertools

deposit_rate= 14
cash_upload_cost= 100
curr_money=np.array([600,1500,700,400,1500,500,2000,5000])
cash_upload_arr=[200,200,150,150,200,300,400]

def get_all_comb_days():
    days=[0,1,2,3,4,5,6]
    all_comb=[]
    for r in range(len(days)+1):
        temp=list(itertools.combinations(days,r))
        all_comb+=temp
    return all_comb

def get_atm_count(day,drain_arr):
    ans=0
    for i in range(day-1):
        ans+=len(drain_arr[i])
    return ans

def get_drain_out_day(forecast):
    drain_out_map=[]
    temp=curr_money
    for i in range(0,7):
        temp=np.subtract(temp,forecast[i])
        em_list=[]
        for j in range(0,len(temp)):
            if(temp[j]<=0):
                em_list.append(j+1)
                temp[j]=1000000
        drain_out_map.append(em_list)
    # print(drain_out_map)
    return drain_out_map

def parse_arguments():
    parser = argparse.ArgumentParser(description='Next Replenishment Optimisation')
    parser.add_argument('--bank_branch', default='sample_branch', type=str,required=False, help='mention the bank branch for which replenishment gaps is to be obtained')
    args = parser.parse_args()
    return args

def get_forecast(bank_branch):
    path='../src/Datasets/'+bank_branch+'_forecasts.xlsx'
    df=pd.read_excel(path)
    arr= df.to_numpy()
    return arr

def drain_day(atm_id,drain_arr):
    for i in range(len(drain_arr)):
        for j in range(len(drain_arr[i])):
            if(drain_arr[i][j]==atm_id):
                return j

def total_rep_amount(atm_id,forecast,drain_arr):
    ans=0
    for j in range(len(atm_id)):
        temp=forecast[drain_day(atm_id[j],drain_arr):,(atm_id[j]-1)]
        ans+=np.sum(temp,axis=0)
    return ans

def get_atm_list(day1,day2,drain_arr):
    atm_list=np.array([])
    for i in range(day1,day2):
        atm_list=np.append(atm_list,drain_arr[i])
    atm_list=atm_list.astype(int)
    return atm_list

def solve_mega_optimisation(forecast,drain_arr,mega_set):
    fir_rep_must_day=-1
    for i in range(len(drain_arr)):
        if(len(drain_arr[i])!=0):
            fir_rep_must_day=i
            break

    if(fir_rep_must_day==-1):
        print("No replenishment required for the week")
        return

    cost_glob=1000000
    ans_glob=np.array([])
    for i in range(1,len(mega_set)):
        cost=0
        rep_day=np.array(mega_set[i])
        rep_days=np.append(rep_day,7)
        # print(rep_days)
        # print(drain_arr)
        if(rep_days[0]>fir_rep_must_day):
            cost=10000000000000000000
        else:
            for j in range(len(rep_days)-1):
                atm_list=get_atm_list(rep_days[j],rep_days[j+1],drain_arr)
                cost+=len(atm_list)*cash_upload_arr[rep_days[j]]+deposit_rate*((7-rep_days[j])/365)*total_rep_amount(atm_list,forecast,drain_arr)/100

        # print(cost,"\n\n")
        if(cost_glob>cost):
            ans_glob=rep_day
            cost_glob=cost

    print("Min cost is: ",cost_glob)
    print("Days to be replenished: ",ans_glob)


def main(args):
    forecast=get_forecast(args.bank_branch)
    drain_arr=get_drain_out_day(forecast)
    mega_set=get_all_comb_days()
    print(forecast)
    print( " drain value ", drain_arr)
    # total_rep_amount(1,4,drain_arr,forecast)
    solve_mega_optimisation(forecast,drain_arr,mega_set)

if __name__=='__main__':
    args=parse_arguments()
    main(args)
