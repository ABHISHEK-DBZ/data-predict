import pandas as pd

# Data load karo
df = pd.read_csv('data/aadhaar_enrollment.csv')

print("BEFORE CLEANING:")
print(f"Total rows: {len(df)}")
print(f"Null values:\n{df.isnull().sum()}")

# ============================================
# CLEANING STEPS
# ============================================

# 1. Null values handle karo
df = df.dropna(subset=['state', 'gender'])  # Ye columns important hain

# 2. Age outliers remove karo (impossible ages)
if 'age' in df.columns:
    df = df[(df['age'] >= 0) & (df['age'] <= 120)]

# 3. Duplicate rows remove karo
df = df.drop_duplicates()

# 4. State names standardize karo (uppercase)
if 'state' in df.columns:
    df['state'] = df['state'].str.upper().str.strip()

# 5. Gender standardize karo
if 'gender' in df.columns:
    df['gender'] = df['gender'].map({'M': 'Male', 'F': 'Female', 'O': 'Other'})
    df = df.dropna(subset=['gender'])  # Unknown gender remove karo

print("\nAFTER CLEANING:")
print(f"Total rows: {len(df)}")
print(f"Null values:\n{df.isnull().sum()}")

# Save clean data
df.to_csv('data/aadhaar_enrollment_clean.csv', index=False)
print("\n✓ Clean data saved as 'data/aadhaar_enrollment_clean.csv'")
