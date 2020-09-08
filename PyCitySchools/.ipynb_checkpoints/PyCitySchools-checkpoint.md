for District info:
round((((float((school_data[school_data["math_score"] >= 70])) / float(tot_students))) * 100), 2)
or
grouping method: use binning on math_grades or math_pass? same for reading.
school_data.groupby(["math_pass_fail"]).count()

tot_schools
tot_students
tot_budget
avg_math
avg_read
pass_rate
pct_pass_math
pct_pass_reading