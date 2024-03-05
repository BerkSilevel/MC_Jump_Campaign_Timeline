import streamlit as st
import pandas as pd
import altair as alt


# CSV dosyasını yükle
uploaded_file = "uploaded_data.csv"

if uploaded_file is not None:
    # Veri setini DataFrame'e yükle
    data = pd.read_csv(uploaded_file)

    # Tarih sütunlarını datetime formatına dönüştür
    data['start_date'] = pd.to_datetime(data['start_date'], format='%Y-%m-%d')
    data['last_date'] = pd.to_datetime(data['last_date'], format='%Y-%m-%d')

    # Unikal kaynak adlarını al
    unique_sources = data['source'].unique().tolist()

    # Kaynak seçim kontrolü
    selected_sources = st.multiselect("Kaynakları Seçin", unique_sources)

    # Seçilen kaynağa göre kampanyaları filtrele
    filtered_campaigns = data[data['source'].isin(selected_sources)]['adn_campaign_name'].unique().tolist()

    # Kampanya seçim kontrolü
    selected_campaigns = st.multiselect("Kampanyaları Seçin", filtered_campaigns, default=filtered_campaigns)

    # Seçilen kampanyalara ve kaynaklara göre veriyi filtrele
    filtered_data = data[(data['source'].isin(selected_sources)) & (data['adn_campaign_name'].isin(selected_campaigns))]

    # Renk kodunu tanımla
    color = alt.Color('source:N', scale=alt.Scale(domain=selected_sources, range=['#D87097', '#159AD0', '#99D686']), legend=alt.Legend(title="Kaynak"))

    # Zaman çizelgesini oluştur
    st.write("""
    # Zaman Çizelgesi
    """)

    # Yatay kaydırma ekleyerek zaman çizelgesini çiz
    chart = alt.Chart(filtered_data).mark_bar().encode(
        x='start_date:T',
        x2='last_date:T',
        y=alt.Y('adn_campaign_name', axis=alt.Axis(labelAngle=0)),
        tooltip=['adn_campaign_name', 'start_date', 'last_date'],
        color=color
    ).properties(
        width=800
    ).interactive()

    st.write(chart)
