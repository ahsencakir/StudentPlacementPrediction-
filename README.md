# 🎓 Öğrenci Yerleşme Tahmin Projesi

## 📌 Veri Seti Seçim Nedeni

Bu proje kapsamında öğrencilerin işe yerleşip yerleşemeyeceklerini sınıflandırmak amacıyla, akademik başarı, sosyal etkinlikler, beceri puanları ve sertifikalar gibi çok yönlü değişkenler içeren kapsamlı bir veri seti tercih edilmiştir.

Bu veri setini seçmemizin başlıca nedenleri şunlardır:

- **Kariyer Planlamasında Önemi:** Öğrencilerin yerleşme potansiyelini tahmin etmek, eğitim kurumlarının kariyer rehberliği sunmasında büyük katkı sağlar.
- **Kapsamlı Özellik Seti:** CGPA, yetenek testi, proje sayısı, staj ve atölye çalışmaları gibi birçok akademik ve sosyal gösterge içerir.
- **Makine Öğrenmesi Uygunluğu:** Hem sayısal hem kategorik veriler içerdiğinden çeşitli algoritmalarla etkili biçimde çalıştırılabilir.

---
Aşağıda her sütunun (özelliğin) anlamı açıklanmıştır:

    CGPA: Öğrencinin genel not ortalamasını (Cumulative Grade Point Average) ifade eder. Akademik başarısını gösterir.

    Internships (Stajlar): Öğrencinin yaptığı staj sayısını gösterir. Gerçek dünya deneyimi kazandığını gösterir.

    Projects (Projeler): Öğrencinin gerçekleştirdiği proje sayısı. Teknik bilgi ve uygulama becerisini gösterir.

    Workshops/Certifications (Atölyeler/Sertifikalar): Öğrencinin çevrim içi kurslar ya da sertifika programlarına katılımını ifade eder. Kendini geliştirme isteğini gösterir.

    ApptitudeTestScore (Yetenek Testi Skoru): Öğrencinin sayısal ve mantıksal düşünme yeteneğini ölçen sınavdan aldığı puandır. İşe alım sürecinde önemli bir yer tutar.

    SoftSkillRating (İletişim Becerisi Değerlendirmesi): Öğrencinin iletişim, takım çalışması gibi sosyal becerilerdeki yeterliliğini gösterir.

    ExtraCurricularActivities (Sosyal Etkinlikler): Akademik olmayan alanlardaki faaliyetlere katılımı gösterir (spor, kulüp, gönüllülük vs.). Öğrencinin çok yönlü kişiliği hakkında bilgi verir.

    PlacementTraining (Yerleştirme Eğitimi): Üniversitenin öğrencilere verdiği işe yerleştirme süreciyle ilgili özel eğitimlerdir.

    SSC ve HSC (Lise ve Ortaokul Notları): Öğrencinin lise (Higher Secondary Certificate - HSC) ve ortaokul (Senior Secondary Certificate - SSC) dönemlerindeki başarı puanlarıdır.

    PlacementStatus (Yerleştirme Durumu): Bu, hedef (target) sütundur. İki sınıf içerir: "placed" (işe yerleşmiş) ve "not placed" (işe yerleşmemiş).

## ⚙️ Özellik Seçim Yöntemleri

Aşağıdaki üç farklı özellik seçim yöntemi kullanılmış ve performansları karşılaştırılmıştır:

### 1. **SelectKBest (f_classif)**
- ANOVA F-skoruna göre en anlamlı özellikleri seçer.
- Akademik başarıyla doğrudan ilişkili değişkenleri öne çıkarmıştır.
- Basit ve hızlı bir yöntemdir.

### 2. **RFE (Recursive Feature Elimination)**
- Model tabanlı iteratif bir yöntemdir.
- CGPA, Soft Skills gibi bireysel başarı göstergelerini seçmiştir.
- Genellikle daha yüksek doğruluk sağlar.

### 3. **Mutual Information**
- Özelliklerin hedef değişkenle olan bilgi kazancını ölçer.
- Doğrusal olmayan ilişkileri yakalayabilir.
- Bazı sosyal göstergeleri vurgulamakta etkili olmuştur.

---

## 🤖 Uygulanan Modeller ve Değerlendirme

| Sıra | Model Adı                    | Tür / Yaklaşım              | Açıklama                                                                                          |
|------|------------------------------|-----------------------------|---------------------------------------------------------------------------------------------------|
| 1    | **Logistic Regression**      | Doğrusal / Parametrik       | Hızlı, yorumlanabilir ve temel sınıflandırmalarda etkili.                                        |
| 2    | **Decision Tree**            | Karar Ağacı / Kural Bazlı   | Şeffaf ve açıklanabilir; ancak aşırı öğrenme riski taşır.                                        |
| 3    | **Random Forest**            | Ensemble / Bagging          | Kararlı ve güçlü sonuçlar verir. Dengesiz veri yapılarında avantajlıdır.                         |
| 4    | **Support Vector Machine**   | Marjin Maksimizasyonu / Kernel | Küçük ve karmaşık veri setlerinde etkili. Sınıflar arası ayrımı iyi yapar.                   |

---

## 📊 Genel Değerlendirme

- Özellik seçim yöntemleri içinde **RFE**, en iyi genel doğruluk ve F1 skoru sağlamıştır.
- **Random Forest** ve **Logistic Regression** modelleri, kararlı sonuçlarıyla ön plana çıkmıştır.
- **Mutual Information**, sosyal ve doğrusal olmayan özelliklerde etkili olmuş fakat genel başarıda geride kalmıştır.
- Sınıf dengesizliklerine karşı tüm modellerde `class_weight='balanced'` parametresi uygulanmıştır.
- Modeller `Accuracy`, `Precision`, `Recall` ve `F1-Score` gibi metriklerle değerlendirilmiştir.

---

## 🚀 Nasıl Çalıştırılır?

### Gereksinimler:
```
streamlit
pandas
scikit-learn
joblib
```

### Kurulum:

```bash
pip install -r requirements.txt
```

### Uygulama Başlatma:

```bash
streamlit run streamlit_app.py
```

---

## 🌐 Canlı Demo
> Hazırladığımız demoyu inceleyebilirsiniz: [Öğrenci Yerleşme Tahmin Projesi](https://studentplacement.streamlit.app/)
