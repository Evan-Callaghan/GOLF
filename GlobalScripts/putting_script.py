import pandas as pd
import numpy as np
import math

def initialize(putt, rounds, baselines):
    
    ## Initializing new putt features 
    putt['puttResultDistance'] = 0
    putt['locationBL'] = 0
    putt['nextLocationBL'] = 0
    putt['strokesGained'] = 0
    putt['x_coord'] = 0
    putt['y_coord'] = 0
    
    ## Initializing new round features
    rounds['Putts'] = 0
    rounds['strokesGained'] = 0
    
    ## Calling puttLevel functions
    putt = strokes_gained(putt, baselines)
    
    ## Calling roundLevel functions
    rounds = roundLevel(putt, rounds)
    
    ## Return statement
    return putt, rounds


def strokes_gained(putt, baselines):
    
    ## Location Baseline
    for i in range(0, putt.shape[0]):
        
        ## Extracting the putt distance
        distance = int(putt.at[i, 'puttDistance'])
        
        ## Assigning the SG baseline value based on the putt distance
        putt.at[i, 'locationBL'] = baselines.at[distance-1, 'Baseline']
        
    ## Next Location Baseline
    for i in range(0, putt.shape[0]):
        
        ## If the putt result is nan, then the next location baseline is 0
        if (putt.at[i, 'puttResult'] == 'Hole'):
            
            putt.at[i, 'nextLocationBL'] = 0
            
        ## Else, the putt result is the SG baseline for the next putt
        else:
            putt.at[i, 'nextLocationBL'] = putt.at[i+1, 'locationBL']
            
    ## Strokes Gained
    putt['strokesGained'] = putt['locationBL'] - putt['nextLocationBL'] - 1
    
    ## Calling next function
    putt = putt_results(putt)
    
    ## Return statement
    return putt


def putt_results(putt):
    
    ## puttResultDistance
    for i in range(0, putt.shape[0]):
        
        ## If the puttResult is 'Hole', the puttResultDistance is 0
        if (putt.at[i, 'puttResult'] == 'Hole'):
            
            putt.at[i, 'puttResultDistance'] = 0
            
        ## Else, the puttResultDistance is the puttDistance of the next observation
        else:
            putt.at[i, 'puttResultDistance'] = putt.at[i+1, 'puttDistance']
            
    ## Calling next function
    putt = resultCoordinates(putt)
    
    ## Return statement      
    return putt


def resultCoordinates(putt):
    
    ## Defining a coordinate point for each putt result
    for i in range(0, putt.shape[0]):
        
        ## Extracting the putt distance
        distance = int(putt.at[i, 'puttResultDistance'])
        
        ## Hole
        if (putt.at[i, 'puttResult'] == 'Hole'):
            putt.at[i, 'x_coord'] = 0
            putt.at[i, 'y_coord'] = 0
            
        ## N
        elif (putt.at[i, 'puttResult'] == 'N'):
            putt.at[i, 'x_coord'] = 0
            putt.at[i, 'y_coord'] = distance
            
        ## NE
        elif (putt.at[i, 'puttResult'] == 'NE'):
            putt.at[i, 'x_coord'] = distance * math.cos(math.pi / 4)
            putt.at[i, 'y_coord'] = distance * math.sin(math.pi / 4)
            
        ## E
        elif (putt.at[i, 'puttResult'] == 'E'):
            putt.at[i, 'x_coord'] = distance
            putt.at[i, 'y_coord'] = 0
            
        ## SE
        elif (putt.at[i, 'puttResult'] == 'SE'):
            putt.at[i, 'x_coord'] = distance * math.cos(-math.pi / 4)
            putt.at[i, 'y_coord'] = distance * math.sin(-math.pi / 4)
            
        ## S
        elif (putt.at[i, 'puttResult'] == 'S'):
            putt.at[i, 'x_coord'] = 0
            putt.at[i, 'y_coord'] = -distance
            
        ## SW
        elif (putt.at[i, 'puttResult'] == 'SW'):
            putt.at[i, 'x_coord'] = distance * math.cos(-3 * math.pi / 4)
            putt.at[i, 'y_coord'] = distance * math.sin(-3 * math.pi / 4)
            
        ## W
        elif (putt.at[i, 'puttResult'] == 'W'):
            putt.at[i, 'x_coord'] = -distance
            putt.at[i, 'y_coord'] = 0
            
        ## NW
        elif (putt.at[i, 'puttResult'] == 'NW'):
            putt.at[i, 'x_coord'] = distance * math.cos(3 * math.pi / 4)
            putt.at[i, 'y_coord'] = distance * math.sin(3 * math.pi / 4)
            
    ## Calling next function
    putt = reorder(putt)
    
    ## Return statement
    return putt


def reorder(putt):
    
    ## Reordering the variables in the data-frame
    putt = putt[['puttID', 'roundID', 'holeNumber', 'puttNumber', 'puttDistance', 'locationBL', 'breakCategory', 'breakDegree', 'puttResultDistance', 'puttResult', 'nextLocationBL', 'strokesGained', 'x_coord', 'y_coord']]
    
    ## Return statement
    return putt


def roundLevel(putt, rounds):
    
    ## Adding the total number of putts
    rounds['Putts'] = int(putt.groupby('holeNumber')['puttNumber'].max().sum())
    
    ## Adding the strokes gained putting for the round
    rounds['strokesGained'] = round(putt['strokesGained'].sum(), 2)
    
    ## Return statement
    return rounds