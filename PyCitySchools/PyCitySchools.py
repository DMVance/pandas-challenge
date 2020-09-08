%load_ext lab_black

import pandas as pd

schools_csv = "Resources/schools_complete.csv"
students_csv = "Resources/students_complete.csv"

school_df = pd.read_csv(schools_csv)
student_df = pd.read_csv(students_csv)

school_data = pd.merge(
    student_df, school_df, 
    how="left", 
    on=["school_name", "school_name"]
)

school_data = school_data.rename(
    columns={
        "Student ID": "student_id",
        "student_name": "student_name",
        "gender": "gender",
        "grade": "grade",
        "school_name": "school_name",
        "reading_score": "reading_score",
        "math_score": "math_score",
        "School ID": "school_id",
        "type": "type",
        "size": "size",
        "budget": "budget",
    }
)

### District Summary

tot_schools = school_data["school_name"].nunique()
tot_students = school_data["student_id"].nunique()
tot_budget = school_data["budget"].unique().sum()
avg_math = school_data["math_score"].mean()
avg_read = school_data["reading_score"].mean()
pass_rate = (avg_math + avg_read) / 2

# school_data["math_pass_fail"] = pd.cut(
#     school_data["math_score"], bins=[0, 70, 100], labels=["Fail", "Pass"], right=False
# )
# math_pass = school_data["math_pass_fail"].value_counts()["Pass"]
# math_pct_pass = round(((math_pass / tot_students * 100)), 2)

math_pct_pass = round(
    (
        (
            (
                school_data[school_data["math_score"] >= 70]["math_score"]
                .value_counts()
                .sum()
            )
            / tot_students
        )
        * 100
    ),
    2,
)

# school_data["reading_pass_fail"] = pd.cut(
#     school_data["reading_score"],
#     bins=[0, 70, 100],
#     labels=["Fail", "Pass"],
#     right=False,
# )
# reading_pass = school_data["reading_pass_fail"].value_counts()["Pass"]
# reading_pct_pass = round(((reading_pass / tot_students * 100)), 2)

reading_pct_pass = round(
    (
        (
            (
                school_data[school_data["reading_score"] >= 70]["reading_score"]
                .value_counts()
                .sum()
            )
            / tot_students
        )
        * 100
    ),
    2,
)

distric_summary_table = pd.DataFrame(
    {
        "tot_schools": [tot_schools],
        "tot_students": [tot_students],
        "tot_budget": [tot_budget],
        "avg_math": [avg_math],
        "avg_read": [avg_read],
        "pass_rate": [pass_rate],
        "math_pct_pass": [math_pct_pass],
        "reading_pct_pass": [reading_pct_pass],
    }
)

### School Summary

school_type = school_data.groupby(["school_name"])["school_type"].unique()
school_tot_students = school_data.groupby(["school_name"])["student_id"].nunique()
tot_school_budget = school_data.groupby(["school_name"])["budget"].mean()
per_student_budget = tot_school_budget / school_tot_students

avg_school_math_score = round(
    (school_data.groupby(["school_name"])["math_score"].mean()), 2
)

avg_school_read_score = round(
    (school_data.groupby(["school_name"])["reading_score"].mean()), 2
)

school_pct_pass_math = (
    (
        school_data[school_data["math_score"] >= 70]
        .groupby(["school_name"])["math_score"]
        .count()
    )
    / school_tot_students
) * 100

school_pct_pass_reading = (
    (
        school_data[school_data["reading_score"] >= 70]
        .groupby(["school_name"])["reading_score"]
        .count()
    )
    / school_tot_students
) * 100

school_overall_pass_rate = round(
    ((school_pct_pass_math + school_pct_pass_reading) / 2), 2
)

school_summary_table = pd.DataFrame(
    {
        "school_type": school_type,
        "school_tot_students": school_tot_students,
        "tot_school_budget": tot_school_budget,
        "per_student_budget": per_student_budget,
        "avg_school_math_score": avg_school_math_score,
        "avg_school_read_score": avg_school_read_score,
        "school_pct_pass_math": school_pct_pass_math,
        "school_pct_pass_reading": school_pct_pass_reading,
        "school_overall_pass_rate": school_overall_pass_rate,
    },
)

school_summary_table.sort_values(
    by=["school_overall_pass_rate"], ascending=False
).head()

school_summary_table.sort_values(by=["school_overall_pass_rate"]).head()

math_mean_9th = (
    school_data.loc[school_data["grade"] == "9th"]
    .groupby(["school_name"])["math_score"]
    .mean()
)
math_mean_10th = (
    school_data.loc[school_data["grade"] == "10th"]
    .groupby(["school_name"])["math_score"]
    .mean()
)
math_mean_11th = (
    school_data.loc[school_data["grade"] == "11th"]
    .groupby(["school_name"])["math_score"]
    .mean()
)
math_mean_12th = (
    school_data.loc[school_data["grade"] == "12th"]
    .groupby(["school_name"])["math_score"]
    .mean()
)

avg_math_by_grade = pd.DataFrame(
    {
        "9th": math_mean_9th,
        "10th": math_mean_10th,
        "11th": math_mean_11th,
        "12th": math_mean_12th,
    }
)

reading_mean_9th = (
    school_data.loc[school_data["grade"] == "9th"]
    .groupby(["school_name"])["reading_score"]
    .mean()
)
reading_mean_10th = (
    school_data.loc[school_data["grade"] == "10th"]
    .groupby(["school_name"])["reading_score"]
    .mean()
)
reading_mean_11th = (
    school_data.loc[school_data["grade"] == "11th"]
    .groupby(["school_name"])["reading_score"]
    .mean()
)
reading_mean_12th = (
    school_data.loc[school_data["grade"] == "12th"]
    .groupby(["school_name"])["reading_score"]
    .mean()
)

avg_reading_by_grade = pd.DataFrame(
    {
        "9th": reading_mean_9th,
        "10th": reading_mean_10th,
        "11th": reading_mean_11th,
        "12th": reading_mean_12th,
    }
)

### Scores by School Spending

spend_cat = pd.cut(
    school_summary_table["per_student_budget"],
    bins=[0, 585, 615, 645, 675],
    labels=["<$585", "$585-615", "$615-645", "$645-675"],
)

spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]

spend_per_student_results = pd.DataFrame(
    {
        "Spending_Ranges_(Per Student)": spend_cat,
        "Avg_Math_Score": avg_school_math_score,
        "Avg_Read_Score": avg_school_read_score,
        "%_Passing_Math": school_pct_pass_math,
        "%_Passing_Reading": school_pct_pass_reading,
        "%_Overall_Passing_Rate": school_overall_pass_rate,
    }
)
spend_per_student_results.set_index(["Spending Ranges (Per Student)"]).groupby(
    "Spending Ranges (Per Student)"
).mean()

### Scores by School Size

school_size = pd.cut(
    school_summary_table["school_tot_students"],
    bins=[0, 1000, 2000, 5000],
    labels=["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"],
)

spend_per_student_results = pd.DataFrame(
    {
        "School_Size": school_size,
        "Avg_Math_Score": avg_school_math_score,
        "Avg_Read_Score": avg_school_read_score,
        "%_Passing_Math": school_pct_pass_math,
        "%_Passing_Reading": school_pct_pass_reading,
        "%_Overall_Passing_Rate": school_overall_pass_rate,
    }
)
spend_per_student_results.set_index(["School_Size"]).groupby("School_Size").mean()

### Scores by School Type

school_type = pd.cut(
    school_summary_table["school_type"],
    bins=[],
    labels=["District", "Charter"],
)

scores_by_school_type = pd.DataFrame(
    {
        "School_Type": str(school_type[0]),
        "Avg_Math_Score": avg_school_math_score,
        "Avg_Read_Score": avg_school_read_score,
        "%_Passing_Math": school_pct_pass_math,
        "%_Passing_Reading": school_pct_pass_reading,
        "%_Overall_Passing_Rate": school_overall_pass_rate,
    }
)
scores_by_school_type.set_index(["School_Type"]).groupby("School_Type").mean()

In [9]: mapping = {'set': 1, 'test': 2}

In [10]: df.replace({'set': mapping, 'tesst': mapping})
    
mapping = {"District": 1, "Charter": 2}
school_summary_table.replace({"District": mapping, "Charter": mapping})
school_summary_table