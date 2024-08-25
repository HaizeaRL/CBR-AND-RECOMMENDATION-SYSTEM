# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 12:15:00 2024
@author: Haizea Rumayor

"""
# FUNCTIONS

"""
Acidez fija (Fixed Acidity): 
Generalmente se refiere a la acidez no volátil del vino, como el ácido tartárico y ácido málico.
Una alta acidez fija suele asociarse con una mayor frescura y vivacidad en el vino.
Los rangos más altos pueden indicar un vino con una acidez más pronunciada.
Rango Bajo: 3.0 - 5.0 g/L
Rango Medio: 5.0 - 7.0 g/L
Rango Alto: > 7.0 g/L
"""
def classify_fixed_acidity(fixed_acidity):
    if fixed_acidity <= 5.0:
        return 'Low'
    elif 5.0 < fixed_acidity <= 7.0:
        return 'Medium'
    else:
        return 'High'

"""
Acidez Volátil (Volatile Acidity): Se refiere a los ácidos volátiles que pueden contribuir a la
percepción de acidez y a veces a defectos si están en niveles altos. 
Una alta acidez volátil puede dar lugar a aromas no deseados, como el vinagre.

Rango Bajo: < 0.4 g/L
Rango Medio: 0.4 - 0.7 g/L
Rango Alto: > 0.7 g/L
"""

def classify_volatile_acidity(volatile_acidity):
    if volatile_acidity <= 0.4:
        return 'Low'
    elif 0.4 < volatile_acidity <= 0.7:
        return 'Medium'
    else:
        return 'High'
    
"""
Ácido Cítrico (Citric Acid): Aporta frescura y complejidad. 
Su presencia puede mejorar la acidez y el equilibrio del vino, aunque generalmente se encuentra 
en niveles bajos en los vinos.

Rango Bajo: < 0.1 g/L
Rango Medio: 0.1 - 0.3 g/L
Rango Alto: > 0.3 g/L
"""

def classify_citric_acidity(citric_acidity):
    if citric_acidity <= 0.1:
        return 'Low'
    elif 0.1 < citric_acidity <= 0.3:
        return 'Medium'
    else:
        return 'High'
    
"""
Azúcar Residual (Residual Sugar): Contribuye a la dulzura del vino. 
Los vinos con alto azúcar residual pueden ser percibidos como dulces,
mientras que los niveles bajos pueden hacerlos secos.

Rango Bajo: < 1.0 g/L
Rango Medio: 1.0 - 10.0 g/L
Rango Alto: > 10.0 g/L
"""

def classify_residual_sugar(residual_sugar):
    if residual_sugar <= 1.0:
        return 'Low'
    elif 1.0 < residual_sugar <= 10.0:
        return 'Medium'
    else:
        return 'High'

    
"""
Cloruros (Chlorides): Altos niveles de cloruros pueden dar un matiz salado al vino. 
Normalmente, los cloruros se encuentran en niveles bajos.

Rango Bajo: < 0.02 g/L
Rango Medio: 0.02 - 0.08 g/L
Rango Alto: > 0.08 g/L
    
"""
def classify_chlorides(chlorides):
    if chlorides <= 0.02:
        return 'Low'
    elif 0.02 < chlorides <= 0.08:
        return 'Medium'
    else:
        return 'High'

"""
Dióxido de Azufre Libre (Free Sulfur Dioxide): Ayuda a prevenir la oxidación y el crecimiento 
microbiano. Niveles más altos pueden proteger el vino, pero si son excesivos pueden impartir 
aromas de azufre.

Rango Bajo: < 10 mg/L
Rango Medio: 10 - 40 mg/L
Rango Alto: > 40 mg/L
"""
def classify_free_sulfur_diox(free_sulfur_dioxide):
    if free_sulfur_dioxide <= 10:
        return 'Low'
    elif 10 < free_sulfur_dioxide <= 40:
        return 'Medium'
    else:
        return 'High'

"""
Dióxido de Azufre Total (Total Sulfur Dioxide): Incluye tanto el dióxido de azufre libre como el 
combinado. Niveles altos pueden impactar el aroma y sabor, aunque es esencial para la conservación 
del vino.

Rango Bajo: < 30 mg/L
Rango Medio: 30 - 100 mg/L
Rango Alto: > 100 mg/L
"""
def classify_tot_sulfur_diox(tot_sulfur_dioxide):
    if tot_sulfur_dioxide <= 30:
        return 'Low'
    elif 30< tot_sulfur_dioxide <= 100:
        return 'Medium'
    else:
        return 'High'
    
"""
Densidad (Density): Indica la cantidad de sólidos disueltos en el vino, como azúcares y alcohol.
 La densidad puede dar pistas sobre el contenido de azúcar residual y el alcohol.

Rango Bajo: < 0.990 g/mL
Rango Medio: 0.990 - 1.010 g/mL
Rango Alto: > 1.010 g/mL
"""
def classify_density(density):
    if density <= 0.990:
        return 'Low'
    elif 0.990< density <= 1.010:
        return 'Medium'
    else:
        return 'High'
    
"""    
pH: Influye en la percepción de la acidez y la estabilidad del vino. Un pH bajo indica mayor acidez,
mientras que un pH alto puede dar una sensación más suave.
Rango Bajo: < 3.2
Rango Medio: 3.2 - 3.6
Rango Alto: > 3.6
"""
def classify_ph(ph):
    if ph <= 3.2:
        return 'Low'
    elif 3.2< ph <= 3.6:
        return 'Medium'
    else:
        return 'High'
    
"""  
Sulfatos (Sulphates): Aportan un carácter seco y pueden influir en la percepción del vino. 
En general, niveles más altos pueden dar una sensación más estructurada.

Rango Bajo: < 0.2 g/L
Rango Medio: 0.2 - 0.6 g/L
Rango Alto: > 0.6 g/L
"""  

def classify_sulphates(sulphates):
    if sulphates <= 0.2:
        return 'Low'
    elif 0.2< sulphates <= 0.6:
        return 'Medium'
    else:
        return 'High'
    
"""
Alcohol: Contribuye al cuerpo del vino y puede influir en la percepción de dulzura y calor.
 Los niveles más altos suelen indicar un vino más robusto y potente.

Rango Bajo: < 8%
Rango Medio: 8% - 13%
Rango Alto: > 13%
"""

def classify_alcohol(alcohol):
    if alcohol <= 8:
        return 'Low'
    elif 8< alcohol <= 13:
        return 'Medium'
    else:
        return 'High'
    
    
# READ WINES AND CLASFIFY VALUES IN (LOW, MEDIUM AND HIGH VALUES)
import os
import pandas as pd

path = "C:/Users/jonma/OneDrive/Escritorio/case_base_reasoning/winequality_data_set"
df_red = pd.read_csv(os.path.join(path,"winequality-red.csv"),sep=";")

df_red.columns

# marcar rangos
df_red["Fix_acidity_range"] = df_red['fixed acidity'].apply(classify_fixed_acidity)
df_red["Volatile_acidity_range"] = df_red['volatile acidity'].apply(classify_volatile_acidity)
df_red["Citric_acidity_range"] = df_red['citric acid'].apply(classify_citric_acidity)
df_red["Residual_sugar_range"] = df_red['residual sugar'].apply(classify_residual_sugar)
df_red["Chlorides_range"] = df_red['chlorides'].apply(classify_chlorides)
df_red["Free_sulfur_diox_range"] = df_red['free sulfur dioxide'].apply(classify_free_sulfur_diox)
df_red["Total_sulfur_diox_range"] = df_red['total sulfur dioxide'].apply(classify_tot_sulfur_diox)
df_red["Density_range"] = df_red['density'].apply(classify_density)
df_red["Ph_range"] = df_red['pH'].apply(classify_ph)
df_red["Sulphates_range"] = df_red['sulphates'].apply(classify_sulphates)
df_red["Alcohol_range"] = df_red['alcohol'].apply(classify_alcohol)

# validar rangos
df_red.Fix_acidity_range.value_counts()
df_red.Volatile_acidity_range.value_counts()
df_red.Citric_acidity_range.value_counts()
df_red.Residual_sugar_range.value_counts()
df_red.Chlorides_range.value_counts()
df_red.Free_sulfur_diox_range.value_counts()
df_red.Total_sulfur_diox_range.value_counts()
df_red.Density_range.value_counts()
df_red.Ph_range.value_counts()
df_red.Sulphates_range.value_counts()
df_red.Alcohol_range.value_counts()


# WHITE WINES AND CLASFIFY VALUES IN (LOW, MEDIUM AND HIGH VALUES)
import os
import pandas as pd

path = "C:/Users/jonma/OneDrive/Escritorio/case_base_reasoning/winequality_data_set"
df_white = pd.read_csv(os.path.join(path,"winequality-white.csv"),sep=";")

df_white["Fix_acidity_range"] = df_white['fixed acidity'].apply(classify_fixed_acidity)
df_white["Volatile_acidity_range"] = df_white['volatile acidity'].apply(classify_volatile_acidity)
df_white["Citric_acidity_range"] = df_white['citric acid'].apply(classify_citric_acidity)
df_white["Residual_sugar_range"] = df_white['residual sugar'].apply(classify_residual_sugar)
df_white["Chlorides_range"] = df_white['chlorides'].apply(classify_chlorides)
df_white["Free_sulfur_diox_range"] = df_white['free sulfur dioxide'].apply(classify_free_sulfur_diox)
df_white["Total_sulfur_diox_range"] = df_white['total sulfur dioxide'].apply(classify_tot_sulfur_diox)
df_white["Density_range"] = df_white['density'].apply(classify_density)
df_white["Ph_range"] = df_white['pH'].apply(classify_ph)
df_white["Sulphates_range"] = df_white['sulphates'].apply(classify_sulphates)
df_white["Alcohol_range"] = df_white['alcohol'].apply(classify_alcohol)

# validar rangos
df_white.Fix_acidity_range.value_counts()
df_white.Volatile_acidity_range.value_counts()
df_white.Citric_acidity_range.value_counts()
df_white.Residual_sugar_range.value_counts()
df_white.Chlorides_range.value_counts()
df_white.Free_sulfur_diox_range.value_counts()
df_white.Total_sulfur_diox_range.value_counts()
df_white.Density_range.value_counts()
df_white.Ph_range.value_counts()
df_white.Sulphates_range.value_counts()
df_white.Alcohol_range.value_counts()