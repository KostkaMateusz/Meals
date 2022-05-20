def make_meal_propositions(meals):
    # minimal carbon porposition
    min_carbon=min(meals,key=lambda x:x.carbs)
    # max protein porposition
    max_proteins=max(meals,key=lambda x:x.proteins)   

    return {'min_carbon':min_carbon.name,'max_proteins':max_proteins.name}