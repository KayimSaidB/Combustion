

# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 15:56:34 2020

@author: fanny.lecarpentier
"""

import gurobipy as gb
from gurobipy import multidict
import numpy as np
M = gb.Model('Co-combustion_20ans')
# help(M1)
# help(M1.addVar)
# help(M1.addConstrs)

GES_torrefie_prod=1.7E-3  #GES pour la production en tCo2/t
GES_torrefie_transport_mar=0.015E-3 #GES pour le transport maritime en tCo2/km
GES_torrefie_transport_terr=0.09E-3 #GES pour le transport terrestre en tCo2/km

GES_vert_prod=0.1E-3  #GES pour la production en tCo2/t
GES_vert_transport=0.16E-3 #GES pour le transport terrestre en tCo2/km

GES_recycle_prod_et_tranport=0.01  #GES pour la production et le transport en tCo2/t

GES_frais_prod=1.3E-3  #GES pour la production en tCo2/t
GES_frais_transport=0.16E-3 #GES pour le transport terrestre en tCo2/k

prix_vente_quota=5 #prix de vente de 1 quota (couvrant 1t de CO2) en euros
quota=sorted(5*[i for i in range(80000,0,-20000)])[::-1]


####### Definition des données du pb
combustible, PCI,ratio_sec, cout, prix_vente_elect, emission_GES, dispo_avant2025, dispo_apres2025= multidict({ #PCI en MWh/t, cout en euros/t, prix_vente_elect en euros/MWh, emission GES en tCO2/t
        'charbon':                 [25000/3600,            1,30,  43, 3, 1E24, 1E24],
        'torrefie':              [18000/3600,            1,190, 115, (GES_torrefie_prod+GES_torrefie_transport_mar*7000+GES_torrefie_transport_terr*250), 700E3,    0],
        'NS_vert':               [(18000-21000*0.4)/3600,  1,0, 115, (GES_vert_prod+GES_vert_transport*80)*0,                                                0, 0],
        'AS_vert':                  [(18000-21000*0.05)/3600,  0.65,0, 115, (GES_vert_prod+GES_vert_transport*80)*0,                                                313E3, 313E3],
        'recycle':                   [(18000-21000*0.05)/3600,  1,0, 115, (GES_vert_prod+GES_vert_transport*80)*0,                                                313E3, 313E3],
         'AS_frais_Aigoual':        [(18000-21000*0.05)/3600,0.85,128, 115, (GES_frais_prod+GES_frais_transport*230)*0,                                             18E3, 21E3],
        'AS_frais_Cevennes30':      [(18000-21000*0.05)/3600,0.85 ,120, 115, (GES_frais_prod+GES_frais_transport*210)*0,                                             21E3, 43E3],
        'AS_frais_Cevennes48':      [(18000-21000*0.05)/3600, 0.85,128, 115, (GES_frais_prod+GES_frais_transport*230)*0,                                             12E3, 75E3],
        'AS_frais_Cevennes07':      [(18000-21000*0.05)/3600, 0.85,116, 115, (GES_frais_prod+GES_frais_transport*200)*0,                                              8E3, 56E3],
       'AS_frais_BoucheDuRhone':   [(18000-21000*0.05)/3600,  0.85,44, 115, (GES_frais_prod+GES_frais_transport*20)*0,                                              47E3, 51E3],
        'AS_frais_Vaucluse':        [(18000-21000*0.05)/3600,  0.85,79, 115, (GES_frais_prod+GES_frais_transport*100)*0,                                             24E3, 28E3],
        'AS_frais_Var':             [(18000-21000*0.05)/3600, 0.85 ,60, 115, (GES_frais_prod+GES_frais_transport*60)*0,                                              27E3, 27E3],
        'AS_frais_HauteAples':      [(18000-21000*0.05)/3600, 0.85,100, 115, (GES_frais_prod+GES_frais_transport*160)*0,                                             15E3, 21E3],
        'AS_frais_AplesHteProvence':[(18000-21000*0.05)/3600,  0.85,88, 115, (GES_frais_prod+GES_frais_transport*130)*0,                                             26E3, 37E3],
       'AS_frais_Autres1':         [(18000-21000*0.05)/3600, 0.85,116, 115, (GES_frais_prod+GES_frais_transport*200)*0,                                             27E3, 27E3],
        'AS_frais_Autres2':         [(18000-21000*0.05)/3600, 0.85,156, 115, (GES_frais_prod+GES_frais_transport*300)*0,                                             56E3, 56E3],
        'AS_frais_Autres3':         [(18000-21000*0.05)/3600, 0.85,196, 115, (GES_frais_prod+GES_frais_transport*400)*0,                                            56E3, 56E3],
        'NS_frais_Aigoual':         [(18000-21000*0.2)/3600, 1, 128, 115, (GES_frais_prod+GES_frais_transport*230)*0,                                            0, 0],
        'NS_frais_Cevennes30':      [(18000-21000*0.2)/3600, 1,120, 115, (GES_frais_prod+GES_frais_transport*210)*0,                                             0, 0],
        'NS_frais_Cevennes48':      [(18000-21000*0.2)/3600, 1,128, 115, (GES_frais_prod+GES_frais_transport*230)*0,                                             0, 0],
        'NS_frais_Cevennes07':      [(18000-21000*0.2)/3600,1, 116, 115, (GES_frais_prod+GES_frais_transport*200)*0,                                              0, 0],
       'NS_frais_BoucheDuRhone':   [(18000-21000*0.2)/3600,  1,44, 115, (GES_frais_prod+GES_frais_transport*20)*0,                                              0, 0],
        'NS_frais_Vaucluse':        [(18000-21000*0.2)/3600,  1,79, 115, (GES_frais_prod+GES_frais_transport*100)*0,                                             0, 0],
        'NS_frais_Var':             [(18000-21000*0.2)/3600,  1,60, 115, (GES_frais_prod+GES_frais_transport*60)*0,                                              0, 0],
        'NS_frais_HauteAples':      [(18000-21000*0.2)/3600, 1,100, 115, (GES_frais_prod+GES_frais_transport*160)*0,                                             0, 0],
        'NS_frais_AplesHteProvence':[(18000-21000*0.2)/3600, 1, 88, 115, (GES_frais_prod+GES_frais_transport*130)*0,                                             0, 0],
       'NS_frais_Autres1':         [(18000-21000*0.2)/3600, 1,116, 115, (GES_frais_prod+GES_frais_transport*200)*0,                                             0, 0],
        'NS_frais_Autres2':         [(18000-21000*0.2)/3600, 1,156, 115, (GES_frais_prod+GES_frais_transport*300)*0,                                             0, 0],
        'NS_frais_Autres3':         [(18000-21000*0.2)/3600, 1,196, 115, (GES_frais_prod+GES_frais_transport*400)*0,                                             0, 0]
    })
dico={}
for c in combustible :
    if c[0:2]=="AS": 
        dico[c]="NS"+c[2:len(c)]

Eff         = 0.38           # Efficacité
P_Nominal   = 150            # Puissance Nominale (en MWe)
fc          = 7500           # Facteur de charge (en heures / an)
T_act       = 0.02           # Taux actualisation
E_Prod_Therm = P_Nominal * fc / Eff # Production thermique annuelle
taux_C_min = 0.1
prix_under=215*0.0036
prix_over=430*0.0036
stock_min=365*1500
#stock_max=stock_min*2
disponibilite_rv=np.array([1000,7000,22000,29000,52000,57000,143000,21000,313000])
prix_unitaire_rv=np.array([4,7,10,16,25,31,46,61,76])
cout_fixe_stock=500000 #euros
prix_total_rv=disponibilite_rv*prix_unitaire_rv
route_rv=np.array([10,20,30,50,80,100,150,200,250])
cout_vert=20*[0]
cout_sechage=20*[0]
capa_grand_secheur=150000
capa_petit_secheur=50000
cout_petit_secheur=300000*0
cout_grand_secheur=600000*0
# profit en euros pour 1 unité de combustible 'comb' l'année'an'
def unit_profit(comb, an):
    return (Eff * PCI[comb] * prix_vente_elect[comb] * ratio_sec[comb] - cout[comb] - prix_vente_quota*emission_GES[comb])

####### Definition des variables
# masse de combustible par an 
mass = M.addVars(combustible, 20, lb=0, vtype=gb.GRB.CONTINUOUS) 
lambda_rv=M.addVars(9, 20,vtype=gb.GRB.CONTINUOUS,ub=1)
for i in range(20):
    M.addSOS(gb.GRB.SOS_TYPE2,[lambda_rv[j,i] for j in range(9)])

M.update()

activation=M.addVars(20, vtype=gb.GRB.BINARY) # vaut 
activation_stockage=M.addVars(20, vtype=gb.GRB.BINARY) # vaut 1 l'annee ou on a debloque du stockage 0 sinon
activation_stockage_sum=M.addVars(20, vtype=gb.GRB.BINARY) # vaut 1 si on a debloque du stoackage

cout_variable_biomasse=M.addVars(20, vtype=gb.GRB.CONTINUOUS) # valeur du cout variable associé à la biomasse
nb_petit_secheur=M.addVars(20, vtype=gb.GRB.INTEGER)
nb_grand_secheur=M.addVars(20, vtype=gb.GRB.INTEGER)

####### Definition des contrainte/an
ctrs = {}
profit = {}

#M.addConstr(gb.quicksum(activation_stockage)<=1) #contrainte de stock sur l'ensemble de la simulation
M.addConstr(gb.quicksum(nb_petit_secheur[i]+nb_grand_secheur[i]for i in range(20))<=5 ) #contrainte de stock sur l'ensemble de la simulation

for i in range (20):
    
    ctrs['mincharbon', i] = M.addConstr((1-taux_C_min) * mass['charbon', i] - taux_C_min * (gb.quicksum(mass[c,i] for c in combustible if c!='charbon')) >= 0, name='10pourcent_min_charbon')
    ctrs['prod', i] = M.addConstr(gb.quicksum(mass[c,i] * PCI[c] for c in combustible) == E_Prod_Therm, name='prod_suffisante')
    ctrs['apro_torrefie', i] = M.addConstr(mass['torrefie', i] <= dispo_avant2025['torrefie'], name='appro_torrefie_max')
 #   ctrs['apro_vert', i] = M.addConstr(mass['vert', i] <=dispo_avant2025['vert'] , name='appro_vert_max')
   # ctrs['max_biomasse',i]=M.addConstr(gb.quicksum(mass[c,i] for c in combustible if c!='charbon') <= 150e3)
    if i<=10:
        ctrs['apro_avant2025 non seche', i] = M.addConstrs((mass[c, i] <= dispo_avant2025[c] for c in combustible if c!='charbon' and c[0:2]!="AS" and c[0:2]!="NS"), name='appro_avant2025_max non seche')
        ctrs['apro_avant2025 a secher', i] = M.addConstrs((mass[c, i]+mass[dico[c],i] <= dispo_avant2025[c] for c in combustible if c[0:2]=='AS') ,name='appro_avant2025_max a secher')

    else:
        ctrs['apro_apres2025, non seche', i] = M.addConstrs((mass[c, i] <= dispo_apres2025[c] for c in combustible if c!='charbon' and c[0:2]!="AS" and c[0:2]!="NS"), name='appro_apres2025_max non seche')
        ctrs['apro_apres2025 a secher', i] = M.addConstrs((mass[c, i]+mass[dico[c],i] <= dispo_apres2025[c] for c in combustible if c[0:2]=='AS') ,name='appro_apres2025_max a secher')
    #if i<=10:
    #    ctrs['apro_local', i] = M.addConstr(0.4*(mass['vert', i]+mass['recycle', i])-0.6*mass['torrefie', i]>=0 , name='appro_local_min')
    #else:
        #ctrs['apro_local', i] = M.addConstr(mass['torrefie', i] == dispo_apres2025['torrefie'] , name='appro_local_min') 
    ctrs['Ctrs CV biomasse 1',i]=M.addConstr(cout_variable_biomasse[i]>=prix_over*gb.quicksum(mass[c,i]*PCI[c] for c in combustible)-10e15*(1-activation[i]))
    ctrs['Ctrs CV biomasse 2',i]=M.addConstr(0.5*gb.quicksum(mass[c,i] for c in combustible)>=gb.quicksum(mass[c,i] for c in combustible if c!='charbon')-10e15*activation[i])
    ctrs["Ctrs CV biomasse 3",i]=M.addConstr(cout_variable_biomasse[i]>=prix_under*gb.quicksum(mass[c,i]*PCI[c] for c in combustible))
    ctrs["Ctrs fct lineaire vert 1",i]=M.addConstr(gb.quicksum(disponibilite_rv[k]*lambda_rv[k,i] for k in range(9))==mass['AS_vert',i]+mass['NS_vert',i])
    ctrs["Ctrs fct lineaire vert 2",i]=M.addConstr(gb.quicksum(lambda_rv[k,i] for k in range(9))<=1 )
   # ctrs["Contrainte stock 2",i]=M.addConstr(gb.quicksum(mass[c,i] for c in combustible if c!='charbon')<=stock_min+stock_min*gb.quicksum(activation_stockage[k] for k in range(i+1))+stock_min*activation_stockage_sum[i])
   # ctrs["Ctrs stock 3"]=M.addConstr(gb.quicksum(activation_stockage[k] for k in range(i))==activation_stockage_sum[i])
    # ctrs["Contrainte stock 3",i]=M.addConstr(gb.quicksum(mass[c,i] for c in combustible if c!='charbon')<=10e7+(stock_min-10e7)*(1-activation_stockage[i]))
   # ctrs["Ctrs capa sechage",i]=gb.quicksum(mass[c,i] for c in combustible if c[0:2]=='AS')<=gb.quicksum(nb_petit_secheur[k]*capa_petit_secheur+nb_grand_secheur[k]*capa_grand_secheur for k in range(i+1)) #deux premieres lettres correspondent à AS
    cout_vert[i]=gb.quicksum(prix_total_rv[k]*lambda_rv[k,i] for k in range(9))
    cout_sechage[i]=nb_grand_secheur[i]*cout_grand_secheur+nb_petit_secheur[i]*cout_petit_secheur
    profit[i] = gb.quicksum(unit_profit(c,i) * mass[c,i] for c in combustible)-cout_vert[i]+quota[i]-cout_variable_biomasse[i]-cout_sechage[i]#-cout_fixe_stock*activation_stockage[i]

M.setObjective(gb.quicksum(profit[i]  / (1 + T_act) ** i for i in range(20)))
M.modelSense = gb.GRB.MAXIMIZE


###### Optimization
M.write('monmodele.lp')
M.optimize()
assert M.status == gb.GRB.status.OPTIMAL, f"solver stopped with status {M.status}"

###### Affichage des résultats
for i in (0,19):
    print(f"masse de combustibles à année {i+1} est :")
    for c in combustible:
        print(f"{c}: {mass[c,i].x:.1f}")
    print(f"profit pour année {i+1} = {profit[i].getValue():.2f}")
    ratio = mass['charbon',i].x / sum(mass[c,i].x for c in combustible)
    print(f"ratio charbon/masse totale à  année {i+1} est : {ratio*100:.1f} %")

#Sensibilité
#print(f"sensibilite: {ctrs['mincharbon',0].pi}, {ctrs['mincharbon',0].slack}, {mass['charbon',0].rc}")
