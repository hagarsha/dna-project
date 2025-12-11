# דוח מסכם - נתוני DNA
# DNA Dataset Summary Report

---

## 1. סקירת הנתונים | Dataset Overview

| קובץ | מספר שורות (כולל כותרת) | מספר דגימות |
|------|-------------------------|-------------|
| train.csv | 22,594 | **22,593** |
| test.csv | 8,327 | **8,326** |
| validation.csv | 4,578 | **4,577** |
| **סה"כ** | **35,499** | **35,496** |

---

## 2. משתנים (עמודות) | Variables (Columns)

הנתונים כוללים **6 משתנים**:

| # | שם המשתנה | תיאור | סוג |
|---|-----------|-------|-----|
| 1 | **NCBIGeneID** | מזהה גן ייחודי מ-NCBI | מספרי (Numeric) |
| 2 | **Symbol** | סימול הגן | טקסט (Text) |
| 3 | **Description** | תיאור מילולי של הגן | טקסט (Text) |
| 4 | **GeneType** | סוג הגן - **התיוג הראשי** | קטגורי (Categorical) |
| 5 | **GeneGroupMethod** | שיטת קיבוץ הגנים | קטגורי (Categorical) |
| 6 | **NucleotideSequence** | רצף הנוקלאוטידים (DNA) | רצף (Sequence) |

---

## 3. ניתוח התיוגים (GeneType) | Label Analysis

### סוגי הגנים הראשיים:

| סוג הגן | כמות | אחוז | תיאור |
|---------|------|------|-------|
| **PSEUDO** | ~11,019 | ~31.0% | פסאודוגנים - גנים לא פעילים |
| **BIOLOGICAL_REGION** | ~10,955 | ~30.9% | אזורים ביולוגיים רגולטוריים |
| **ncRNA** | ~3,898 | ~11.0% | RNA לא מקודד (non-coding RNA) |
| **snoRNA** | ~977 | ~2.8% | Small nucleolar RNA |
| **PROTEIN_CODING** | ~792 | ~2.2% | גנים מקודדים לחלבון |
| **tRNA** | ~708 | ~2.0% | Transfer RNA |
| **OTHER** | ~587 | ~1.7% | סוגים אחרים |
| **rRNA** | ~333 | ~0.9% | Ribosomal RNA |
| **snRNA** | ~162 | ~0.5% | Small nuclear RNA |
| **scRNA** | ~4 | ~0.01% | Small cytoplasmic RNA |

### התפלגות התיוגים (ויזואלי):

```
PSEUDO            ████████████████████████████████ 31.0%
BIOLOGICAL_REGION ███████████████████████████████▉ 30.9%
ncRNA             ███████████▏                     11.0%
snoRNA            ██▉                               2.8%
PROTEIN_CODING    ██▎                               2.2%
tRNA              ██                                2.0%
OTHER             █▊                                1.7%
rRNA              █                                 0.9%
snRNA             ▌                                 0.5%
scRNA             ▏                                 0.01%
```

---

## 4. GeneGroupMethod | שיטת הקיבוץ

| שיטה | כמות | אחוז |
|------|------|------|
| **NCBI Ortholog** | ~29,435 | ~82.9% |
| **pseudogene** | ~2,490 | ~7.0% |
| **אחר** | ~3,574 | ~10.1% |

---

## 5. דוגמאות מהנתונים | Sample Data

### דוגמה 1 - פסאודוגן (PSEUDO):
```
NCBIGeneID: 106481178
Symbol: RNU4-21P
Description: RNA, U4 small nuclear 21, pseudogene
GeneType: PSEUDO
Sequence: AGCTTAGCACAGTGGCAGTATCATAGGCAGTGAGGTTTATCCGAGGCGTGATTATTGCCAATTGAAAACTTTTCTCGATAC...
```

### דוגמה 2 - אזור ביולוגי (BIOLOGICAL_REGION):
```
NCBIGeneID: 123477792
Symbol: LOC123477792
Description: Sharpr-MPRA regulatory region 12926
GeneType: BIOLOGICAL_REGION
Sequence: CTGGAGCGGCCACGATGTGAACTGTCACCGGCCACTGCTGCTCCGACTCCCTGGAAGCACACAGGGTGATTAAAGGAGGCG...
```

### דוגמה 3 - גן מקודד לחלבון (PROTEIN_CODING):
```
NCBIGeneID: 8335
Symbol: H2AC4
Description: H2A clustered histone 4
GeneType: PROTEIN_CODING
Sequence: GTAGTTTCATTACATTTTCTTGTGGCGATTTTCCCTTATCAGAAGTAGTTATGTCTGGTCGCGGCAAACAAGGCGGTAAAG...
```

### דוגמה 4 - microRNA (ncRNA):
```
NCBIGeneID: 100500828
Symbol: MIR3619
Description: microRNA 3619
GeneType: ncRNA
Sequence: ACGGCATCTTTGCACTCAGCAGGCAGGCTGGTGCAGCCCGTGGTGGGGGACCATCCTGCCTGCTGTGGGGTAAGGACGGCTGT
```

---

## 6. מבנה רצפי ה-DNA | DNA Sequence Structure

- **פורמט הרצף**: רצפים מוקפים בסימני `<` ו-`>`
- **נוקלאוטידים**: A (אדנין), T (תימין), G (גואנין), C (ציטוזין)
- **אורך הרצפים**: משתנה - מ-28 נוקלאוטידים ועד מאות/אלפי נוקלאוטידים

---

## 7. סיכום | Summary

### נקודות עיקריות:

✅ **סה"כ ~35,500 דגימות** מחולקות ל-3 קבצים (train, test, validation)

✅ **10 סוגי גנים (תיוגים)** - כאשר PSEUDO ו-BIOLOGICAL_REGION מהווים יחד ~62% מהנתונים

✅ **6 משתנים** לכל דגימה - כולל מזהה, סימול, תיאור, סוג, שיטה ורצף DNA

✅ **רצפי DNA** באורכים שונים - מתאימים לניתוח ולימוד מכונה

### חלוקת הנתונים:
- **Train**: ~64% (22,593 דגימות)
- **Test**: ~23% (8,326 דגימות)  
- **Validation**: ~13% (4,577 דגימות)

### המלצות לעבודה עם הנתונים:

1. **סיווג (Classification)**: ניתן להשתמש ב-GeneType כמשתנה התיוג לסיווג רצפי DNA
2. **חוסר איזון (Imbalanced)**: יש לשים לב לחוסר איזון בין הקטגוריות
3. **עיבוד רצפים**: רצפי ה-DNA מתאימים לשימוש במודלים כמו CNN, RNN, או Transformers

---

*הדוח נוצר אוטומטית מתוך ניתוח קבצי הנתונים*
*Report generated automatically from data analysis*

