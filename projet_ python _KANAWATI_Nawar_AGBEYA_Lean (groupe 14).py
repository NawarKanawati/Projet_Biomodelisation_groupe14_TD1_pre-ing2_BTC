# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 22:53:14 2024

@author: mma
"""
# importation of libraries
import matplotlib.pyplot as plt
import csv
import math

def filterData (fileName,typeSample) :
    #open de file in reading mode
    file = open (fileName,'r')
    #allow to explore the csv file
    csvreader = csv.DictReader(file,delimiter=';')
    #creation of the dictionnary that will be used for graph building
    d=dict()
    
    dictDays = {}
    #counting days
    dictDays['treatment_start']=-7
    dictDays['treatment_day4']=-3
    dictDays['treatment_end']=0
    dictDays['washout_day1']=1
    dictDays['washout_day2']=2
    dictDays['washout_day3']=3
    dictDays['washout_day4']=4
    #creation of a dictionnary to associate ID to sample Type
    dictType = {}
    #exploration of the csv file
    for row in csvreader:
        if row['sample_type'] == typeSample:
            if typeSample == 'fecal' :
                dictType[row['mouse_ID']]= row['treatment']
                if not row['mouse_ID'] in d:
                    d[row ['mouse_ID']]= {}
                d[row['mouse_ID']][dictDays[row['timepoint']]]=math.log10(float(row['counts_live_bacteria_per_wet_g']))
            else :
                #in case in sample type is cecal or ileal, because the script for the graphs are the same
                if not row['treatment'] in d :
                    d[row['treatment']]=[]
                #association of the treatment and the number of alive bacteria (log10) in dictionary d
                d[row['treatment']].append(math.log10(float(row['counts_live_bacteria_per_wet_g'])))
    #call function saveData 
    saveData(d,dictType,typeSample)
    return (d,dictType)
    

def buildGraph (fileName,typeSample) :
    d,dictType=filterData(fileName, typeSample)
    
    # creation of dictColors dictionary that associate the treatment type with de color of graphs
    dictColors={}
    dictColors['ABX']= 'red'
    dictColors['placebo']='blue'
    
    
    if typeSample == 'fecal' :
        # for fecal graph
        figure, axes = plt.subplots()
        #fixing graph settings
        axes.set_title('Fecal live bacteria',fontsize = 20)
        axes.set_xlabel ('Washout day')
        axes.set_ylabel ('log10(live bacteria/wet g)')
        figure.legend (loc= 'upper right',fontsize=20, title='traitement')
        axes.grid(True)
        figure.savefig('Graphique_fécale.png',dpi=300)
        for k in d.keys():
            # use association of values and keys in dictionaries to know what color to use (blue for placebo and red for ABX)
            axes.plot(d[k].keys(),d[k].values(),color=dictColors [dictType[k]],label='ABX')     
        
    else :
        # we need a list to build a violin graph :
        data=list()
        # selection of values according to their association in dictionary d : 
        for e in d.keys():
            
            #if OK, a dictionary (value and key) is added in the list data
            data.append(d[e])

        #fixing violin graphs settings
        figure, axes = plt.subplots()
        axes.set_title(typeSample+' live bacteria',fontsize = 20)
        axes.set_xlabel ('Treatment')
        axes.set_ylabel ('log10(live bacteria/wet g)')
        axes.grid(True)
        # no values in x axe
        axes.set_xticks([])
        figure.savefig('Graphique_'+typeSample+'.png',dpi=300)
        parts = axes.violinplot(data,showextrema = True,showmedians=True)
        # speraration of the 2 violin graph following their indexation
        for idx , body in enumerate (parts['bodies']) :
            # selection of the right color with the values of the dictionary dictColors 
            body.set_facecolor(list(dictColors.values())[idx])
    # showing graphs
    plt.show()
    
def saveData(d,dT,typeSample):
    # opening a csv file in writing mode
  f = open (typeSample+'_data.csv',"w")
    
  if typeSample == 'fecal' :
      # creation of the first line (column title)
      f.write('mouse_ID;treatment;timepoint;counts_live_bacteria_per_wet_g\n')
      for k in d.keys():
          #associating values into the right columns by searchings keys in dictionary d, made following filterData
          line = str(k)+';'+str(dT[k])+';'
          # searching in sub-dictionary conatain in dT(here dictType)
          for t in d[k].keys():
              line = line + str(t) +';'+ str(d[k][t])
          # remove te last line    
          line = line + '\n'
          f.write (line)
      f.close()
  else : 
      # same cecal/ileal data : 
      f.write('treatment;counts_live_bacteria_per_wet_g\n')
      for k in d.keys():
          line =str(k)+';'
          for e in d[k] :
              line = line + str(e)+'\n'
              f.write (line)
      f.close()  
                
            
          
   




sample = ['fecal','cecal','ileal']
# exploration of sample list
for s in sample :
    #calling buildGraph
    buildGraph('data_real (1).csv', s)


    
