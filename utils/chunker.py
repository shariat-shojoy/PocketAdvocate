def build_document(row):

    document = f"""
Law Title:
{row['law_title']}

Description:
{row['law_descripton']}

Chapter:
{row['section_chapter_name']}

Section:
{row['section_name']}

Section Description:
{row['section_description']}
"""

    return document.strip()


def dataframe_to_documents(df):

    documents = []

    metadata = []

    for _, row in df.iterrows():

        documents.append(build_document(row))

        metadata.append(
            {
                "law_title": row["law_title"],
                "section_name": row["section_name"],
                "url_id": row["url_id"],
            }
        )

    return documents, metadata