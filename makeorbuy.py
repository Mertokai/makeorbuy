from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpBinary, value

from pulp import *

# Bileşenler (Malzeme listesinden)
components = [
    "Yan Korkuluklar",
    "Başlık Paneli", 
    "Ayak Paneli",
    "Alt Destek Platformu",
    "Yatak",
    "Yastık",
    "Yan Koruma Minderi",
    "Tekerlek (Frenli)",
    "Alt Ayaklar",
    "Köşe Koruyucular",
    "Vida (4x40 mm)",
    "Vida (4x60 mm)",
    "Cibinlik (Tüll Kumaş)",
    "Cibinlik Askı Direği",
    "Kurulum Kılavuzu"
]

# Mevcut Durum (Malzeme listesinden)
current_decision = {
    "Yan Korkuluklar": "Üretim",
    "Başlık Paneli": "Üretim", 
    "Ayak Paneli": "Üretim",
    "Alt Destek Platformu": "Üretim",
    "Yatak": "Satın Alma",
    "Yastık": "Satın Alma",
    "Yan Koruma Minderi": "Satın Alma",
    "Tekerlek (Frenli)": "Satın Alma",
    "Alt Ayaklar": "Üretim",
    "Köşe Koruyucular": "Satın Alma",
    "Vida (4x40 mm)": "Satın Alma",
    "Vida (4x60 mm)": "Satın Alma",
    "Cibinlik (Tüll Kumaş)": "Satın Alma",
    "Cibinlik Askı Direği": "Üretim",
    "Kurulum Kılavuzu": "Üretim"
}

# Parametreler
make_cost = {
    "Yan Korkuluklar": 380, 
    "Başlık Paneli": 260,  
    "Ayak Paneli": 260, 
    "Alt Destek Platformu": 220, 
    "Yatak": 600, 
    "Yastık": 150, 
    "Yan Koruma Minderi": 250, 
    "Tekerlek (Frenli)": 320, 
    "Alt Ayaklar": 190, 
    "Köşe Koruyucular": 120, 
    "Vida (4x40 mm)": 90, 
    "Vida (4x60 mm)": 105, 
    "Cibinlik (Tüll Kumaş)": 180, 
    "Cibinlik Askı Direği": 140, 
    "Kurulum Kılavuzu": 60 
}

buy_cost = {
    "Yan Korkuluklar": 550, 
    "Başlık Paneli": 330,  
    "Ayak Paneli": 330, 
    "Alt Destek Platformu": 290, 
    "Yatak": 450, 
    "Yastık": 120, 
    "Yan Koruma Minderi": 200, 
    "Tekerlek (Frenli)": 250, 
    "Alt Ayaklar": 280, 
    "Köşe Koruyucular": 90, 
    "Vida (4x40 mm)": 60, 
    "Vida (4x60 mm)": 75, 
    "Cibinlik (Tüll Kumaş)": 150, 
    "Cibinlik Askı Direği": 210, 
    "Kurulum Kılavuzu": 90 
}

maintenance_cost = {
    "Yan Korkuluklar": 15,
    "Başlık Paneli": 10, 
    "Ayak Paneli": 10,
    "Alt Destek Platformu": 8,
    "Yatak": 20,
    "Yastık": 5,
    "Yan Koruma Minderi": 10,
    "Tekerlek (Frenli)": 12,
    "Alt Ayaklar": 7,
    "Köşe Koruyucular": 5,
    "Vida (4x40 mm)": 2,
    "Vida (4x60 mm)": 2,
    "Cibinlik (Tüll Kumaş)": 10,
    "Cibinlik Askı Direği": 5,
    "Kurulum Kılavuzu": 0
}

lifespan = {
    "Yan Korkuluklar": 5,
    "Başlık Paneli": 5, 
    "Ayak Paneli": 5,
    "Alt Destek Platformu": 4,
    "Yatak": 3,
    "Yastık": 2,
    "Yan Koruma Minderi": 3,
    "Tekerlek (Frenli)": 4,
    "Alt Ayaklar": 5,
    "Köşe Koruyucular": 3,
    "Vida (4x40 mm)": 5,
    "Vida (4x60 mm)": 5,
    "Cibinlik (Tüll Kumaş)": 2,
    "Cibinlik Askı Direği": 4,
    "Kurulum Kılavuzu": 5
}

renewal_cost = {
    "Yan Korkuluklar": 90,
    "Başlık Paneli": 60, 
    "Ayak Paneli": 60,
    "Alt Destek Platformu": 50,
    "Yatak": 150,
    "Yastık": 40,
    "Yan Koruma Minderi": 65,
    "Tekerlek (Frenli)": 70,
    "Alt Ayaklar": 45,
    "Köşe Koruyucular": 25,
    "Vida (4x40 mm)": 20,
    "Vida (4x60 mm)": 23,
    "Cibinlik (Tüll Kumaş)": 45,
    "Cibinlik Askı Direği": 35,
    "Kurulum Kılavuzu": 15
}

failure_rate = {
    "Yan Korkuluklar": 0.05,
    "Başlık Paneli": 0.05, 
    "Ayak Paneli": 0.05,
    "Alt Destek Platformu": 0.08,
    "Yatak": 0.12,
    "Yastık": 0.15,
    "Yan Koruma Minderi": 0.10,
    "Tekerlek (Frenli)": 0.10,
    "Alt Ayaklar": 0.06,
    "Köşe Koruyucular": 0.10,
    "Vida (4x40 mm)": 0.02,
    "Vida (4x60 mm)": 0.02,
    "Cibinlik (Tüll Kumaş)": 0.15,
    "Cibinlik Askı Direği": 0.07,
    "Kurulum Kılavuzu": 0.05
}

# Karar değişkenleri (1: Üretim, 0: Satın Alma)
x = {c: LpVariable(f"x_{c}", cat=LpBinary) for c in components}

# Model
model = LpProblem("Bebek_Besigi_Make_or_Buy", LpMinimize)

# Amaç fonksiyonu: Toplam yaşam döngüsü maliyetini minimize et
model += lpSum([
    x[c] * (make_cost[c] + maintenance_cost[c] * lifespan[c] + renewal_cost[c] * failure_rate[c]) +
    (1 - x[c]) * buy_cost[c]
    for c in components
])

# Bütçe kısıtlaması (Opsiyonel - varsayılan olarak 1500 TL)
total_budget = 1500
model += lpSum([
    x[c] * make_cost[c] + (1 - x[c]) * buy_cost[c]
    for c in components
]) <= total_budget, "BütçeKısıtlaması"

# Modeli çöz
model.solve()

# Sonuçları yazdır
print("BEBEK BEŞİĞİ - MAKE OR BUY ANALİZİ")
print("=" * 60)
print(f"{'Parça':<25} {'Karar':<15} {'Mevcut Durum':<15} {'Uyumluluk':<15}")
print("-" * 60)

total_current_cost = 0
total_optimal_cost = 0
total_lifecycle_current = 0
total_lifecycle_optimal = 0

for c in components:
    decision = "Produce" if x[c].value() == 1 else "Buy"
    match = "✓" if (decision == "Produce" and current_decision[c] == "Produce") or \
                   (decision == "Buy" and current_decision[c] == "Buy") else "✗"
    
    print(f"{c:<25} {decision:<15} {current_decision[c]:<15} {match:<15}")
    
    if current_decision[c] == "Produce":
        current_cost = make_cost[c]
        lifecycle_current = make_cost[c] + maintenance_cost[c] * lifespan[c] + renewal_cost[c] * failure_rate[c]
    else:
        current_cost = buy_cost[c]
        lifecycle_current = buy_cost[c]
    
    if decision == "Produce":
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
print(f"Toplam Başlangıç Maliyeti (Mevcut): {total_current_cost} TL")
print(f"Toplam Başlangıç Maliyeti (Optimal): {total_optimal_cost} TL")
print(f"Toplam Yaşam Döngüsü Maliyeti (Mevcut): {total_lifecycle_current} TL")
print(f"Toplam Yaşam Döngüsü Maliyeti (Optimal): {total_lifecycle_optimal} TL")
print(f"Potansiyel Tasarruf (Yaşam Döngüsü): {total_lifecycle_current - total_lifecycle_optimal} TL")
print("=" * 60)

# Duyarlılık Analizi - Kritik parçaları belirle
print("\nKRİTİK PARÇALAR ANALİZİ")
print("=" * 60)
print(f"{'Parça':<25} {'Üretim/Satın Alma Farkı':<25} {'Öneri':<20}")
print("-" * 60)

for c in components:
    manufacture_cost = make_cost[c] + maintenance_cost[c] * lifespan[c] + renewal_cost[c] * failure_rate[c]
    purchase_cost = buy_cost[c]
    difference = manufacture_cost - purchase_cost
    
    if abs(difference) > 50:  # Önemli maliyet farkı
        if difference > 0:
            recommendation = "Satın Alma Tercih Edilmeli"
        else:
            recommendation = "Üretim Tercih Edilmeli"
        print(f"{c:<25} {difference:<25.2f} {recommendation:<20}")

print("=" * 60)

# BEBEK BEŞİĞİ - MAKE OR BUY ANALİZİ
# ============================================================
# Parça                     Karar          
# ------------------------------------------------------------
# Yan Korkuluklar           Make (Üret)    
# Başlık Paneli             Make (Üret)    
# Ayak Paneli               Make (Üret)    
# Alt Destek Platformu      Make (Üret)    
# Yatak                     Buy (Satın Al) 
# Yastık                    Buy (Satın Al) 
# Yan Koruma Minderi        Buy (Satın Al) 
# Tekerlek (Frenli)         Buy (Satın Al) 
# Alt Ayaklar               Make (Üret)    
# Köşe Koruyucular          Buy (Satın Al) 
# Vida (4x40 mm)            Buy (Satın Al) 
# Vida (4x60 mm)            Buy (Satın Al) 
# Cibinlik (Tüll Kumaş)     Buy (Satın Al) 
# Cibinlik Askı Direği      Make (Üret)    
# Kurulum Kılavuzu          Make (Üret)    
# ------------------------------------------------------------
# Toplam Başlangıç Maliyeti: 2905.0 TL
# Toplam Yaşam Döngüsü Maliyeti: 3187.3999999999996 TL
# ============================================================