import pandas as pd
import json

def transform_data(file_path, output_file_path):
    data_df = pd.read_json(file_path)
    # Adding book_id column
    data_df["book_id"] = data_df.url.str.extract(r".*?(\d+)")
    data_df['rating_count'] = data_df['rating_count'].str.extract(r'(\d+(?:,\d+)*)')
    data_df['rating_count'] = data_df['rating_count'].str.replace(',', '').astype(int)

    data_df['reviews'] = data_df['reviews'].str.extract(r'(\d+(?:,\d+)*)')
    data_df['reviews'] = data_df['reviews'].str.replace(',', '').astype(int)
    data_df["rating_stars"] = data_df["rating_stars"].astype(float)
    
    # pagecount column 
    data_df["format_type"] = data_df['pagecount'].str.extract(r'pages,\s*(.*)')[0]
    data_df['pagecount'] = data_df['pagecount'].str.extract(r'(\d+(?:,\d+)*)')
    data_df['pagecount'] = data_df['pagecount'].astype('Int64')
    data_df['format_type'] = data_df['format_type'].fillna('Not Specified')

    data_df['published_date'] = data_df['published_date'].str.extract(r'(\b\w+ \d{1,2}, \d{4}\b)')
    data_df['published_date'] = data_df['published_date'].fillna('Not Specified')

    # Saving clean data in a file.
    data_list = data_df.to_dict(orient="records")

    with open(output_file_path, "w") as file:
        json.dump(data_list, file, indent=4)



if __name__ == "__main__":
    transform_data("../goodreads_books_extracted.json", "../data/goodreads_books_clean.json")