from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpBinary, value

from pulp import *

# List of components
components = [
    "Side Rails",
    "Headboard Panel", 
    "Footboard Panel",
    "Bottom Support Platform",
    "Mattress",
    "Pillow",
    "Side Protection Cushion",
    "Wheel (With Brake)",
    "Bottom Feet",
    "Corner Protectors",
    "Screw (4x40 mm)",
    "Screw (4x60 mm)",
    "Canopy (Tulle Fabric)",
    "Canopy Support Rod",
    "Assembly Manual"
]

# Current decision (Make or Buy)
current_decision = {
    "Side Rails": "Make",
    "Headboard Panel": "Make", 
    "Footboard Panel": "Make",
    "Bottom Support Platform": "Make",
    "Mattress": "Buy",
    "Pillow": "Buy",
    "Side Protection Cushion": "Buy",
    "Wheel (With Brake)": "Buy",
    "Bottom Feet": "Make",
    "Corner Protectors": "Buy",
    "Screw (4x40 mm)": "Buy",
    "Screw (4x60 mm)": "Buy",
    "Canopy (Tulle Fabric)": "Buy",
    "Canopy Support Rod": "Make",
    "Assembly Manual": "Make"
}

# Cost of making each component
make_cost = {
    "Side Rails": 380, 
    "Headboard Panel": 260,  
    "Footboard Panel": 260, 
    "Bottom Support Platform": 220, 
    "Mattress": 600, 
    "Pillow": 150, 
    "Side Protection Cushion": 250, 
    "Wheel (With Brake)": 320, 
    "Bottom Feet": 190, 
    "Corner Protectors": 120, 
    "Screw (4x40 mm)": 90, 
    "Screw (4x60 mm)": 105, 
    "Canopy (Tulle Fabric)": 180, 
    "Canopy Support Rod": 140, 
    "Assembly Manual": 60 
}

# Cost of buying each component
buy_cost = {
    "Side Rails": 550, 
    "Headboard Panel": 330,  
    "Footboard Panel": 330, 
    "Bottom Support Platform": 290, 
    "Mattress": 450, 
    "Pillow": 120, 
    "Side Protection Cushion": 200, 
    "Wheel (With Brake)": 250, 
    "Bottom Feet": 280, 
    "Corner Protectors": 90, 
    "Screw (4x40 mm)": 60, 
    "Screw (4x60 mm)": 75, 
    "Canopy (Tulle Fabric)": 150, 
    "Canopy Support Rod": 210, 
    "Assembly Manual": 90 
}

# Maintenance cost per year
maintenance_cost = {
    "Side Rails": 15,
    "Headboard Panel": 10, 
    "Footboard Panel": 10,
    "Bottom Support Platform": 8,
    "Mattress": 20,
    "Pillow": 5,
    "Side Protection Cushion": 10,
    "Wheel (With Brake)": 12,
    "Bottom Feet": 7,
    "Corner Protectors": 5,
    "Screw (4x40 mm)": 2,
    "Screw (4x60 mm)": 2,
    "Canopy (Tulle Fabric)": 10,
    "Canopy Support Rod": 5,
    "Assembly Manual": 0
}

# Lifespan of each component in years
lifespan = {
    "Side Rails": 5,
    "Headboard Panel": 5, 
    "Footboard Panel": 5,
    "Bottom Support Platform": 4,
    "Mattress": 3,
    "Pillow": 2,
    "Side Protection Cushion": 3,
    "Wheel (With Brake)": 4,
    "Bottom Feet": 5,
    "Corner Protectors": 3,
    "Screw (4x40 mm)": 5,
    "Screw (4x60 mm)": 5,
    "Canopy (Tulle Fabric)": 2,
    "Canopy Support Rod": 4,
    "Assembly Manual": 5
}

# Renewal cost for each component
renewal_cost = {
    "Side Rails": 90,
    "Headboard Panel": 60, 
    "Footboard Panel": 60,
    "Bottom Support Platform": 50,
    "Mattress": 150,
    "Pillow": 40,
    "Side Protection Cushion": 65,
    "Wheel (With Brake)": 70,
    "Bottom Feet": 45,
    "Corner Protectors": 25,
    "Screw (4x40 mm)": 20,
    "Screw (4x60 mm)": 23,
    "Canopy (Tulle Fabric)": 45,
    "Canopy Support Rod": 35,
    "Assembly Manual": 15
}

# Failure rate for each component
failure_rate = {
    "Side Rails": 0.05,
    "Headboard Panel": 0.05, 
    "Footboard Panel": 0.05,
    "Bottom Support Platform": 0.08,
    "Mattress": 0.12,
    "Pillow": 0.15,
    "Side Protection Cushion": 0.10,
    "Wheel (With Brake)": 0.10,
    "Bottom Feet": 0.06,
    "Corner Protectors": 0.10,
    "Screw (4x40 mm)": 0.02,
    "Screw (4x60 mm)": 0.02,
    "Canopy (Tulle Fabric)": 0.15,
    "Canopy Support Rod": 0.07,
    "Assembly Manual": 0.05
}

# Decision variables (1: Make, 0: Buy)
x = {c: LpVariable(f"x_{c}", cat=LpBinary) for c in components}

# Model
model = LpProblem("Baby_Crib_Make_or_Buy", LpMinimize)

# Objective function: Minimize total lifecycle cost
model += lpSum([
    x[c] * (make_cost[c] + maintenance_cost[c] * lifespan[c] + renewal_cost[c] * failure_rate[c]) +
    (1 - x[c]) * buy_cost[c]
    for c in components
])

# Budget constraint
total_budget = 1500
model += lpSum([
    x[c] * make_cost[c] + (1 - x[c]) * buy_cost[c]
    for c in components
]) <= total_budget, "BudgetConstraint"

model.solve()

print("BABY CRIB - MAKE OR BUY ANALYSIS")
print("=" * 60)
print(f"{'Component':<25} {'Decision':<15} {'Current Decision':<15} {'Match':<15}")
print("-" * 60)

total_current_cost = 0
total_optimal_cost = 0
total_lifecycle_current = 0
total_lifecycle_optimal = 0

for c in components:
    decision = "Make" if x[c].value() == 1 else "Buy"
    match = "✓" if (decision == "Make" and current_decision[c] == "Make") or \
                   (decision == "Buy" and current_decision[c] == "Buy") else "✗"
    
    print(f"{c:<25} {decision:<15} {current_decision[c]:<15} {match:<15}")
    
    if current_decision[c] == "Make":
        current_cost = make_cost[c]
        lifecycle_current = make_cost[c] + maintenance_cost[c] * lifespan[c] + renewal_cost[c] * failure_rate[c]
    else:
        current_cost = buy_cost[c]
        lifecycle_current = buy_cost[c]
    
    if decision == "Make":
        optimal_cost = make_cost[c]
        lifecycle_optimal = make_cost[c] + maintenance_cost[c] * lifespan[c] + renewal_cost[c] * failure_rate[c]
    else:
        optimal_cost = buy_cost[c]
        lifecycle_optimal = buy_cost[c]
    
    total_current_cost += current_cost
    total_optimal_cost += optimal_cost
    total_lifecycle_current += lifecycle_current
    total_lifecycle_optimal += lifecycle_optimal

print("-" * 60)
print(f"Total Initial Cost (Current): {total_current_cost} TL")
print(f"Total Initial Cost (Optimal): {total_optimal_cost} TL")
print(f"Total Lifecycle Cost (Current): {total_lifecycle_current} TL")
print(f"Total Lifecycle Cost (Optimal): {total_lifecycle_optimal} TL")
print(f"Potential Savings (Lifecycle): {total_lifecycle_current - total_lifecycle_optimal} TL")
print("=" * 60)

print("\nCRITICAL COMPONENTS ANALYSIS")
print("=" * 60)
print(f"{'Component':<25} {'Make/Buy Difference':<25} {'Recommendation':<20}")
print("-" * 60)

for c in components:
    manufacture_cost = make_cost[c] + maintenance_cost[c] * lifespan[c] + renewal_cost[c] * failure_rate[c]
    purchase_cost = buy_cost[c]
    difference = manufacture_cost - purchase_cost
    
    if abs(difference) > 50:  
        if difference > 0:
            recommendation = "Prefer Buying"
        else:
            recommendation = "Prefer Making"
        print(f"{c:<25} {difference:<25.2f} {recommendation:<20}")

print("=" * 60)
