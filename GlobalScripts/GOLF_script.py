## Strokes Gained Analysis - Evan Callaghan

## Python script file for all code that that creates a final Strokes Gained data set for analysis in Python and Tableau.

import pandas as pd
import numpy as np

## Completing joins between data-frames
def initialize(shot, rounds, courses, baselines):
    
    ## Initializing an empty data-frame to store final Strokes Gained information
    strokes = pd.DataFrame()
    
    ## Joining Shot and Rounds data-frames
    strokes = shot.merge(rounds[['roundID', 'courseID', 'Tees', 'holesPlayed']], on = 'roundID', how = 'left')
    
    ## Joining Strokes and Courses data-frames
    strokes = strokes.merge(courses, on = ['courseID', 'Tees', 'holeNumber'], how = 'left')
    
    ## Calling subsequent function
    strokes = cleaning(strokes)
    
    ## Calling baseline function
    strokes = locationBL(strokes, baselines)
    
    ## Return statement
    return strokes


def cleaning(strokes):
    
    ## Creating new variables within the Strokes data-frame
    strokes['shotCategory'] = ''
    strokes['Location'] = 0
    strokes['locationLieType'] = ''
    strokes['locationBL'] = 0
    strokes['nextLocationBL'] = 0
    strokes['penaltyStrokeValue'] = 0
    strokes['strokesGained'] = 0
    strokes['grossStrokes'] = 0
    strokes['Putt'] = 0
    strokes['Fairway'] = 0
    strokes['GIR'] = 0

    strokes['holeNumber'] = strokes['holeNumber'].astype(int)
    strokes['shotNumber'] = strokes['shotNumber'].astype(int)
    strokes['nextLocation'] = strokes['nextLocation'].astype(float)
    strokes['Location'] = strokes['Location'].astype(float)
    strokes['nextLocationBL'] = strokes['nextLocationBL'].astype(float)
    strokes['locationBL'] = strokes['locationBL'].astype(float)
    strokes['penaltyStrokeValue'] = strokes['penaltyStrokeValue'].astype(int)
    strokes['strokesGained'] = strokes['strokesGained'].astype(float)
    strokes['grossStrokes'] = strokes['grossStrokes'].astype(int)
    strokes['Putt'] = strokes['Putt'].astype(int)
    strokes['Fairway'] = strokes['Fairway'].astype(int)
    strokes['GIR'] = strokes['GIR'].astype(int)
    
    ## Calling subsequent function
    strokes = location(strokes)
    
    ## Return statement
    return strokes
    
    
def location(strokes):
    
    ## Setting n equal to the number of shots in the Strokes data-frame
    n = strokes.shape[0]
    
    ## Looping through each shot for conditional statements
    for i in range(0, n):
        
        ## Location ##
        
        ## If the shotNumber is one, then the Location is the holeYardage
        if (strokes.at[i, 'shotNumber'] == 1):
            strokes.at[i, 'Location'] = strokes.at[i, 'holeYardage']
    
        ## Else, the Location is the nextLocation of the previous shot
        else:
            strokes.at[i, 'Location'] = strokes.at[i-1, 'nextLocation']
            
        ## locationLieType ##
        
        ## If the shotNumber is one, then the locationLieType is 'Tee'
        if (strokes.at[i, 'shotNumber'] == 1):
            strokes.at[i, 'locationLieType'] = 'Tee'
    
        ## Else, the locationLieType is the nextLocationLieType of the previous shot
        else:
            strokes.at[i, 'locationLieType'] = strokes.at[i-1, 'nextLocationLieType']
    
    ## Calling subsequent function
    strokes = shotCategory(strokes)
    
    ## Return statement
    return strokes


def shotCategory(strokes):  

    ## Setting n equal to the number of shots in the Strokes data-frame
    n = strokes.shape[0]

    ## Looping through each shot for conditional statements
    for i in range(0, n):
    
        ## If the shotNumber is one, then the shotCategory is either 'Tee' or 'Approach'
        if (strokes.at[i, 'shotNumber'] == 1):
            
            ## If the holePar is three, then the shotCategory is 'Approach'
            if (strokes.at[i, 'holePar'] == 3):
                strokes.at[i, 'shotCategory'] = 'Approach'
                
            ## Else (Par 4 or 5), the shot category is 'Tee'
            else:
                strokes.at[i, 'shotCategory'] = 'Tee'
    
        ## Else-if the locationLieType is 'Green', then the shot category is 'Putt'
        elif (strokes.at[i, 'locationLieType'] == 'Green'):
            strokes.at[i, 'shotCategory'] = 'Putt'
        
        ## Else-if Location <= 45, then shot category is 'Around-the-Green'
        elif (strokes.at[i, 'Location'] <= 45):
             strokes.at[i, 'shotCategory'] = 'Around-the-Green'
        
        else:
            strokes.at[i, 'shotCategory'] = 'Approach'
    
    ## Calling subsequent function
    strokes = penaltyStrokeValue(strokes)
    
    ## Return statement
    return strokes


def penaltyStrokeValue(strokes):
    
    ## Setting n equal to the number of shots in the Strokes data-frame
    n = strokes.shape[0]

    ## Looping through each shot for conditional statements
    for i in range(0, n):
        
        ## If penaltyIncurred is 'PA', then penaltyStrokeValue is 1
        if (strokes.at[i, 'penaltyIncurred'] == 'PA'):
            strokes.at[i, 'penaltyStrokeValue'] = 1
        
        ## Else-if penaltyIncurred is 'OB', then penaltyStrokeValue is 2
        elif (strokes.at[i, 'penaltyIncurred'] == 'OB'):
            strokes.at[i, 'penaltyStrokeValue'] = 2
        
        ## Else, penaltyStrokeValue is 0
        else:
            strokes.at[i, 'penaltyStrokeValue'] = 0
    
    ## Return statement
    return strokes


def locationBL(strokes, baselines):
    
    ## Subsetting the baseline date-frame into 'shotBL' and 'puttBL'
    shotBL = baselines[baselines['Type'] == 'Shot'].reset_index(drop = True)
    puttBL = baselines[baselines['Type'] == 'Putt'].reset_index(drop = True)
    
    ## Setting n equal to the number of shots in the Strokes data-frame
    n = strokes.shape[0]

    ## Looping through each shot for conditional statements
    for i in range(0, n):
        
        ## If the locationLieType is 'Green'...
        if (strokes.at[i, 'locationLieType'] == 'Green'):
            
            ## Yardage is equal to Location
            yardage = int(strokes.at[i, 'Location'])
            
            ## locationBL is equal to the average number of strokes to hole-out from that yardage
            strokes.at[i, 'locationBL'] = puttBL.at[yardage-1, 'Green']
        
        ## Else...
        else:
            
            ## If locationLieType is 'Tee', then
            if (strokes.at[i, 'locationLieType'] == 'Tee'):
                
                ## Yardage is equal to Location
                yardage = int(strokes.at[i, 'Location'])
                
                ## LocationBL is set to the average number of strokes to hole-out from that yardage
                strokes.at[i, 'locationBL'] = shotBL.at[yardage-3, 'Tee']
            
            ## If locationLieType is 'Fairway', then
            elif (strokes.at[i, 'locationLieType'] == 'Fairway'):
                
                ## Yardage is equal to Location
                yardage = int(strokes.at[i, 'Location'])
                
                ## locationBL is set to the average number of strokes to hole-out from that yardage
                strokes.at[i, 'locationBL'] = shotBL.at[yardage-3, 'Fairway']
            
            ## If locationLieType is 'Rough', then
            elif (strokes.at[i, 'locationLieType'] == 'Rough'):
                
                ## Yardage is equal to Location
                yardage = int(strokes.at[i, 'Location'])
                
                ## locationBL is set to the average number of strokes to hole-out from that yardage
                strokes.at[i, 'locationBL'] = shotBL.at[yardage-3, 'Rough']
                
            ## If locationLieType is 'Fescue', then
            elif (strokes.at[i, 'locationLieType'] == 'Fescue'):
                
                ## Yardage is equal to Location
                yardage = int(strokes.at[i, 'Location'])
                
                ## locationBL is set to the average number of strokes to hole-out from that yardage
                strokes.at[i, 'locationBL'] = shotBL.at[yardage-3, 'Rough']
                
            ## If locationLieType is 'Sand', then
            elif (strokes.at[i, 'locationLieType'] == 'Sand'):
                
                ## Yardage is equal to Location
                yardage = int(strokes.at[i, 'Location'])
                
                ## locationBL is set to the average number of strokes to hole-out from that yardage
                strokes.at[i, 'locationBL'] = shotBL.at[yardage-3, 'Sand']
    
    ## Calling subsequent function
    strokes = nextLocationBL(strokes, baselines)
    
    ## Return statement
    return strokes


def nextLocationBL(strokes, baselines):
    
    ## Subsetting the baseline date-frame into 'shotBL' and 'puttBL'
    shotBL = baselines[baselines['Type'] == 'Shot'].reset_index(drop = True)
    puttBL = baselines[baselines['Type'] == 'Putt'].reset_index(drop = True)
    
    ## Setting n equal to the number of shots in the Strokes data-frame
    n = strokes.shape[0]
    
    ## Looping through each shot for conditional statements
    for i in range(0, n):
        
        ## If nextLocationLieType is 'Hole', then the nextLocationBL is zero
        if (strokes.at[i, 'nextLocationLieType'] == 'Hole'):
            
            strokes.at[i, 'nextLocationBL'] = 0
            
        ## Else-if the nextLocationLieType is 'Green'...
        elif (strokes.at[i, 'nextLocationLieType'] == 'Green'):
            
            ## Yardage is equal to nextLocation
            yardage = int(strokes.at[i, 'nextLocation'])
            
            ## nextLocationBL is equal to the average number of strokes to hole-out from that yardage
            strokes.at[i, 'nextLocationBL'] = puttBL.at[yardage-1, 'Green']
        
        ## Else...
        else:
            
            ## If nextLocationLieType is 'Tee', then
            if (strokes.at[i, 'nextLocationLieType'] == 'Tee'):
                
                ## Yardage is equal to nextLocation
                yardage = int(strokes.at[i, 'nextLocation'])
                
                ## nextLocationBL is set to the average number of strokes to hole-out from that yardage
                strokes.at[i, 'nextLocationBL'] = shotBL.at[yardage-3, 'Tee']
            
            ## If nextLocationLieType is 'Fairway', then
            elif (strokes.at[i, 'nextLocationLieType'] == 'Fairway'):
                
                ## Yardage is equal to nextLocation
                yardage = int(strokes.at[i, 'nextLocation'])
                
                ## nextLocationBL is set to the average number of strokes to hole-out from that yardage
                strokes.at[i, 'nextLocationBL'] = shotBL.at[yardage-3, 'Fairway']
            
            ## If nextLocationLieType is 'Rough', then
            elif (strokes.at[i, 'nextLocationLieType'] == 'Rough'):
                
                ## Yardage is equal to nextLocation
                yardage = int(strokes.at[i, 'nextLocation'])
                
                ## nextLocationBL is set to the average number of strokes to hole-out from that yardage
                strokes.at[i, 'nextLocationBL'] = shotBL.at[yardage-3, 'Rough']
            
             ## If nextLocationLieType is 'Fescue', then
            elif (strokes.at[i, 'nextLocationLieType'] == 'Fescue'):
                
                ## Yardage is equal to Location
                yardage = int(strokes.at[i, 'nextLocation'])
                
                ## nextLocationBL is set to the average number of strokes to hole-out from that yardage
                strokes.at[i, 'nextLocationBL'] = shotBL.at[yardage-3, 'Rough']
                
            ## If nextLocationLieType is 'Sand', then
            elif (strokes.at[i, 'nextLocationLieType'] == 'Sand'):
                
                ## Yardage is equal to Location
                yardage = int(strokes.at[i, 'nextLocation'])
                
                ## nextLocationBL is set to the average number of strokes to hole-out from that yardage
                strokes.at[i, 'nextLocationBL'] = shotBL.at[yardage-3, 'Sand']
    
    ## Calling subsequent function
    strokes = strokesGained(strokes)
    
    ## Return statement
    return strokes


def strokesGained(strokes):
    
    ## Setting n equal to the number of shots in the Strokes data-frame
    n = strokes.shape[0]
    
    ## Looping through each shot for conditional statements
    for i in range (0, n):
        
        ## Strokes Gained = locationBL - nextLocationBL - 1 - penaltyStrokeValue
        strokes.at[i, 'strokesGained'] = strokes.at[i, 'locationBL'] - strokes.at[i, 'nextLocationBL'] - 1 - strokes.at[i, 'penaltyStrokeValue']
        
    ## Rounding strokesGained values to two decimal places
    strokes['strokesGained'] = strokes['strokesGained'].round(3)
    
    ## Calling subsequent function
    strokes = traditionals(strokes)
    
    ## Return statement
    return strokes


def traditionals(strokes):
    
    ## Strokes
    ## The grossStrokes of a shot is one plus the number of penalty strokes incurred on that particular shot
    strokes['grossStrokes'] = 1 + strokes['penaltyStrokeValue']
    
    ## Putts
    ## When shot category is 'Putt', putts = 1. ELse, 0
    strokes['Putt'] = np.where(strokes['shotCategory'] == 'Putt', 1, 0)
    
    ## Driving Accuracy
    ## When shot category is 'Tee', and nextLocationLieType is 'Fairway', Fairway = 1. Else, 0
    strokes['Fairway'] = np.where((strokes['shotCategory'] == 'Tee') & (strokes['nextLocationLieType'] == 'Fairway'), 1, 0)
    
    ## Greens-in-Regulation
    ## Setting n equal to the number of shots in the Strokes data-frame
    n = strokes.shape[0]
    
    ## Looping through each shot for conditional statements
    for i in range (0, n):
        
        ## If holePar is three...
        if (strokes.at[i, 'holePar'] == 3):
            
            ## If shotNumber is one and the nextLocationLieType is 'Hole' or 'Green', then GIR is one
            if (strokes.at[i, 'shotNumber'] == 1 and (strokes.at[i, 'nextLocationLieType'] == 'Hole' or strokes.at[i, 'nextLocationLieType'] == 'Green')):
                strokes.at[i, 'GIR'] = 1

            ## Else, GIR is zero
            else:
                strokes.at[i, 'GIR'] = 0
                
        ## Else-if holePar is four...
        elif (strokes.at[i, 'holePar'] == 4):
            
            ## If shotNumber is one and the nextLocationLieType is 'Hole' or 'Green', then GIR is one
            if (strokes.at[i, 'shotNumber'] == 1 and (strokes.at[i, 'nextLocationLieType'] == 'Hole' or strokes.at[i, 'nextLocationLieType'] == 'Green')):
                strokes.at[i, 'GIR'] = 1
                
            ## Else-if shotNumber is two and the nextLocationLieType is 'Hole' or 'Green', then GIR is one
            elif (strokes.at[i, 'shotNumber'] == 2 and (strokes.at[i, 'nextLocationLieType'] == 'Hole' or strokes.at[i, 'nextLocationLieType'] == 'Green')):
                strokes.at[i, 'GIR'] = 1
            
            ## Else, GIR is zero
            else:
                strokes.at[i, 'GIR'] = 0
        
        ## Else-if holePar is five...
        elif (strokes.at[i, 'holePar'] == 5):
            
            ## If shotNumber is one and the nextLocationLieType is 'Hole' or 'Green', then GIR is one
            if (strokes.at[i, 'shotNumber'] == 1 and (strokes.at[i, 'nextLocationLieType'] == 'Hole' or strokes.at[i, 'nextLocationLieType'] == 'Green')):
                strokes.at[i, 'GIR'] = 1
                
            ## Else-if shotNumber is two and the nextLocationLieType is 'Hole' or 'Green', then GIR is one
            elif (strokes.at[i, 'shotNumber'] == 2 and (strokes.at[i, 'nextLocationLieType'] == 'Hole' or strokes.at[i, 'nextLocationLieType'] == 'Green')):
                strokes.at[i, 'GIR'] = 1
            
            ## Else-if shotNumber is three and the nextLocationLieType is 'Hole' or 'Green', then GIR is one
            elif (strokes.at[i, 'shotNumber'] == 3 and (strokes.at[i, 'nextLocationLieType'] == 'Hole' or strokes.at[i, 'nextLocationLieType'] == 'Green')):
                strokes.at[i, 'GIR'] = 1
            
            ## Else, GIR is zero
            else:
                strokes.at[i, 'GIR'] = 0 
    
    ## Return statement
    return strokes