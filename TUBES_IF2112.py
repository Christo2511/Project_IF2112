"""
FINAL PROJECT IF2112
Christopher WH / 12220076
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image

#DATASET
import json
import csv

with open("kode_negara_lengkap.json") as c:
    code = json.load(c)

handle = open("produksi_minyak_mentah.csv")
csv = csv.reader(handle)
header = next(csv)
data = []
for row in csv:
    data.append(row)

#VALID COUNTRY TRANSLATIONS
country_code_raw = []
country_code = []
country_name = []
year_list = []
for set in data:
    country_code_raw.append(set[0])
for c in country_code_raw:
    if c not in country_code:
        country_code.append(c)
        
for c in country_code:
    for group in code:
        if group["alpha-3"]==c:
            country_name.append(group["name"])
            
for set in data:
    if set[1] not in year_list:
        year_list.append(set[1])           
 

##title##
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
image2 = Image.open('AXIOM_banner3.png')
st.image(image2)

st.title("International Oil Production Database")
st.markdown("Data from Certified Sources")
###title###

##sidebar##
image = Image.open('AXIOM_banner2.png')
st.sidebar.image(image)

st.sidebar.title("Input Menu")
#left_col, right_col = st.columns(2) #MOVE LATER

## User inputs on the control panel
st.sidebar.subheader("Pengaturan konfigurasi tampilan")
negara = st.sidebar.selectbox("Pilih negara", country_name)
tahun = st.sidebar.selectbox("Pilih tahun", year_list)

n_peringkat = st.sidebar.number_input("Jumlah peringkat produksi terbesar", min_value=1, max_value=None, value=5)
###sidebar###

##1A##
for set in data:
    for group in code:
        if set[0]==group["alpha-3"]:
            set.insert(0,group["name"])

A_graphy = []
A_graphx = []
for set in data:
    if set[0]==negara:
        A_graphy.append(float(set[3]))
        A_graphx.append(set[2])
        
y_A = A_graphy
x_A = A_graphx

st.header(" Line Plot Produksi Minyak Mentah "+negara)
st.caption("Line plot yang memproyeksikan produksi minyak mentah negara pilihan dari tahun 1971 sampai tahun 2015 dengan sumbu-x menyatakan tahun produksi dan sumbu-y menyatakan besar produksi")

fig, ax = plt.subplots()
ax.plot(A_graphx, A_graphy, color='green')
ax.grid()
fig.set_figwidth(36)
fig.set_figheight(9)
ax.set_xticklabels(A_graphx, rotation=0, fontsize=14)
ax.set_xlabel("Tahun", fontsize=30)
ax.set_ylabel("Produksi minyak mentah", fontsize=25)
st.pyplot(fig)

A_table = dict()
A_table["Tahun"] = A_graphx
A_table["Produksi"] = A_graphy
A_table = pd.DataFrame(A_table)
A_code = ""
for group in code:
    if group["name"]==negara:
        A_code = group["alpha-3"]

with st.expander("Lihat Data line Plot"):
    st.subheader(" Tabel Data Produksi Minyak Mentah "+negara)
    st.write("Kode negara: "+A_code)
    st.table(A_table)

image3 = Image.open('AXIOM_banner1.png')
st.image(image3)
left_col, right_col = st.columns(2) #MOVE LATER
###1A###

##1B##
B_raw = []
B_graphx = []
B_graphy = []
for set in data:
    if float(set[2])==float(tahun):
        B_raw.append((float(set[3]),set[0]))
B_raw.sort(reverse=True)
for num in range(n_peringkat):
    B_graphy.append(B_raw[num][0])
    B_graphx.append(B_raw[num][1])

cmap_name = 'tab20'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:n_peringkat]
left_col.header(" Bar Plot "+str(n_peringkat)+" Negara dengan Produksi Terbesar Tahun "+str(tahun))
left_col.caption("Bar plot yang memproyeksikan negara dengan produksi minyak mentah terbesar")
fig, ax = plt.subplots()
ax.barh(B_graphx, B_graphy, color=colors)
ax.set_yticklabels(B_graphx, rotation=0)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel("Produksi Minyak Mentah", fontsize=12)
left_col.pyplot(fig)

B_table = dict()
B_table["Negara"] = B_graphx
B_code = []
for name in B_table["Negara"]:
    for group in code:
        if name==group["name"]:
            B_code.append(group["alpha-3"])
B_table["Kode Negara"] = B_code
B_table["Produksi"] = B_graphy
B_table = pd.DataFrame(B_table)

with left_col.expander("Lihat Data Bar Plot Tahun "+tahun):
    st.subheader(" Tabel Data "+str(n_peringkat)+" Negara dengan Produksi Terbesar Tahun "+str(tahun))
    st.table(B_table)
###1B###

##1C##
C_dict = dict()
C_raw = []
C_graphx = []
C_graphy = []

for name in country_name:
    sum_prod=0
    for set in data:
        if set[0]==name:
            sum_prod = sum_prod+float(set[3])
            C_dict[name] = sum_prod

for name,prod in C_dict.items():
    tup = prod,name
    C_raw.append(tup)
C_raw.sort(reverse=True)

for num in range(n_peringkat):
    C_graphx.append(C_raw[num][1])
    C_graphy.append(C_raw[num][0])

cmap_name = 'tab20'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:n_peringkat]
right_col.header(" Bar Plot "+str(n_peringkat)+" Negara dengan Produksi Terbesar Kumulatif")
right_col.caption("Bar plot negara dengan produksi minyak mentah terbesar dari tahun 1971-2015")
fig, ax = plt.subplots()
ax.barh(C_graphx, C_graphy, color=colors)
ax.set_yticklabels(C_graphx, rotation=0)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel("Produksi Minyak Mentah", fontsize=12)
right_col.pyplot(fig)

C_table = dict()
C_table["Negara"] = C_graphx
C_code = []
for name in C_table["Negara"]:
    for group in code:
        if name==group["name"]:
            C_code.append(group["alpha-3"])
C_table["Kode Negara"] = C_code
C_table["Produksi"] = C_graphy
C_table = pd.DataFrame(C_table)

with right_col.expander("Lihat Data Bar Plot Kumulatif"):
    st.subheader(" Tabel Data "+str(n_peringkat)+" Negara dengan Produksi Terbesar Kumulatif")
    st.table(C_table)
###1C###

##1D##
D_dict1 = dict()
D_raw1 = []
for set in data:
    if float(set[2])==float(tahun):
        D_raw1.append((float(set[3]),set[0]))
D_raw1.sort()

D_dict1["Deskripsi"] = ["Produksi terbesar","Produksi terkecil"]
D_dict1["Negara"] = [B_raw[0][1],D_raw1[0][1]]
for group in code:
    if group["name"]==B_raw[0][1]:
        code1 = group["alpha-3"]
        region1 = group["region"]
        subregion1 = group["sub-region"]
for group in code:
    if group["name"]==D_raw1[0][1]:
        code2 = str(group["alpha-3"])
        region2 = group["region"]
        subregion2 = group["sub-region"]
D_dict1["Kode"]= [code1,code2]
D_dict1["Region"] = [region1,region2]
D_dict1["Sub-region"]=[subregion1,subregion2]
D_table1 = pd.DataFrame(D_dict1)

D_dict2 = dict()
D_raw2 = []
for name,prod in C_dict.items():
    c = prod,name
    D_raw2.append(c)
D_raw2.sort()

D_dict2["Deskripsi"] = ["Produksi terbesar","Produksi terkecil"]
D_dict2["Negara"] = [str(C_raw[0][1]),str(D_raw2[0][1])]
for group in code:
    if group["name"]==C_raw[0][1]:
        code1 = group["alpha-3"]
        region1 = group["region"]
        subregion1 = group["sub-region"]
for group in code:
    if group["name"]==D_raw2[0][1]:
        code2 = str(group["alpha-3"])
        region2 = group["region"]
        subregion2 = group["sub-region"]
D_dict2["Kode"]= [code1,code2]
D_dict2["Region"] = [region1,region2]
D_dict2["Sub-region"]=[subregion1,subregion2]
D_table2 = pd.DataFrame(D_dict2)

###1D###

##1E##
zero_country1 = []
zero_code1 = []
zero_reg1 = []
zero_subreg1 = []
zero_dict1 = dict()
for set in B_raw:
    if set[0]==0:
        zero_country1.append(set[1])
for name in zero_country1:
    for group in code:
        if group["name"]==name:
            zero_code1.append(group["alpha-3"])
            zero_reg1.append(group["region"])
            zero_subreg1.append(group["sub-region"])
            
zero_dict1["Negara"] = zero_country1
zero_dict1["Kode"] = zero_code1
zero_dict1["Region"] = zero_reg1
zero_dict1["Sub-region"] = zero_subreg1
zero_table1 = pd.DataFrame(zero_dict1)

zero_country2 = []
zero_code2 = []
zero_reg2 = []
zero_subreg2 = []
zero_dict2 = dict()
for set in C_raw:
    if set[0]==0:
        zero_country2.append(set[1])
for name in zero_country2:
    for group in code:
        if group["name"]==name:
            zero_code2.append(group["alpha-3"])
            zero_reg2.append(group["region"])
            zero_subreg2.append(group["sub-region"])

zero_dict2["Negara"] = zero_country2
zero_dict2["Kode"] = zero_code2
zero_dict2["Region"] = zero_reg2
zero_dict2["Sub-region"] = zero_subreg2
zero_table2 = pd.DataFrame(zero_dict2)
###1E###

with left_col.expander("Lihat Summary Data Tahun "+tahun):
    st.subheader(" Tabel Summary Data Tahun "+str(tahun))
    st.table(D_table1)
    st.subheader(" Tabel Zero Production Tahun "+str(tahun))
    st.write("Kumpulan negara dengan besar produksi minyak mentah nol pada tahun "+tahun)
    st.table(zero_table1)
    

with right_col.expander("Lihat Summary Data Kumulatif"):
    st.subheader(" Tabel Summary Data Kumulatif")
    st.table(D_table2)
    st.subheader(" Tabel Zero Production Kumulatif")
    st.write("Kumpulan negara dengan besar produksi minyak mentah nol untuk keseluruhan tahun")
    st.table(zero_table2)

image3 = Image.open('AXIOM_banner4.png')
st.image(image3)