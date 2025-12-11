# דוח בעיות בנתונים ופתרונות
# Data Issues Report & Solutions

---

## 🚨 סיכום חומרת הבעיות | Severity Summary

| בעיה | חומרה | השפעה |
|------|-------|-------|
| **Data Leakage** | 🔴 קריטי | מבטל תוקף כל הערכת מודל |
| **CSV Parsing Issues** | 🔴 קריטי | 3,844 רשומות עם תיוג שגוי |
| **Class Imbalance** | 🟠 גבוה | מודל יטה לתיוגים נפוצים |
| **Extreme Sequence Lengths** | 🟡 בינוני | בעיות בפדינג/טרנקציה |
| **Duplicate Sequences** | 🟡 בינוני | אובר-פיטינג אפשרי |

---

## 🔴 בעיה #1: DATA LEAKAGE (קריטי!)

### הממצא:
```
┌─────────────────────────────────────────────────────────────┐
│  ⚠️  זליגת נתונים חמורה בין הסטים!                          │
├─────────────────────────────────────────────────────────────┤
│  Train ∩ Test:        7,204 רצפים זהים  (87% מ-Test!)      │
│  Train ∩ Validation:  4,577 רצפים זהים  (100% מ-Val!)      │
│  Test ∩ Validation:     903 רצפים זהים                     │
└─────────────────────────────────────────────────────────────┘
```

### המשמעות:
- **הערכת המודל לא אמינה** - המודל "ראה" את הדוגמאות ב-test/validation
- **Accuracy מנופח** - תוצאות ייראו טובות מהמציאות
- **Validation Set כמעט חסר תועלת** - 100% חפיפה עם Train!

### 📋 פתרונות:

#### פתרון 1: יצירת חלוקה חדשה (מומלץ)
```python
import pandas as pd
from sklearn.model_selection import train_test_split

# טעינת כל הנתונים
all_data = pd.concat([train_df, test_df, val_df])

# הסרת כפילויות
all_data_unique = all_data.drop_duplicates(subset=['NucleotideSequence'])

# חלוקה חדשה נקייה
train_new, temp = train_test_split(all_data_unique, test_size=0.3, 
                                    stratify=all_data_unique['GeneType'],
                                    random_state=42)
val_new, test_new = train_test_split(temp, test_size=0.5,
                                      stratify=temp['GeneType'],
                                      random_state=42)
```

#### פתרון 2: סינון רצפים כפולים מ-Test/Val
```python
# שמירת רק רצפים ייחודיים ב-test
test_unique = test_df[~test_df['NucleotideSequence'].isin(train_df['NucleotideSequence'])]
val_unique = val_df[~val_df['NucleotideSequence'].isin(train_df['NucleotideSequence'])]
```

---

## 🔴 בעיה #2: CSV PARSING ISSUES (קריטי!)

### הממצא:
```
3,844 רשומות (17%!) עם GeneType שגוי!

דוגמאות לערכי GeneType פגומים:
- " 7SL"                  (656 רשומות)
- " pseudogene""          (178 רשומות)  
- " mitochondrial-like""  (8 רשומות)
- " Y-linked""            (7 רשומות)
- " folic acid type"      (8 רשומות)
```

### הסיבה:
שדה Description מכיל פסיקים (`,`) שגורמים לפיצול שגוי של העמודות בקריאת ה-CSV.

### 📋 פתרונות:

#### פתרון 1: קריאה נכונה עם quoting
```python
import pandas as pd

# קריאה נכונה - התעלמות מפסיקים בתוך מרכאות
df = pd.read_csv('train.csv', 
                  quoting=1,  # QUOTE_ALL
                  escapechar='\\')
```

#### פתרון 2: תיקון רטרואקטיבי
```python
# מיפוי ערכים שגויים לנכונים
fix_mapping = {
    ' 7SL': 'ncRNA',
    ' pseudogene"': 'PSEUDO',
    ' mitochondrial-like"': 'PSEUDO',
    ' Y-linked"': 'PSEUDO',
    # ... להמשיך עבור כל הערכים הפגומים
}

df['GeneType'] = df['GeneType'].replace(fix_mapping)
df['GeneType'] = df['GeneType'].str.strip().str.strip('"')
```

#### פתרון 3: סינון רשומות פגומות
```python
valid_gene_types = ['PSEUDO', 'BIOLOGICAL_REGION', 'ncRNA', 'snoRNA', 
                    'PROTEIN_CODING', 'tRNA', 'OTHER', 'rRNA', 'snRNA', 'scRNA']
df_clean = df[df['GeneType'].isin(valid_gene_types)]
```

---

## 🟠 בעיה #3: CLASS IMBALANCE (חוסר איזון)

### הממצא:
```
התפלגות GeneType:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PSEUDO            ████████████████████████████  30.9%
BIOLOGICAL_REGION ███████████████████████████▌  30.6%
ncRNA             ███████████                   11.0%
snoRNA            ██▊                            2.8%
PROTEIN_CODING    ██▎                            2.3%
tRNA              ██▏                            2.2%
OTHER             █▋                             1.6%
rRNA              █▏                             1.1%
snRNA             ▌                              0.5%
scRNA             ▏                              0.01%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

יחס: PSEUDO (6,976) vs scRNA (3) = 2,325:1 !
```

### 📋 פתרונות:

#### פתרון 1: Class Weights
```python
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

# חישוב משקלות אוטומטי
class_weights = compute_class_weight('balanced', 
                                      classes=np.unique(y_train), 
                                      y=y_train)
class_weight_dict = dict(zip(np.unique(y_train), class_weights))

# שימוש באימון
model.fit(X, y, class_weight=class_weight_dict)
```

#### פתרון 2: Oversampling (SMOTE)
```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
```

#### פתרון 3: Undersampling
```python
from imblearn.under_sampling import RandomUnderSampler

rus = RandomUnderSampler(random_state=42)
X_resampled, y_resampled = rus.fit_resample(X_train, y_train)
```

#### פתרון 4: מיזוג קטגוריות נדירות
```python
# מיזוג קטגוריות עם פחות מ-100 דגימות ל-"OTHER"
rare_classes = df['GeneType'].value_counts()[df['GeneType'].value_counts() < 100].index
df['GeneType'] = df['GeneType'].replace(rare_classes, 'OTHER')
```

---

## 🟡 בעיה #4: EXTREME SEQUENCE LENGTHS

### הממצא:
```
סטטיסטיקות אורך רצפים:
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Min:     3 נוקלאוטידים (!)
Max:     1,001 נוקלאוטידים
Mean:    360.7
Median:  296
━━━━━━━━━━━━━━━━━━━━━━━━━━━

רצפים קצרים מדי (<30):
- 3 נוקלאוטידים (1 רשומה!)
- 8-29 נוקלאוטידים (~20 רשומות)
```

### 📋 פתרונות:

#### פתרון 1: סינון רצפים קצרים מדי
```python
MIN_SEQ_LENGTH = 30
df = df[df['NucleotideSequence'].str.len() >= MIN_SEQ_LENGTH + 2]  # +2 for <> markers
```

#### פתרון 2: Padding/Truncation אחיד
```python
MAX_LENGTH = 500  # או לפי percentile 95

def preprocess_sequence(seq, max_len=MAX_LENGTH):
    seq = seq.strip('<>')
    if len(seq) > max_len:
        return seq[:max_len]  # Truncate
    return seq.ljust(max_len, 'N')  # Pad with N
```

#### פתרון 3: Bucketing לפי אורך
```python
def length_bucket(length):
    if length < 100: return 'short'
    elif length < 500: return 'medium'
    else: return 'long'

df['seq_length_bucket'] = df['NucleotideSequence'].str.len().apply(length_bucket)
```

---

## 🟡 בעיה #5: DUPLICATE SEQUENCES (בתוך הסט)

### הממצא:
```
רצפים ייחודיים:  21,884 (96.9%)
רצפים כפולים:    709 (3.1%)
```

### 📋 פתרונות:

#### פתרון 1: הסרת כפילויות
```python
df_unique = df.drop_duplicates(subset=['NucleotideSequence'], keep='first')
```

#### פתרון 2: בדיקת עקביות התיוג
```python
# האם רצפים זהים מתויגים אחרת?
dup_seqs = df[df.duplicated(subset=['NucleotideSequence'], keep=False)]
inconsistent = dup_seqs.groupby('NucleotideSequence')['GeneType'].nunique()
problematic = inconsistent[inconsistent > 1]
print(f"רצפים עם תיוג לא עקבי: {len(problematic)}")
```

---

## 📊 סיכום כמותי | Quantitative Summary

| מדד | ערך | בעיה? |
|-----|-----|-------|
| סה"כ רשומות | 35,496 | - |
| רשומות עם GeneType פגום | 3,844 (10.8%) | 🔴 |
| Data Leakage Train→Test | 7,204 (86.5% מ-Test) | 🔴 |
| Data Leakage Train→Val | 4,577 (100% מ-Val) | 🔴 |
| יחס חוסר איזון מקסימלי | 2,325:1 | 🟠 |
| רצפים קצרים (<30) | ~20 | 🟡 |
| רצפים כפולים | 709 (3.1%) | 🟡 |

---

## ✅ צ'קליסט לניקוי הנתונים | Data Cleaning Checklist

```
□ 1. תקן את קריאת ה-CSV עם quoting נכון
□ 2. נקה/תקן ערכי GeneType פגומים
□ 3. צור חלוקה חדשה Train/Test/Val ללא חפיפה
□ 4. החלט על אסטרטגיה לחוסר איזון
□ 5. קבע אורך מקסימלי/מינימלי לרצפים
□ 6. הסר או סמן רצפים כפולים
□ 7. וודא עקביות תיוג לרצפים זהים
□ 8. שקול להסיר משתנים מיותרים (ראה CORRELATION_ANALYSIS.md)
```

---

## 🛠️ סקריפט ניקוי מומלץ | Recommended Cleaning Script

```python
import pandas as pd
from sklearn.model_selection import train_test_split

def clean_dna_dataset(train_path, test_path, val_path):
    """
    ניקוי מלא של מערך הנתונים
    """
    
    # 1. טעינה נכונה
    train = pd.read_csv(train_path, index_col=0)
    test = pd.read_csv(test_path, index_col=0)
    val = pd.read_csv(val_path, index_col=0)
    
    # 2. איחוד
    all_data = pd.concat([train, test, val], ignore_index=True)
    
    # 3. תיקון GeneType
    valid_types = ['PSEUDO', 'BIOLOGICAL_REGION', 'ncRNA', 'snoRNA', 
                   'PROTEIN_CODING', 'tRNA', 'OTHER', 'rRNA', 'snRNA', 'scRNA']
    all_data = all_data[all_data['GeneType'].isin(valid_types)]
    
    # 4. הסרת כפילויות
    all_data = all_data.drop_duplicates(subset=['NucleotideSequence'])
    
    # 5. סינון רצפים קצרים
    all_data['seq_len'] = all_data['NucleotideSequence'].str.len() - 2
    all_data = all_data[all_data['seq_len'] >= 30]
    
    # 6. חלוקה חדשה
    train_new, temp = train_test_split(
        all_data, test_size=0.3, 
        stratify=all_data['GeneType'], 
        random_state=42
    )
    val_new, test_new = train_test_split(
        temp, test_size=0.5, 
        stratify=temp['GeneType'], 
        random_state=42
    )
    
    print(f"Train: {len(train_new)}")
    print(f"Test: {len(test_new)}")
    print(f"Val: {len(val_new)}")
    
    return train_new, test_new, val_new

# הפעלה
train_clean, test_clean, val_clean = clean_dna_dataset(
    'train.csv', 'test.csv', 'validation.csv'
)
```

---

*דוח זה מזהה את הבעיות העיקריות בנתונים ומציע פתרונות מעשיים*

