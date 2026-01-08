import pandas as pd
import glob
import os

print("="*70)
print("LOADING AADHAAR DATA FROM MULTIPLE FILES")
print("="*70)

# ============================================
# LOAD BIOMETRIC DATA
# ============================================
print("\n1. Loading Biometric Data...")
biometric_files = glob.glob('data/api_data_aadhar_biometric/**/*.csv', recursive=True)
print(f"   Found {len(biometric_files)} biometric files")

biometric_dfs = []
for file in sorted(biometric_files):
    df = pd.read_csv(file)
    biometric_dfs.append(df)
    print(f"   ✓ Loaded {os.path.basename(file)}: {len(df)} rows")

biometric_data = pd.concat(biometric_dfs, ignore_index=True)
print(f"\n   Total Biometric Records: {len(biometric_data):,}")
print(f"   Columns: {biometric_data.columns.tolist()}")

# ============================================
# LOAD DEMOGRAPHIC DATA
# ============================================
print("\n2. Loading Demographic Data...")
demographic_files = glob.glob('data/api_data_aadhar_demographic/**/*.csv', recursive=True)
print(f"   Found {len(demographic_files)} demographic files")

demographic_dfs = []
for file in sorted(demographic_files):
    df = pd.read_csv(file)
    demographic_dfs.append(df)
    print(f"   ✓ Loaded {os.path.basename(file)}: {len(df)} rows")

demographic_data = pd.concat(demographic_dfs, ignore_index=True)
print(f"\n   Total Demographic Records: {len(demographic_data):,}")
print(f"   Columns: {demographic_data.columns.tolist()}")

# ============================================
# LOAD ENROLMENT DATA
# ============================================
print("\n3. Loading Enrolment Data...")
enrolment_files = glob.glob('data/api_data_aadhar_enrolment/**/*.csv', recursive=True)
print(f"   Found {len(enrolment_files)} enrolment files")

enrolment_dfs = []
for file in sorted(enrolment_files):
    df = pd.read_csv(file)
    enrolment_dfs.append(df)
    print(f"   ✓ Loaded {os.path.basename(file)}: {len(df)} rows")

enrolment_data = pd.concat(enrolment_dfs, ignore_index=True)
print(f"\n   Total Enrolment Records: {len(enrolment_data):,}")
print(f"   Columns: {enrolment_data.columns.tolist()}")

# ============================================
# SAVE COMBINED DATA
# ============================================
print("\n" + "="*70)
print("SAVING COMBINED DATA")
print("="*70)

biometric_data.to_csv('data/combined_biometric_data.csv', index=False)
print("✓ Saved: data/combined_biometric_data.csv")

demographic_data.to_csv('data/combined_demographic_data.csv', index=False)
print("✓ Saved: data/combined_demographic_data.csv")

enrolment_data.to_csv('data/combined_enrolment_data.csv', index=False)
print("✓ Saved: data/combined_enrolment_data.csv")

# ============================================
# QUICK PREVIEW
# ============================================
print("\n" + "="*70)
print("QUICK DATA PREVIEW")
print("="*70)

print("\n--- BIOMETRIC DATA (First 5 rows) ---")
print(biometric_data.head())

print("\n--- DEMOGRAPHIC DATA (First 5 rows) ---")
print(demographic_data.head())

print("\n--- ENROLMENT DATA (First 5 rows) ---")
print(enrolment_data.head())

print("\n" + "="*70)
print("DATA LOADING COMPLETE!")
print("="*70)
print("\n✓ All data combined and saved successfully!")
print("✓ You can now run analysis.py or deep_analysis.py")
