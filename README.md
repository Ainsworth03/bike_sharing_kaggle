# Feb's Bike Rentals

answering several business questions from bike sharing dataset on Kaggle
## Questions to Answer:

- Bagaimana tren penyewaan sepeda setiap bulan selama tahun 2011 sampai 2012?
- Bagaimana pengaruh registered dengan rate sewa sepeda?
- Pada jam berapa umumnya penyewaan sepeda paling banyak?
- Pada jam berapa baiknya perawatan harian sepeda dilakukan agar tidak mengganggu pelanggan?





## Setup Envoirement Shell/Terminal

Create project directory

```bash
mkdir project_data_analyst
```

Move to project directory
```bash
cd project_data_analyst
```

Make Virtual Envoirement
```bash
python -m venv projectvenv
```

Activate Virtual Envoirment
```bash
.\projectvenv\Scripts\activate
```

Install all libraries neeeded (requirements.txt is made using freeze from the original project)
```bash
pip install -r requirements.txt
```

## Open Streamlit Dashboard

change directory to dashboard

```bash
cd dashboard
```

run the dashboard

```bash
streamlit run dashboard.py
```
