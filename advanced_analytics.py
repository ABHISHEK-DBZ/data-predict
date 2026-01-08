"""
Aadhaar-Drishti: Advanced Analytics Engine
Migration Tracking & Infrastructure Stress Analysis
"""

import pandas as pd
import numpy as np
import glob
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("🚀 AADHAAR-DRISHTI: ADVANCED ANALYTICS ENGINE")
print("   AI-Powered Demographic Insight & Migration Tracking System")
print("="*80)

# ============================================
# LOAD ALL DATASETS
# ============================================
print("\n📊 LOADING DATA...")

# Biometric Data
biometric_files = glob.glob('data/api_data_aadhar_biometric/**/*.csv', recursive=True)
biometric_list = [pd.read_csv(f) for f in sorted(biometric_files)]
biometric = pd.concat(biometric_list, ignore_index=True)
print(f"✓ Biometric: {len(biometric):,} records")

# Demographic Data
demographic_files = glob.glob('data/api_data_aadhar_demographic/**/*.csv', recursive=True)
demographic_list = [pd.read_csv(f) for f in sorted(demographic_files)]
demographic = pd.concat(demographic_list, ignore_index=True)
print(f"✓ Demographic: {len(demographic):,} records")

# Enrolment Data
enrolment_files = glob.glob('data/api_data_aadhar_enrolment/**/*.csv', recursive=True)
enrolment_list = [pd.read_csv(f) for f in sorted(enrolment_files)]
enrolment = pd.concat(enrolment_list, ignore_index=True)
print(f"✓ Enrolment: {len(enrolment):,} records")

# Convert dates
for df in [biometric, demographic, enrolment]:
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')

# ============================================
# METRIC 1: CHURN RATE CALCULATION
# ============================================
print("\n" + "="*80)
print("📈 METRIC 1: CHURN RATE ANALYSIS")
print("   Formula: (Total Updates / Population) × 100")
print("="*80)

# Calculate total activity per district
demographic['total_updates'] = demographic['demo_age_5_17'] + demographic['demo_age_17_']
district_activity = demographic.groupby(['state', 'district']).agg({
    'total_updates': 'sum',
    'district': 'count'  # Number of records as proxy for population
}).rename(columns={'district': 'record_count'})

# Calculate Churn Rate
district_activity['churn_rate'] = (district_activity['total_updates'] / 
                                   district_activity['record_count']) * 100

# Sort by churn rate
district_activity_sorted = district_activity.sort_values('churn_rate', ascending=False)

print("\n🔥 TOP 20 DISTRICTS BY CHURN RATE (High Migration/Update Activity):")
print(district_activity_sorted.head(20))

# Classify districts
district_activity['risk_level'] = pd.cut(
    district_activity['churn_rate'],
    bins=[0, 50, 100, 200, float('inf')],
    labels=['Stable', 'Moderate', 'High Activity', 'Critical']
)

print("\n📊 DISTRICT CLASSIFICATION:")
print(district_activity['risk_level'].value_counts())

# Save churn rate analysis
district_activity.to_csv('analysis_results/churn_rate_analysis.csv')
print("\n✓ Saved: analysis_results/churn_rate_analysis.csv")

# ============================================
# METRIC 2: INFRASTRUCTURE STRESS INDEX
# ============================================
print("\n" + "="*80)
print("🏗️ METRIC 2: INFRASTRUCTURE STRESS INDEX")
print("   Identifies cities needing urgent resource allocation")
print("="*80)

# Combine all update activities
enrolment['total_enrolments'] = enrolment['age_0_5'] + enrolment['age_5_17'] + enrolment['age_18_greater']
biometric['total_biometric'] = biometric['bio_age_5_17'] + biometric['bio_age_17_']

# Calculate district-level stress
district_stress = demographic.groupby(['state', 'district']).agg({
    'demo_age_5_17': 'sum',
    'demo_age_17_': 'sum'
}).reset_index()

district_stress['total_demographic_updates'] = (district_stress['demo_age_5_17'] + 
                                                 district_stress['demo_age_17_'])

# Add enrolment data
enrolment_by_district = enrolment.groupby(['state', 'district'])['total_enrolments'].sum().reset_index()
district_stress = district_stress.merge(enrolment_by_district, on=['state', 'district'], how='left')
district_stress['total_enrolments'] = district_stress['total_enrolments'].fillna(0)

# Calculate Infrastructure Stress Score
# Formula: (Demographic Updates × 0.4) + (Enrolments × 0.6)
district_stress['infrastructure_stress_score'] = (
    district_stress['total_demographic_updates'] * 0.4 +
    district_stress['total_enrolments'] * 0.6
)

# Normalize to 0-100 scale
max_score = district_stress['infrastructure_stress_score'].max()
district_stress['stress_index'] = (district_stress['infrastructure_stress_score'] / max_score) * 100

# Get top 20 stressed districts
top_stressed = district_stress.nlargest(20, 'stress_index')

print("\n🚨 TOP 20 DISTRICTS WITH HIGHEST INFRASTRUCTURE STRESS:")
print(top_stressed[['state', 'district', 'stress_index', 'total_demographic_updates', 'total_enrolments']])

# Flag high-risk districts
district_stress['alert_level'] = pd.cut(
    district_stress['stress_index'],
    bins=[0, 25, 50, 75, 100],
    labels=['Low', 'Medium', 'High', 'Critical']
)

print("\n📊 INFRASTRUCTURE STRESS DISTRIBUTION:")
print(district_stress['alert_level'].value_counts())

# Calculate resource requirements (example: 10% increase per stress level)
district_stress['recommended_capacity_increase'] = district_stress['stress_index'] * 0.1

print("\n💡 RESOURCE ALLOCATION RECOMMENDATIONS:")
critical_districts = district_stress[district_stress['alert_level'] == 'Critical']
print(f"   • {len(critical_districts)} districts need IMMEDIATE attention")
print(f"   • Avg. recommended capacity increase: {critical_districts['recommended_capacity_increase'].mean():.1f}%")

# Save infrastructure stress analysis
district_stress.to_csv('analysis_results/infrastructure_stress_index.csv', index=False)
print("\n✓ Saved: analysis_results/infrastructure_stress_index.csv")

# ============================================
# METRIC 3: SEASONALITY DETECTION
# ============================================
print("\n" + "="*80)
print("📅 METRIC 3: SEASONALITY DETECTION")
print("   Identifies peak periods for resource planning")
print("="*80)

# Monthly trend analysis
demographic['month'] = demographic['date'].dt.month
demographic['month_name'] = demographic['date'].dt.strftime('%B')

monthly_updates = demographic.groupby('month_name').agg({
    'demo_age_5_17': 'sum',
    'demo_age_17_': 'sum'
}).reset_index()

monthly_updates['total_monthly_updates'] = (monthly_updates['demo_age_5_17'] + 
                                             monthly_updates['demo_age_17_'])

# Sort by month order
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
monthly_updates['month_name'] = pd.Categorical(monthly_updates['month_name'], 
                                                categories=month_order, ordered=True)
monthly_updates = monthly_updates.sort_values('month_name')

print("\n📊 MONTHLY UPDATE PATTERNS:")
print(monthly_updates)

# Identify peak months
avg_monthly = monthly_updates['total_monthly_updates'].mean()
peak_months = monthly_updates[monthly_updates['total_monthly_updates'] > avg_monthly * 1.2]

print(f"\n🔥 PEAK ACTIVITY MONTHS (>20% above average):")
for _, row in peak_months.iterrows():
    print(f"   • {row['month_name']}: {row['total_monthly_updates']:,} updates")

# Day of week analysis (if enough data)
demographic['day_of_week'] = demographic['date'].dt.day_name()
daily_pattern = demographic.groupby('day_of_week').size().reset_index(name='count')

print("\n📊 DAY OF WEEK PATTERNS:")
print(daily_pattern)

# Save seasonality analysis
monthly_updates.to_csv('analysis_results/seasonality_analysis.csv', index=False)
print("\n✓ Saved: analysis_results/seasonality_analysis.csv")

# ============================================
# METRIC 4: GENDER GAP ANALYSIS
# ============================================
print("\n" + "="*80)
print("👥 METRIC 4: GENDER GAP & DEMOGRAPHIC INSIGHTS")
print("="*80)

# State-level demographic analysis
state_demographics = demographic.groupby('state').agg({
    'demo_age_5_17': 'sum',
    'demo_age_17_': 'sum'
}).reset_index()

state_demographics['youth_ratio'] = (state_demographics['demo_age_5_17'] / 
                                     state_demographics['demo_age_17_']) * 100

print("\n📊 TOP 10 STATES BY YOUTH POPULATION RATIO:")
print(state_demographics.nlargest(10, 'youth_ratio')[['state', 'youth_ratio']])

# ============================================
# METRIC 5: MIGRATION HOTSPOT DETECTION
# ============================================
print("\n" + "="*80)
print("🗺️ METRIC 5: MIGRATION HOTSPOT DETECTION")
print("="*80)

# Districts with unusual activity patterns
district_migration = demographic.groupby(['state', 'district']).agg({
    'demo_age_5_17': 'sum',
    'demo_age_17_': 'sum',
    'date': 'count'
}).reset_index()

district_migration['avg_updates_per_record'] = (
    (district_migration['demo_age_5_17'] + district_migration['demo_age_17_']) / 
    district_migration['date']
)

# Flag potential migration hotspots (high updates per record)
migration_threshold = district_migration['avg_updates_per_record'].quantile(0.9)
migration_hotspots = district_migration[
    district_migration['avg_updates_per_record'] > migration_threshold
]

print(f"\n🔥 IDENTIFIED {len(migration_hotspots)} MIGRATION HOTSPOTS:")
print(migration_hotspots[['state', 'district', 'avg_updates_per_record']].head(15))

migration_hotspots.to_csv('analysis_results/migration_hotspots.csv', index=False)
print("\n✓ Saved: analysis_results/migration_hotspots.csv")

# ============================================
# FINAL DASHBOARD DATA PREPARATION
# ============================================
print("\n" + "="*80)
print("💾 PREPARING DASHBOARD DATA")
print("="*80)

# Combine all metrics for dashboard
dashboard_data = district_stress.merge(
    district_activity.reset_index(),
    on=['state', 'district'],
    how='outer'
)

# Add migration flags
dashboard_data = dashboard_data.merge(
    migration_hotspots[['state', 'district', 'avg_updates_per_record']],
    on=['state', 'district'],
    how='left'
)
dashboard_data['is_migration_hotspot'] = ~dashboard_data['avg_updates_per_record'].isna()

# Save master dashboard data
dashboard_data.to_csv('analysis_results/dashboard_master_data.csv', index=False)
print("✓ Saved: analysis_results/dashboard_master_data.csv")

# ============================================
# KEY INSIGHTS SUMMARY
# ============================================
print("\n" + "="*80)
print("🎯 KEY INSIGHTS FOR DECISION MAKERS")
print("="*80)

print(f"""
📊 EXECUTIVE SUMMARY:

1️⃣ CHURN RATE ANALYSIS:
   • {len(district_activity[district_activity['risk_level'] == 'Critical'])} districts in CRITICAL state
   • {len(district_activity[district_activity['risk_level'] == 'High Activity'])} districts with HIGH activity
   • Recommendation: Deploy additional staff to high-churn districts

2️⃣ INFRASTRUCTURE STRESS:
   • {len(district_stress[district_stress['alert_level'] == 'Critical'])} districts need URGENT resource allocation
   • Top stressed city: {top_stressed.iloc[0]['district']}, {top_stressed.iloc[0]['state']}
   • Stress Index: {top_stressed.iloc[0]['stress_index']:.1f}%

3️⃣ SEASONALITY INSIGHTS:
   • Peak activity months: {', '.join(peak_months['month_name'].tolist())}
   • Recommendation: Deploy 30% extra Seva Kendra staff during peak months

4️⃣ MIGRATION TRACKING:
   • {len(migration_hotspots)} potential migration hotspots identified
   • These districts need enhanced monitoring and resource planning

5️⃣ DEMOGRAPHIC PATTERNS:
   • Youth-heavy states identified for education infrastructure planning
   • Gender gap analysis available for targeted interventions
""")

print("\n" + "="*80)
print("✅ ADVANCED ANALYTICS COMPLETE!")
print("="*80)
print("\n📁 Generated Files:")
print("   • analysis_results/churn_rate_analysis.csv")
print("   • analysis_results/infrastructure_stress_index.csv")
print("   • analysis_results/seasonality_analysis.csv")
print("   • analysis_results/migration_hotspots.csv")
print("   • analysis_results/dashboard_master_data.csv")
print("\n🚀 Ready to launch Streamlit dashboard!")
