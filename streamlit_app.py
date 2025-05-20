import streamlit as st
import pandas as pd
import joblib

# Model dosya yolları
model_paths = {
    'SVM': {
        'SelectKBest': 'models/model_SVM_SelectKBest.pkl',
        'RFE': 'models/model_SVM_RFE.pkl',
        'Mutual Information': 'models/model_SVM_MutualInformation.pkl'
    }
}

# Özellik setleri
feature_sets = {
    'SelectKBest': ['AptitudeTestScore', 'HSC_Marks', 'ExtracurricularActivities', 'Projects', 'SSC_Marks'],
    'RFE': ['AptitudeTestScore', 'HSC_Marks', 'SoftSkillsRating', 'CGPA', 'SSC_Marks'],
    'Mutual Information': ['AptitudeTestScore', 'HSC_Marks', 'Projects', 'ExtracurricularActivities', 'SSC_Marks', 'SoftSkillsRating', 'CGPA', 'Workshops/Certifications', 'PlacementTraining', 'Internships']
}

# TR-EN etiket eşleşmeleri
label_map = {
    'AptitudeTestScore': "Yetenek Testi Puanı",
    'HSC_Marks': "Lise Not Ortalaması (HSC)", 
    'Projects': "Proje Sayısı",
    'ExtracurricularActivities': "Ekstra Aktiviteler",
    'SSC_Marks': "Ortaokul Not Ortalaması (SSC)",
    'SoftSkillsRating': "İletişim Beceri Puanı",
    'CGPA': "Genel Not Ortalaması (GPA)",
    'Workshops/Certifications': "Atölye/Sertifika Sayısı",
    'PlacementTraining': "Yerleştirme Eğitimi",
    'Internships': "Staj Sayısı"
}

# Encoding sözlükleri
gender_encoding = {'Erkek (Male)': 1, 'Kadın (Female)': 0}

# --- ÖRNEK INPUTLAR ---
example_inputs = {
    'Yerleşemeyecek Öğrenci': {
        'AptitudeTestScore': 50,
        'HSC_Marks': 50,
        'Projects': 0,
        'ExtracurricularActivities': 0,
        'SSC_Marks': 50,
        'SoftSkillsRating': 2,
        'CGPA': 3,
        'Workshops/Certifications': 0,
        'PlacementTraining': 0,
        'Internships': 0
    },
    'Yerleşecek Öğrenci': {
        'AptitudeTestScore': 90,
        'HSC_Marks': 82,
        'Projects': 3,
        'ExtracurricularActivities': 1,
        'SSC_Marks': 78,
        'SoftSkillsRating': 4.0,
        'CGPA': 8.9,
        'Workshops/Certifications': 2,
        'PlacementTraining': 1,
        'Internships': 0
    }
}

# Streamlit Arayüzü
st.title("🎓 Öğrenci Yerleşme Tahmini Uygulaması")
model_choice = st.selectbox("🔍 Model Seçin", list(model_paths.keys()))
feature_choice = st.selectbox("🧩 Özellik Seti Seçin", list(feature_sets.keys()))

# --- ÖRNEK ÖĞRENCİ BUTONLARI ---
col1, col2 = st.columns(2)
if col1.button('Yerleşemeyecek Öğrenci'):
    for feature in feature_sets[feature_choice]:
        if feature in example_inputs['Yerleşemeyecek Öğrenci']:
            st.session_state[feature] = example_inputs['Yerleşemeyecek Öğrenci'][feature]
if col2.button('Yerleşecek Öğrenci'):
    for feature in feature_sets[feature_choice]:
        if feature in example_inputs['Yerleşecek Öğrenci']:
            st.session_state[feature] = example_inputs['Yerleşecek Öğrenci'][feature]

# Girdi Formu
st.subheader("📝 Girdi Verileri")
inputs = {}

for feature in feature_sets[feature_choice]:
    label = label_map.get(feature, feature)

    if feature in ['AptitudeTestScore', 'HSC_Marks', 'SSC_Marks']:
        inputs[feature] = float(st.number_input(label, min_value=0.0, max_value=100.0, step=1.0, 
                                        value=float(st.session_state.get(feature, 0.0)), 
                                        key=feature))

    elif feature == 'CGPA':
        inputs[feature] = float(st.number_input(label, min_value=0.0, max_value=10.0, step=0.1, 
                                        value=float(st.session_state.get(feature, 0.0)), 
                                        key=feature))

    elif feature == 'SoftSkillsRating':
        inputs[feature] = float(st.number_input(label, min_value=0.0, max_value=5.0, step=0.1, 
                                        value=float(st.session_state.get(feature, 0.0)), 
                                        key=feature))

    elif feature == 'ExtracurricularActivities':
        inputs[feature] = int(st.selectbox(label, [0, 1], format_func=lambda x: "Hayır" if x == 0 else "Evet",
                                        index=int(st.session_state.get(feature, 0)), 
                                        key=feature))

    elif feature == 'PlacementTraining':
        inputs[feature] = int(st.selectbox(label, [0, 1], format_func=lambda x: "Hayır" if x == 0 else "Evet",
                                        index=int(st.session_state.get(feature, 0)), 
                                        key=feature))

    elif feature in ['Projects', 'Workshops/Certifications', 'Internships']:
        inputs[feature] = int(st.number_input(label, min_value=0, max_value=10, step=1, 
                                        value=int(st.session_state.get(feature, 0)), 
                                        key=feature))

    else:
        inputs[feature] = float(st.number_input(label, min_value=0.0, step=1.0, 
                                        value=float(st.session_state.get(feature, 0.0)), 
                                        key=feature))

# Tahmin Butonu
if st.button("📊 Tahmin Et"):
    model_data = joblib.load(model_paths[model_choice][feature_choice])
    model = model_data['model']
    expected_features = model_data['features']

    # Sadece seçili özellik setindeki değerleri al
    ordered_inputs = {}
    for feature in expected_features:
        if feature in inputs:
            ordered_inputs[feature] = inputs[feature]
        else:
            ordered_inputs[feature] = 0.0

    # DataFrame oluştur
    input_df = pd.DataFrame([ordered_inputs])

    # Debug için modelin beklediği özellikleri ve sırasını göster
    st.write("Modelin beklediği özellikler ve sırası:", expected_features)
    st.write("Girilen Değerler:", ordered_inputs)

    # Tahmin yap
    try:
        prediction = model.predict(input_df)[0]
        prediction_proba = model.predict_proba(input_df)[0]
    except Exception as e:
        st.error(f"⚠️ Tahmin sırasında hata oluştu: {e}")
        st.stop()

    st.write("📌 Model Tahmini (Ham Değer):", prediction)

    # Tahmin sonuçlarını güncelle
    label_map_result = {
       0: 'Yerleşemeyecek',
       1: 'Yerleşecek'
    }

    if prediction in label_map_result:
        st.success(f"✅ Tahmin Sonucu: **{label_map_result[prediction]}**")

        # Modelin hangi sınıfı neden seçtiğini yaz
        selected_class = model.classes_[prediction]
        selected_proba = prediction_proba[prediction]

        st.info(f"🧠 Model, **'{label_map_result[selected_class]}'** sınıfını **{selected_proba:.2%}** olasılıkla seçti.")
        
        # Olasılık grafiği (isteğe bağlı)
        st.subheader("🔍 Olasılık Dağılımı")
        proba_df = pd.DataFrame({
            'Sınıf': [label_map_result.get(i, str(i)) for i in model.classes_],
            'Olasılık': prediction_proba
        })
        st.bar_chart(proba_df.set_index('Sınıf'))

    else:
        st.error(f"❌ Beklenmeyen tahmin değeri: {prediction}")
