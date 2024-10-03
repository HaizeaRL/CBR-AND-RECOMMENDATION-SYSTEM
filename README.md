# CBR-AND-RECOMMENDATION-SYSTEM

# Executatzeko kategorizazio sorrera
docker build -t wine_app .
docker run -it wine_app   
cd src
python wine_profilling.py

# Profile bisualizazioa ikustea TODO

# Profile definizioa sartzea readmen: TODO
'''
WINE DESCRIPTORS:
    1- VIBRANCY (defined by acidity) 
        - fixed acidity => A higher fixed acidity value suggests a fresher or more acidic wine.
        - volatile acidity => if it is too high, it may indicate a vinegary taste.
        - citric acid => Wines with more citric acid tend to be perceived as fresher or livelier.
        - PH => A low pH (acidic) is usually associated with greater freshness and stability, while a high pH may suggest a 
        softer or less fresh wine.
        Low: Liveliness
        Medium: Live
        High: Brilliant 
        
    2- SWEETNESS (defined by sugars)
        - residual sugar => A high value implies a sweet wine, while a low value suggests a dry wine.
        Low: Dry
        Medium: Semi-Dry
        High: Sweet
        
    3- BODY (defined by alcohol & density)
        - alcohol => The higher the alcohol content, the more robust and full-bodied
        - density => A denser wine suggests more body and richness in the mouth.
        Low: Light
        Medium: Medium
        High: Full-Bodied
        
    4- NUANCE (defined by chlorides)
       - chlorides: salinity traces in the wine, which can influence a mineral sensation in the taste.
       Low: Simple
       Medium: Complex, Spicy
       High: Intense
     
    5- TANNICITY (defined by sulphates)
       - shulpathes: Higher levels may contribute to a greater sensation of dryness on the palate.
        Low: Soft
        Medium: Balanced, Structured
        High: Robust
       
'''