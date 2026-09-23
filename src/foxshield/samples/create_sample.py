import pandas as pd
import os

# Create test_files folder
os.makedirs("test_files", exist_ok=True)

print("🦊 Creating FoxShield test files...\n")

# ============================================================================
# TEST 1: LEAK SCENARIO (CSV + Excel)
# ============================================================================
print("📄 Creating LEAK test files...")

leak_data = {
    "Employee_Name": ["Ramesh Kumar", "Priya Sharma", "Amit Patel", "Sunita Desai", "Vikram Singh"],
    "Employee_ID": ["EMP001", "EMP002", "EMP003", "EMP004", "EMP005"],
    "Department": ["HR", "Finance", "IT", "Admin", "Legal"],
    "Bank_Account_Number": ["1234567890123456", "9876543210987654", "5678901234567890", "3456789012345678", "2345678901234567"],
    "Password": ["Secret@123", "Priya#2024", "Amit$ecure", "Sunita@2024", "Vikram!Legal"],
    "Phone_Number": ["+91-9876543210", "+91-8765432109", "+91-7654321098", "+91-6543210987", "+91-5432109876"],
    "Email": ["ramesh.kumar@company.internal", "priya.sharma@company.internal", "amit.patel@company.internal", "sunita.desai@company.internal", "vikram.singh@company.internal"],
    "Notes": ["CONFIDENTIAL - Internal Use Only", "Draft - Not for Distribution", "Restricted Access", "Private - Do Not Share", "SENSITIVE - Proprietary"]
}

df_leak = pd.DataFrame(leak_data)
df_leak.to_csv("test_files/test_leak.csv", index=False)
df_leak.to_excel("test_files/test_leak.xlsx", index=False)
print("  ✅ test_leak.csv")
print("  ✅ test_leak.xlsx")

# ============================================================================
# TEST 2: SAFE RTI SCENARIO (CSV + Excel)
# ============================================================================
print("\n📄 Creating SAFE (RTI) test files...")

rti_data = {
    "Official_Name": ["Ramesh Kumar", "Priya Sharma", "Amit Patel", "Sunita Desai", "Vikram Singh"],
    "Designation": ["Deputy Commissioner", "Assistant Engineer", "Section Officer", "Deputy Director", "Public Information Officer"],
    "Department": ["Municipal Corporation", "Public Works Dept", "Gazette Notification", "Audit Department", "RTI Cell"],
    "Monthly_Salary": [75000, 65000, 55000, 80000, 70000],
    "RTI_Reference": ["RTI/2024/MUN/045", "RTI/2024/PWD/123", "GAZ/2024/SEC/789", "AUDIT/2024/DD/456", "RTI/2024/PIO/321"],
    "Publication_Date": ["2024-01-15", "2024-02-20", "2024-03-10", "2024-04-05", "2024-05-12"],
    "Disclosure_Type": ["Public Disclosure - RTI Mandated", "Transparency Report", "Official Gazette", "Public Audit Report", "Mandated Disclosure"]
}

df_rti = pd.DataFrame(rti_data)
df_rti.to_csv("test_files/test_rti.csv", index=False)
df_rti.to_excel("test_files/test_rti.xlsx", index=False)
print("  ✅ test_rti.csv")
print("  ✅ test_rti.xlsx")

# ============================================================================
# TEST 3: EDGE CASE (CSV + Excel)
# ============================================================================
print("\n⚠️ Creating EDGE CASE test files...")

edge_data = {
    "Document_Section": ["Main_Document", "Main_Document", "Appendix_A", "Appendix_A", "Appendix_B", "Appendix_B"],
    "Content_Type": ["RTI_Response", "RTI_Response", "Internal_Notes", "Internal_Notes", "Raw_Data", "Raw_Data"],
    "Name": ["Ramesh Kumar", "Priya Sharma", "Amit Patel", "Sunita Desai", "Vikram Singh", "Rajesh Kumar"],
    "Information": ["Public Official Salary: 75000", "Department Budget Allocation", "Employee ID: EMP789", "Personal Phone: +91-9876543210", "Bank Account: 1234567890", "Password: Secret123"],
    "Classification": ["Public - RTI Mandated", "Transparency Report", "Confidential Draft", "Private - Restricted", "Internal Use Only", "Not for Distribution"]
}

df_edge = pd.DataFrame(edge_data)
df_edge.to_csv("test_files/test_edge.csv", index=False)
df_edge.to_excel("test_files/test_edge.xlsx", index=False)
print("  ✅ test_edge.csv")
print("  ✅ test_edge.xlsx")

# ============================================================================
# TEST 4: PDF FILES (Written line by line to avoid syntax errors)
# ============================================================================
print("\n📄 Creating PDF text files (convert to PDF manually)...")

# --- LEAK PDF ---
leak_lines = [
    "CONFIDENTIAL - INTERNAL USE ONLY",
    "Employee Database - Q1 2024",
    "Draft Version - Not for Distribution",
    "",
    "Employee Records:",
    "-------------------",
    "Name: Ramesh Kumar",
    "Employee ID: EMP001",
    "Department: Human Resources",
    "Personal Phone: +91-9876543210",
    "Email: ramesh.kumar@internal.company.com",
    "",
    "Name: Priya Sharma",
    "Employee ID: EMP002",
    "Department: Finance",
    "Personal Phone: +91-8765432109",
    "Email: priya.sharma@internal.company.com",
    "",
    "Name: Amit Patel",
    "Employee ID: EMP003",
    "Department: IT",
    "Personal Phone: +91-7654321098",
    "Email: amit.patel@internal.company.com",
    "",
    "SENSITIVE - PROPRIETARY INFORMATION",
    "DO NOT DISTRIBUTE"
]

with open("test_files/leak_document.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(leak_lines))
print("  ✅ leak_document.txt")

# --- RTI PDF ---
rti_lines = [
    "RIGHT TO INFORMATION ACT, 2005",
    "Public Disclosure - Section 4",
    "",
    "RTI Reference: RTI/2024/MUN/045",
    "Date: 15 January 2024",
    "Subject: Public Official Salary Disclosure",
    "",
    "In compliance with the Right to Information Act and transparency",
    "mandates, the following information is published for public interest:",
    "",
    "Public Officials Salary Information (Gazette Notification):",
    "-----------------------------------------------------------",
    "",
    "Name: Ramesh Kumar",
    "Designation: Deputy Commissioner",
    "Department: Municipal Corporation",
    "Monthly Salary: 75000",
    "Annual Salary: 900000",
    "Appointment: Gazette Notification No. 45/2024",
    "",
    "Name: Priya Sharma",
    "Designation: Assistant Engineer",
    "Department: Public Works Department",
    "Monthly Salary: 65000",
    "Annual Salary: 780000",
    "Appointment: Public Record - Transparency Report",
    "",
    "Name: Amit Patel",
    "Designation: Section Officer",
    "Department: Administration",
    "Monthly Salary: 55000",
    "Annual Salary: 660000",
    "Appointment: Official Gazette",
    "",
    "Name: Sunita Desai",
    "Designation: Deputy Director",
    "Department: Audit Department",
    "Monthly Salary: 80000",
    "Annual Salary: 960000",
    "Appointment: Public Audit Report",
    "",
    "Name: Vikram Singh",
    "Designation: Public Information Officer",
    "Department: RTI Cell",
    "Monthly Salary: 70000",
    "Annual Salary: 840000",
    "Appointment: Mandated Disclosure",
    "",
    "This information is mandated for public disclosure under Section 4",
    "of the RTI Act and is published in the public interest.",
    "",
    "Public Information Officer",
    "Municipal Corporation"
]

with open("test_files/rti_response.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(rti_lines))
print("  ✅ rti_response.txt")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("✅ ALL TEST FILES CREATED SUCCESSFULLY!")
print("=" * 60)
print("\n📁 Files location: test_files/")
print("\n📋 Expected Results:")
print("  🔴 test_leak.csv/xlsx    → CRITICAL DATA LEAK")
print("  🟢 test_rti.csv/xlsx     → LEGITIMATE RTI DISCLOSURE")
print("  🟡 test_edge.csv/xlsx    → REQUIRES MANUAL REVIEW")
print("\n📄 For PDFs:")
print("  1. Open .txt files in Word/Google Docs")
print("  2. Save As → PDF")
print("  3. Upload to FoxShield")
print("\n🦊 Happy Testing!")