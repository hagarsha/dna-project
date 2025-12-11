# ניתוח קורלציות וזיהוי משתנים מיותרים
# Correlation Analysis & Redundant Variables Detection

---

## 1. סיכום ממצאים | Executive Summary

### משתנים מיותרים שזוהו:

| משתנה | סטטוס | סיבה |
|-------|-------|------|
| **GeneGroupMethod** | ⚠️ **מיותר** | ~83% מהערכים זהים ("NCBI Ortholog") - שונות נמוכה מאוד |
| **NCBIGeneID** | ⚠️ **מיותר לסיווג** | מזהה ייחודי בלבד, אין ערך פרדיקטיבי |
| **Description** | ⚠️ **רדונדנטי חלקית** | מכיל מידע שניתן לחלץ מ-GeneType |
| **Symbol** | ✅ **שימושי** | מכיל דפוסים פרדיקטיביים לגבי GeneType |
| **GeneType** | ✅ **חיוני** | משתנה היעד (Label) |
| **NucleotideSequence** | ✅ **חיוני** | המשתנה העיקרי לניתוח |

---

## 2. ניתוח מפורט | Detailed Analysis

### 2.1 GeneGroupMethod - **מיותר**

```
התפלגות ערכים:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NCBI Ortholog    ████████████████████████████████████████  ~83%
PSEUDO           ██                                         ~4%
snoRNA           █                                          ~2%
pseudogene"      ███                                        ~7%
אחר              █                                          ~4%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**בעיות:**
- **שונות נמוכה מאוד** - ~83% מהערכים הם "NCBI Ortholog"
- **מידע שכבר קיים** - ערכים אחרים (PSEUDO, snoRNA) חופפים ל-GeneType
- **זליגת נתונים (Data Leakage)** - חלק מהערכים הם למעשה GeneType!

**המלצה:** ❌ **להסיר משתנה זה מהמודל**

---

### 2.2 NCBIGeneID - **מיותר לסיווג**

```
סטטיסטיקות:
- 22,593 ערכים ייחודיים מתוך 22,593 רשומות (100% ייחודי)
- משמש כמזהה (Primary Key) בלבד
- אין קורלציה עם GeneType
```

**המלצה:** ❌ **להסיר - מזהה בלבד, אין ערך פרדיקטיבי**

---

### 2.3 Description - **רדונדנטי חלקית**

**קורלציה עם GeneType:**

| מילת מפתח ב-Description | קורלציה עם GeneType |
|------------------------|---------------------|
| "pseudogene" | → PSEUDO (93%+ מהמקרים) |
| "regulatory region" | → BIOLOGICAL_REGION |
| "microRNA" | → ncRNA |
| "small nucleolar" | → snoRNA |
| "ribosomal" | → rRNA או PSEUDO |

```
ניתוח "pseudogene" בטקסט:
- רשומות עם "pseudogene" בתיאור: 9,517
- רשומות עם GeneType=PSEUDO: 10,220
- חפיפה: ~93% מהרשומות עם "pseudogene" הן אכן PSEUDO
```

**בעיות:**
- **רדונדנטיות** - המילים ב-Description מנבאות את GeneType
- **זליגת נתונים** - שימוש ב-Description עלול "לרמות" במודל

**המלצה:** ⚠️ **להשתמש בזהירות או להסיר אם המטרה לסווג לפי רצף בלבד**

---

### 2.4 Symbol - **שימושי אך מכיל רדונדנטיות**

**דפוסים שזוהו:**

| דפוס ב-Symbol | GeneType נפוץ | כמות |
|---------------|---------------|------|
| מתחיל ב-"LOC" | BIOLOGICAL_REGION | 6,893 (70%) |
| מתחיל ב-"LOC" | PSEUDO | 1,206 (12%) |
| מתחיל ב-"RPL" | PSEUDO | 1,105 |
| מתחיל ב-"RPS" | PSEUDO | 576 |
| מסתיים ב-"P" | PSEUDO | ~67% |
| מתחיל ב-"TRNA" | tRNA | רוב |
| מתחיל ב-"MIR" | ncRNA | רוב |

```
ניתוח סיומת "P" (מציין Pseudogene):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Symbol מסתיים ב-P → PSEUDO:     ~67% מהמקרים
Symbol מסתיים ב-P → סוג אחר:    ~33% מהמקרים
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**המלצה:** ✅ **שימושי לפיצ'רים, אך צריך לשקול אם רוצים לחזות מהרצף בלבד**

---

### 2.5 NucleotideSequence - **חיוני**

```
סטטיסטיקות:
- רשומות כוללות: 22,593
- רצפים ייחודיים: 21,884 (96.9%)
- רצפים כפולים: ~709 (3.1%)
```

**בעיות פוטנציאליות:**
- ~3% מהרצפים חוזרים על עצמם
- צריך לבדוק אם כפילויות הן בין train/test/validation (Data Leakage)

**המלצה:** ✅ **המשתנה העיקרי לסיווג**

---

## 3. מטריצת קורלציות | Correlation Matrix

```
                    NCBIGeneID  Symbol  Description  GeneType  GeneGroupMethod  Sequence
                    ─────────────────────────────────────────────────────────────────────
NCBIGeneID          │    -      │  0.0  │    0.0     │   0.0   │      0.0       │   0.0
Symbol              │   0.0     │   -   │   ~0.7     │  ~0.6   │     ~0.3       │  ~0.2
Description         │   0.0     │ ~0.7  │     -      │  ~0.8   │     ~0.4       │  ~0.1
GeneType            │   0.0     │ ~0.6  │   ~0.8     │    -    │     ~0.5       │    ?
GeneGroupMethod     │   0.0     │ ~0.3  │   ~0.4     │  ~0.5   │       -        │  ~0.1
Sequence            │   0.0     │ ~0.2  │   ~0.1     │    ?    │     ~0.1       │    -
                    ─────────────────────────────────────────────────────────────────────
```

**הערה:** הקורלציות הן הערכות מבוססות על הניתוח האיכותני

---

## 4. המלצות לעיבוד נתונים | Recommendations

### 4.1 אם המטרה: סיווג גנים מרצף DNA בלבד

```python
# משתנים לשימוש:
features = ['NucleotideSequence']
target = 'GeneType'

# משתנים להסרה:
drop_columns = ['NCBIGeneID', 'Symbol', 'Description', 'GeneGroupMethod']
```

### 4.2 אם המטרה: סיווג מבוסס כל המידע הזמין

```python
# משתנים לשימוש:
features = ['Symbol', 'NucleotideSequence']
target = 'GeneType'

# משתנים להסרה (מיותרים/זולגים):
drop_columns = ['NCBIGeneID', 'Description', 'GeneGroupMethod']
```

### 4.3 בדיקות נוספות מומלצות:

1. **בדיקת Data Leakage:**
   - האם יש רצפים זהים בין train/test/validation?
   - האם יש גנים מאותו משפחה בסטים שונים?

2. **Feature Engineering מומלץ:**
   ```python
   # מ-Symbol:
   - symbol_prefix (3-4 אותיות ראשונות)
   - ends_with_P (boolean)
   - has_numbers (boolean)
   
   # מ-Sequence:
   - sequence_length
   - gc_content (אחוז G+C)
   - nucleotide_frequencies
   ```

3. **טיפול בחוסר איזון:**
   - PSEUDO ו-BIOLOGICAL_REGION = ~62% מהנתונים
   - שקול SMOTE, undersampling, או class weights

---

## 5. סיכום | Summary

| משתנה | להשאיר? | הערות |
|-------|---------|-------|
| NCBIGeneID | ❌ לא | מזהה בלבד |
| Symbol | ⚠️ אופציונלי | שימושי אם רוצים פיצ'רים נוספים |
| Description | ❌ לא | רדונדנטי ל-GeneType |
| GeneType | ✅ כן | משתנה היעד |
| GeneGroupMethod | ❌ לא | שונות נמוכה + רדונדנטי |
| NucleotideSequence | ✅ כן | המשתנה העיקרי |

### משתנים מיותרים לגמרי:
1. **GeneGroupMethod** - 83% ערך אחד, רדונדנטי
2. **NCBIGeneID** - מזהה בלבד
3. **Description** - רדונדנטי ל-GeneType

---

*ניתוח זה בוצע על בסיס train.csv (22,593 רשומות)*

