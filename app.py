import streamlit as st
import urllib.parse

st.set_page_config(
    page_title="Looker Studio BigQuery usage cost dashboard generator",
    page_icon="💸",
)

st.title('Looker Studio BigQuery usage cost dashboard generator')
st.markdown('''> Example of the generated dashboard (also serves as a [TEMPLATE] for new ones):
>
> https://lookerstudio.google.com/reporting/6e873fe2-8118-44e7-ab14-e8f84ca4e636
>
> Project ID: `gbg-a-3`
>
> Region qualifier: `region-eu`
> 
> Authuser: `toriya@precisdigital.com`
> 
> Days back: `30`
''')

st.subheader('Fill in the form below to generate a URL for a Looker Studio dashboard')

project_id = st.text_input('(required) Project ID', 'my-project-123')
region = st.text_input('(required) Region qualifier. \
                       Queries against this view must include a [region qualifier](https://cloud.google.com/bigquery/docs/information-schema-intro#region_qualifier). \
                       Be aware, it restricts results to the specified location. So, if in your project you have 3 datasets with EU (region-eu) location and 1 dataset with europe-west1 (region-europe-west1) \
                       location only the costs from 3 datasets (region-eu) will be included', 'region-eu')
# dataset_id = st.text_input('Dataset ID', 'my_dataset')
authuser = st.text_input(f"(required) Google Account email to use for `{project_id}`. This email should have `bigquery.jobs.listAll` permission, it's included in either `BigQuery Admin` or `BigQuery Resource Viewer` role.", "tech-solutions@precisdigital.com")
days_back = st.number_input('Days back to query from now. Be aware, getting the data about BigQuery cost, also cost money. However, `30` days from now is quite cheap.', 1, 365, 30)
report_name = st.text_input('Report Name', f"v1.0.1 - BigQuery Cost / {project_id} / {region} / last {days_back} days")

def generate_encoded_url(project_id, report_name, sql, authuser="tech-solutions@precisdigital.com"):
    base_url = "https://lookerstudio.google.com/reporting/create"
    params = {
        "authuser": authuser,
        "c.reportId": "6e873fe2-8118-44e7-ab14-e8f84ca4e636",
        "c.explain": True,
        "r.reportName": report_name,
        "ds.ds18.connector": "bigQuery",
        "ds.ds18.type": "CUSTOM_QUERY",
        "ds.ds18.projectId": project_id,
        "ds.ds18.sql": sql
    }

    encoded_params = urllib.parse.urlencode(params, safe=".")
    return f"{base_url}?{encoded_params}"

if st.button('Generate URL'):
    sql = f"""SELECT * FROM `{project_id}`.`{region}`.INFORMATION_SCHEMA.JOBS
WHERE statement_type != 'SCRIPT'
and creation_time BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24*{days_back} HOUR) AND CURRENT_TIMESTAMP()"""
    url = generate_encoded_url(project_id, report_name, sql, authuser)
    st.write("Use this URL to generate a Looker Studio dashboard:")
    st.write(url)

    st.write("If you see data on the dashboard, you're good to go. Click 'Edit and share' > 'Acknowledge and save'")
    st.image('images/chrome_PxUxerjowd.png', use_column_width=True)

    st.write("If you experience any issues, check the 'Report details'")
    st.image('images/chrome_xhDJuEx0SD.png', use_column_width=True)
