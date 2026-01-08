import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Styling
sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ============================================
# ANALYSIS 1: STATE-WISE COVERAGE
# ============================================
print("Analysis 1: State-wise Coverage")
print("="*60)

df = pd.read_csv('data/aadhaar_enrollment.csv')

# State-wise count
state_count = df['state'].value_counts().sort_values(ascending=False)
print(f"\nTop 10 States:")
print(state_count.head(10))

# Visualization
fig, ax = plt.subplots(figsize=(12, 6))
state_count.head(15).plot(kind='barh', ax=ax, color='skyblue')
ax.set_title('Top 15 States by Aadhaar Enrollment', fontsize=14, fontweight='bold')
ax.set_xlabel('Number of Enrollments')
plt.tight_layout()
plt.savefig('visualizations/top_states.png', dpi=300)
plt.show()

# ============================================
# ANALYSIS 2: GENDER GAP ANALYSIS
# ============================================
print("\n" + "="*60)
print("Analysis 2: Gender-wise Analysis")
print("="*60)

gender_count = df['gender'].value_counts()
gender_pct = df['gender'].value_counts(normalize=True) * 100

print(f"\nGender Distribution:")
for gender, count in gender_count.items():
    pct = gender_pct[gender]
    print(f"{gender}: {count:,} ({pct:.1f}%)")

# State-wise gender breakdown
print("\nGender Distribution by Top 5 States:")
top_states = df['state'].value_counts().head(5).index
for state in top_states:
    state_data = df[df['state'] == state]
    male = len(state_data[state_data['gender'] == 'M'])
    female = len(state_data[state_data['gender'] == 'F'])
    total = len(state_data)
    male_pct = (male/total)*100
    female_pct = (female/total)*100
    print(f"{state}: M={male_pct:.1f}%, F={female_pct:.1f}%")

# ============================================
# ANALYSIS 3: AGE DISTRIBUTION
# ============================================
print("\n" + "="*60)
print("Analysis 3: Age Distribution")
print("="*60)

age_stats = df['age'].describe()
print(f"\nAge Statistics:")
print(age_stats)

# Age group breakdown
age_bins = [0, 18, 30, 45, 60, 100]
age_labels = ['0-17', '18-29', '30-44', '45-59', '60+']
df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels)

age_group_count = df['age_group'].value_counts().sort_index()
print(f"\nEnrollment by Age Group:")
print(age_group_count)

# Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Histogram
ax1.hist(df['age'], bins=30, color='green', alpha=0.7, edgecolor='black')
ax1.set_title('Age Distribution', fontsize=12, fontweight='bold')
ax1.set_xlabel('Age')
ax1.set_ylabel('Count')

# Age group bar chart
age_group_count.plot(kind='bar', ax=ax2, color='orange')
ax2.set_title('Enrollment by Age Group', fontsize=12, fontweight='bold')
ax2.set_xlabel('Age Group')
ax2.set_ylabel('Count')
ax2.tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.savefig('visualizations/age_analysis.png', dpi=300)
plt.show()

# ============================================
# ANALYSIS 4: RURAL VS URBAN (If you have area column)
# ============================================
if 'area_type' in df.columns:
    print("\n" + "="*60)
    print("Analysis 4: Rural vs Urban")
    print("="*60)
    
    area_count = df['area_type'].value_counts()
    area_pct = df['area_type'].value_counts(normalize=True) * 100
    
    print(f"\nArea Type Distribution:")
    for area, count in area_count.items():
        pct = area_pct[area]
        print(f"{area}: {count:,} ({pct:.1f}%)")

# ============================================
# ANALYSIS 5: KEY INSIGHTS SUMMARY
# ============================================
print("\n" + "="*60)
print("KEY INSIGHTS SUMMARY")
print("="*60)

total_enrollments = len(df)
unique_states = df['state'].nunique()
top_state = df['state'].value_counts().index[0]
top_state_count = df['state'].value_counts().values[0]
top_state_pct = (top_state_count / total_enrollments) * 100

print(f"\n✓ Total Enrollments: {total_enrollments:,}")
print(f"✓ Unique States: {unique_states}")
print(f"✓ Top State: {top_state} ({top_state_count:,} = {top_state_pct:.1f}%)")
print(f"✓ Coverage: {unique_states} states covered")
print(f"✓ Analysis Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}")

print("\n✓ All visualizations saved!")
print("  - visualizations/top_states.png")
print("  - visualizations/age_analysis.png")
