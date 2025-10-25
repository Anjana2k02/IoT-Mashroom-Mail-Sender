from db_handler import fetch_all_data, fetch_filtered_data
from email_handler import send_email
from llama_handler import (
    initialize_llama,
    create_index_from_dataframe,
    query_index,
    save_index,
    load_index
)

def main():
    # Initialize LlamaIndex
    initialize_llama()
   
    # Fetch all data from details table
    print("Fetching data from 'details' table...")
    data = fetch_all_data('details')
   
    if data is not None and not data.empty:
        print(f"Fetched {len(data)} records from database")
        print(f"Columns: {list(data.columns)}")
        print(f"\nData preview:\n{data.head()}")
        
        # Convert data to text format for LlamaIndex
        # Since 'details' table doesn't have a 'description' column,
        # we create a text representation of the data
        data['text_content'] = data.apply(
            lambda row: f"Type: {row['type']}, Date: {row['date']}, Value: {row['value']}, Status: {'Active' if row['status'] else 'Inactive'}",
            axis=1
        )
        
        # Create index from DataFrame
        print("\nCreating index from data...")
        index = create_index_from_dataframe(data, text_column='text_content')
       
        # Query the index
        print("\nQuerying the index...")
        response = query_index(index, "What are the patterns in the values and dates?")
        print(f"Response: {response}")
       
        # Save index for later use
        print("\nSaving index...")
        save_index(index)
       
        # Prepare email body with summary statistics
        summary = f"""
LlamaIndex Analysis Complete
=============================

Total Records: {len(data)}
Active Records: {data['status'].sum()}
Inactive Records: {(~data['status']).sum()}

Date Range: {data['date'].min()} to {data['date'].max()}
Value Range: {data['value'].min()} to {data['value'].max()}
Average Value: {data['value'].mean():.2f}

Analysis Results:
{response}
        """
        
        # Send results via email
        print("\nSending email...")
        send_email(
        'anjanaindu3699@gmail.com',
        'LlamaIndex Analysis Results - Details Table',
        summary
)
        
        print("\nProcess completed successfully!")
    else:
        print("No data fetched from database or data is empty.")
   
    # Example 2: Load existing index (uncomment to use)
    # print("\nLoading existing index...")
    # loaded_index = load_index()
    # if loaded_index:
    #     response = query_index(loaded_index, "What is the trend in the data?")
    #     print(f"Response from loaded index: {response}")

if __name__ == "__main__":
    main()