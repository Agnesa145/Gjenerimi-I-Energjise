import pandas as pd
import matplotlib.pyplot as plt
import os

# Krijo folderin 'plots' nëse nuk ekziston
os.makedirs('plots', exist_ok=True)

# Leximi i të dhënave
df = pd.read_csv("data/gjenerimi_energjise_europe.csv")

# Konvertimi i kolonave kryesore
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["electricity_generation"] = pd.to_numeric(df["electricity_generation"], errors="coerce")
df["biofuel_share_energy"] = pd.to_numeric(df["biofuel_share_energy"], errors="coerce")
df = df.sort_values("year")

# Eksporto DataFrame në CSV për Power BI
df.to_csv("gjenerimi_energjise_europe_export.csv", index=False)

# Llogaritja e rritjes vjetore
df["growth_pct"] = df["electricity_generation"].pct_change() * 100
df["ngjyra"] = df["growth_pct"].apply(lambda x: "black" if x < 0 else "skyblue")

# === GRAFIKU 1: Linjë me 2 akse ===
fig, ax1 = plt.subplots(figsize=(12,6))

ax1.set_xlabel("Viti")
ax1.set_ylabel("Gjenerimi i Energjisë (TWh)", color='skyblue')
ax1.plot(df["year"], df["electricity_generation"], color='lightblue', marker='o', label="Gjenerimi")
ax1.tick_params(axis='y', labelcolor='blue')

ax2 = ax1.twinx()
ax2.set_ylabel("Rritja Vjetore (%)", color='black')
ax2.plot(df["year"], df["growth_pct"], color='red', marker='x', linestyle='--', label="Rritja (%)")
ax2.axhline(df["growth_pct"].mean(), color="green", linestyle="--", label="Mesatarja")
ax2.tick_params(axis='y', labelcolor='red')

plt.title("Gjenerimi Total dhe Rritja Vjetore e Energjisë në Evropë")
plt.grid(True)
plt.tight_layout()
plt.savefig('plots/grafiku1.png')
plt.close()

# === GRAFIKU 2: Bar chart me ngjyra sipas rritjes ===
plt.figure(figsize=(10,5))
plt.bar(df["year"], df["growth_pct"], color=df["ngjyra"])
plt.axhline(df["growth_pct"].mean(), color="black", linestyle="--", label="Mesatarja")
plt.title("Rritja Vjetore në Gjenerimin e Energjisë (Ngjyrosje)")
plt.xlabel("Viti")
plt.ylabel("Rritja (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('plots/grafiku2.png')
plt.close()

# === GRAFIKU 3: Pie chart për biofuel (vetëm nëse ka të dhëna) ===
if df["biofuel_share_energy"].notna().any():
    latest = df.dropna(subset=["biofuel_share_energy"]).iloc[-1]
    sizes = [latest["biofuel_share_energy"], 100 - latest["biofuel_share_energy"]]
    labels = ["Biofuel", "Tjera"]

    plt.figure(figsize=(6,6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=["blue", "orange"])
    plt.title(f"Pjesëmarrja e Biofuel në Energji ({int(latest['year'])})")
    plt.tight_layout()
    plt.savefig('plots/grafiku3.png')
    plt.close()

# === GRAFIKU 4: Bar chart për mesataren çdo 5 vite ===
df["grupi_viteve"] = (df["year"] // 5) * 5
bar_data = df.groupby("grupi_viteve")["growth_pct"].mean().dropna()

plt.figure(figsize=(10,5))
plt.bar(bar_data.index.astype(str), bar_data.values, color="pink")
plt.title("Rritja Mesatare e Energjisë për Çdo 5 Vite")
plt.xlabel("Periudha (5-vjeçare)")
plt.ylabel("Rritja mesatare (%)")
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('plots/grafiku4.png')
plt.close()

# === GRAFIKU 5: Histogram për shpërndarjen e rritjes ===
plt.figure(figsize=(8,4))
plt.hist(df["growth_pct"].dropna(), bins=10, color="coral", edgecolor="black")
plt.title("Shpërndarja e Rritjes Vjetore në Evropë")
plt.xlabel("Rritja (%)")
plt.ylabel("Frekuenca")
plt.grid(True)
plt.tight_layout()
plt.savefig('plots/grafiku5.png')
plt.close()
