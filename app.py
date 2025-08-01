import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import base64
import numpy as np  # Added here for NaN/infinite checks


# PAGE CONFIGURATION


st.set_page_config(page_title="Telangana Minorities Residential Educational Institutions Society", layout="wide")


# Custom CSS for UI
st.markdown("""
    <style>
    .big-font {font-size:20px !important; font-weight:600;}
    .kpi-box {background-color:#f9f9f9; padding:15px; border-radius:10px; text-align:center; border: 1px solid #ddd;}
    </style>
""", unsafe_allow_html=True)


# DATA UPLOAD


st.title("Telangana Minorities Residential Educational Institutions Society Analysis Dashboard")
uploaded_file = st.file_uploader("Upload your dataset (Excel or CSV)", type=["xlsx", "csv"])


if uploaded_file:
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)


    st.success("Dataset uploaded successfully!")
    # After uploading dataset successfully:


    if uploaded_file:
        ...
        st.session_state["uploaded_df"] = df  # Save dataset globally for other pages


    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df.fillna(0, inplace=True)


    # DYNAMIC COLUMN DETECTION


    def find_column(keyword):
        for col in df.columns:
            if keyword in col:
                return col
        return None


    columns = {
        "v_minority": {
            "sanctioned": find_column("vth_class_minority_sanction"),
            "admitted": find_column("vth_class_minority_admitted"),
            "vacancy": find_column("vth_class_minority_vacancies"),
            "attendance": find_column("total_school_attendance"),
        },
        "v_non_minority": {
            "sanctioned": find_column("vth_class_non_minority_sanction"),
            "admitted": find_column("vth_class_non_minority_admitted"),
            "vacancy": find_column("vth_class_non_minority_vacancies"),
            "attendance": find_column("total_school_attendance"),
        },
        "inter_minority": {
            "sanctioned": find_column("1st_year_minority_sanction"),
            "admitted": find_column("1st_year_minority_admitted"),
            "vacancy": find_column("1st_year_minority_vacancies"),
            "attendance": find_column("total_intermediate_attendance"),
        },
        "inter_non_minority": {
            "sanctioned": find_column("1st_year_non_minority_sanction"),
            "admitted": find_column("1st_year_non_minority_admitted"),
            "vacancy": find_column("1st_year_non_minority_vacancies"),
            "attendance": find_column("total_intermediate_attendance"),
        },
        "absentees": find_column("total_absentees"),
    }


    # FILTERS


    st.sidebar.header("Filters")
    level_filter = st.sidebar.radio("Select Level", ["V (School)", "Inter 1st Year"])
    category_filter = st.sidebar.radio("Select Category", ["Minority", "Non-Minority"])
    districts = st.sidebar.multiselect("Select District(s)", options=df["district"].unique(), default=df["district"].unique())
    search_college = st.sidebar.text_input("Search College Name (Optional)")


    df = df[df["district"].isin(districts)]
    if search_college:
        df = df[df["college_name"].str.contains(search_college, case=False, na=False)]


    # Map columns dynamically
    if level_filter == "V (School)":
        key = "v_minority" if category_filter == "Minority" else "v_non_minority"
    else:
        key = "inter_minority" if category_filter == "Minority" else "inter_non_minority"


    sanctioned_col = columns[key]["sanctioned"]
    admitted_col = columns[key]["admitted"]
    vacant_col = columns[key]["vacancy"]
    attendance_col = columns[key]["attendance"]
    absentees_col = columns["absentees"]


    # KPI CALCULATIONS


    total_sanctioned = df[sanctioned_col].sum()
    total_admitted = df[admitted_col].sum()
    total_vacant = df[vacant_col].sum()
    total_attendance = df[attendance_col].sum()
    total_absentees = df[absentees_col].sum()
    attendance_pct = round((total_attendance / (total_attendance + total_absentees)) * 100, 2) if (total_attendance + total_absentees) > 0 else 0


    # KPI DISPLAY
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.markdown(f"<div class='kpi-box'>🏫 <br><span class='big-font'>{total_sanctioned:,}</span><br>Total Sanctioned</div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='kpi-box'>🎓 <br><span class='big-font'>{total_admitted:,}</span><br>Total Admitted</div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='kpi-box'>📌 <br><span class='big-font'>{total_vacant:,}</span><br>Total Vacant</div>", unsafe_allow_html=True)
    col4.markdown(f"<div class='kpi-box'>✅ <br><span class='big-font'>{total_attendance:,}</span><br>Total Attendance</div>", unsafe_allow_html=True)
    col5.markdown(f"<div class='kpi-box'>❌ <br><span class='big-font'>{total_absentees:,}</span><br>Total Absentees</div>", unsafe_allow_html=True)
    col6.markdown(f"<div class='kpi-box'>📈 <br><span class='big-font'>{attendance_pct}%</span><br>Attendance %</div>", unsafe_allow_html=True)


    st.markdown("---")


    # VISUALIZATIONS
    df["admission_rate"] = (df[admitted_col] / df[sanctioned_col]) * 100
    df["vacancy_rate"] = (df[vacant_col] / df[sanctioned_col]) * 100
    df["attendance_%"] = (df[attendance_col] / (df[attendance_col] + df[absentees_col])) * 100

    # Clean data to remove NaN or infinite admission_rate values before plotting
    df_clean = df[df["admission_rate"].notna() & np.isfinite(df["admission_rate"])]

    # 1. Vacancy Rate vs Admission Rate (Bubble)
    st.plotly_chart(px.scatter(
        df_clean, 
        x="admission_rate", 
        y="vacancy_rate", 
        size="admission_rate",
        color=attendance_col, 
        hover_name="college_name",
        title="Vacancy Rate vs Admission Rate"
    ), use_container_width=True)


    # 2. Attendance Impact on Vacancies
    st.plotly_chart(px.scatter(df, x=attendance_col, y="vacancy_rate", title="Attendance Impact on Vacancy Rate", trendline="ols"), use_container_width=True)


    # 3. Top 10 Districts by Absenteeism
    absentee_summary = df.groupby("district")[absentees_col].sum().reset_index().sort_values(absentees_col, ascending=False).head(10)
    st.plotly_chart(px.bar(absentee_summary, x="district", y=absentees_col, title="Top 10 Districts by Absenteeism"), use_container_width=True)


    # 4. Vacancy Rate Distribution
    st.plotly_chart(px.box(df, y="vacancy_rate", x="district", title="Vacancy Rate Distribution by District"), use_container_width=True)


    # 5. Sanction vs Admission
    stacked = df.groupby("district")[[sanctioned_col, admitted_col]].sum().reset_index()
    stacked = stacked.melt(id_vars="district", value_vars=[sanctioned_col, admitted_col], var_name="Type", value_name="Seats")
    st.plotly_chart(px.bar(stacked, x="district", y="Seats", color="Type", title="Sanctioned vs Admitted Seats"), use_container_width=True)


    # 6. Top & Bottom 5 Institutes
    top_5 = df.nlargest(5, "attendance_%")[["college_name", "attendance_%"]]
    bottom_5 = df.nsmallest(5, "attendance_%")[["college_name", "attendance_%"]]
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 5 Institutes (Attendance %)")
        st.dataframe(top_5)
    with col2:
        st.subheader("Bottom 5 Institutes (Attendance %)")
        st.dataframe(bottom_5)


    # DRILL-DOWN: SELECT DISTRICT
    selected_district = st.selectbox("Search for a District for Detailed Institute View", df["district"].unique())
    drill_df = df[df["district"] == selected_district][["college_name", sanctioned_col, admitted_col, vacant_col, attendance_col, absentees_col, "attendance_%"]]
    st.dataframe(drill_df)


    # DOWNLOAD DATA
    def download_excel(dataframe):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            dataframe.to_excel(writer, index=False, sheet_name="Report")
        return output.getvalue()


    st.download_button("📥 Download Excel Report", data=download_excel(df), file_name="education_dashboard_report.xlsx")


else:
    st.warning("Upload the merged dataset to start the analysis.")