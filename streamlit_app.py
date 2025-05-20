import streamlit as st
import pandas as pd
import joblib

# Model dosya yolu
MODEL_PATH = 'model/model_SVM_MutualInformation.pkl'

# Modeli ve bilgileri yükle
model_data = joblib.load(MODEL_PATH)
model = model_data['model']
expected_features = model_data['feature_names']

# TR etiket eşleştirmeleri
label_map = {
    'AptitudeTestScore': "Yetenek Testi Puanı",
    'HSC_Marks': "Lise Not Ortalaması", 
    'Projects': "Proje Sayısı",
    'ExtracurricularActivities': "Ekstra Aktiviteler",
    'SSC_Marks': "Ortaokul Not Ortalaması",
    'SoftSkillsRating': "İletişim Beceri Puanı",
    'CGPA': "Genel Not Ortalaması",
    'Workshops/Certifications': "Atölye/Sertifika Sayısı",
    'PlacementTraining': "Yerleştirme Eğitimi",
    'Internships': "Staj Sayısı"
}

# Örnek veriler
example_inputs = {
    'Yerleşemeyecek Öğrenci': {
        'AptitudeTestScore': 0,
        'HSC_Marks': 0,
        'Projects': 0,
        'ExtracurricularActivities': 0,
        'SSC_Marks': 0,
        'SoftSkillsRating': 0,
        'CGPA': 0,
        'Workshops/Certifications': 0,
        'PlacementTraining': 0,
        'Internships': 0
    },

    'Yerleşecek Öğrenci': {
        'AptitudeTestScore': 86,
        'HSC_Marks': 65,
        'Projects': 3,
        'ExtracurricularActivities': 1,
        'SSC_Marks': 76,
        'SoftSkillsRating': 4.4,
        'CGPA': 8.2,
        'Workshops/Certifications': 2,
        'PlacementTraining': 1,
        'Internships': 1
    }
}

# Başlık
st.title("🎓 Öğrencinin İşe Yerleşme Tahmini")

# Örnek veri butonları
col1, col2 = st.columns(2)
if col1.button("Yerleşemeyecek Öğrenci"):
    for f, v in example_inputs['Yerleşemeyecek Öğrenci'].items():
        st.session_state[f] = v
if col2.button("Yerleşecek Öğrenci"):
    for f, v in example_inputs['Yerleşecek Öğrenci'].items():
        st.session_state[f] = v

# Girdi formu
st.subheader("📝 Öğrenci Bilgileri")
inputs = {}

for feature in expected_features:
    label = label_map.get(feature, feature)

    if feature in ['AptitudeTestScore', 'HSC_Marks', 'SSC_Marks']:
        inputs[feature] = st.number_input(
            label, min_value=0.0, max_value=100.0, step=1.0,
            value=float(st.session_state.get(feature, 0.0))
        )
    elif feature == 'CGPA':
        inputs[feature] = st.number_input(
            label, min_value=0.0, max_value=10.0, step=0.1,
            value=float(st.session_state.get(feature, 0.0))
        )
    elif feature == 'SoftSkillsRating':
        inputs[feature] = st.number_input(
            label, min_value=0.0, max_value=5.0, step=0.1,
            value=float(st.session_state.get(feature, 0.0))
        )
    elif feature in ['ExtracurricularActivities', 'PlacementTraining']:
        inputs[feature] = st.selectbox(
            label, [0, 1],
            format_func=lambda x: "Hayır" if x == 0 else "Evet",
            index=int(st.session_state.get(feature, 0))
        )
    else:
        inputs[feature] = st.number_input(
            label, min_value=0, max_value=10, step=1,
            value=int(st.session_state.get(feature, 0))
        )

# Tahmin butonu
if st.button("📊 Tahmin Et"):
    input_df = pd.DataFrame([inputs])

    # Tahmin
    try:
        prediction = model.predict(input_df)[0]
        proba = model.predict_proba(input_df)[0]
    except Exception as e:
        st.error(f"Tahmin sırasında hata oluştu: {e}")
        st.stop()

    # Etiket eşlemesi
    label_result = {0: "Yerleşemeyecek", 1: "Yerleşecek"}

    # Tahmin edilen sınıfın olasılığı
    class_index = list(model.classes_).index(prediction)
    selected_proba = proba[class_index]

    # Tahmin sonucu
    st.success(f"✅ Tahmin: **{label_result[prediction]}**")

