import json
import os
import pandas as pd

ROW_DATA = "C"
UNCHANGED_DATA_BITMASK = "R"
NULL_DATA_BITMASK = "Ø"

METADATA_KEY_NAME = "S"
LOOKUP_TABLE_ID = "DN"

"""
Based on some random googling, this appears to be the 
possible data types.

    enum PrimitiveType {
        Null = 0,
        Text = 1,
        Decimal = 2,
        Double = 3,
        Integer = 4,
        Boolean = 5,
        Date = 6,
        DateTime = 7,
        DateTimeZone = 8,
        Time = 9,
        Duration = 10,
        Binary = 11,
        None = 12,
    }

"""
COL_DATA_TYPE = "T"
TYPE_TEXT = 1
TYPE_DATETIME = 7

def extract_raw_data(j):
    # return j['results'][0]['result']['data']['dsr']['DS'][0]['PH'][0]["DM0"] ## original parsing
    return j['results'][0]['result']['data']['dsr']['DS'][0]['PH'][0]["DM1"]    ## modify for wastewater
    
def extract_data_compression_table(j):
    return j['results'][0]['result']['data']['dsr']['DS'][0]["ValueDicts"]

def extract_query_metadata(j):
    return j['results'][0]['result']['data']['descriptor']['Select']

def extract_column_count(j):
    m = extract_query_metadata(j)
    return len(m)

def extract_column_metadata(j):
    # why they store this in the first result i do not know
    # this contains (1) what datatype the column is and 
    # (2) what lookup table key should we use to lookup data
    r = extract_raw_data(j)
    return r[0][METADATA_KEY_NAME]

def extract(n):
    # the end result array we'll be returning
    result = []

    query_results = extract_raw_data(n) 
    lookup = extract_data_compression_table(n)

    # We'll need this for loops and calculations.
    num_cols = extract_column_count(n)

    # This presizes an array the same size as our data
    # Part of the data compression algo is dropping columns 
    # if the data is the same as the previous row. So we'll need
    # to keep track of last values at all times.
    last_value_cache = [None] * num_cols

    # Column metadata contains what datatype the column is, and
    # which lookup key we should use to get compressed data
    column_metadata = extract_column_metadata(n)

    for entry in query_results: 
        # this eventually will be the final uncompressed row
        row = []

        raw_data = entry[ROW_DATA]
        
        # we're going to be popping off values from this array
        # in a minute. reversing the array makes this O(2n) instead of O(n^2)
        raw_data.reverse()
        
        # indicates what columns are missing because the data is the same as last row
        # if the mask key is not present, that means no columns removed
        unchanged_mask = entry.get(UNCHANGED_DATA_BITMASK, 0)

        # indicates what columns are missing because they're null
        # if the mask key is not present, that means no columns removed
        null_mask = entry.get(NULL_DATA_BITMASK, 0)

        # for each column in this particular row....
        for n in range(0, num_cols):
            # this will hold the final value of the current cell after we
            # untangle everything
            current_cell = None

            # If you haven't seen the bitshift operator before(<<), this 
            # bit of arcana means that from 0 to NUM_COLS, we can generate a binary
            # number like 000001, 000010, 000100, etc etc.
            #
            # This generates a bitmask for the current row. 
            #
            # if we bitwise AND the current row with the "is data missing" bitmasks,
            # it will return true (non-zero) if col n is missing from our raw data
            #
            # For example, if the unchanged bitmask is 001010, then:
            #
            # col0: 0010010 & 000001 = 000000 = false
            # col1: 0010010 & 000010 = 000010 = true 
            # col2: 0010010 & 000100 = 000000 = false
             
            col_mask = 1 << n

            # is the current column missing from the raw row data? 
            if unchanged_mask & col_mask: # YES, because it's unchanged
                current_cell = last_value_cache[n]
            elif null_mask & col_mask: # YES, because it's null
                current_cell = None
            else: # NO
                current_cell = raw_data.pop()
                # since we have a value, store it in the last value cache
                last_value_cache[n] = current_cell

            metadata = column_metadata[n]
            
            # OK, now that we *have* the data, we need to figure out if we need to 
            # format it, or if it's a reference to a lookup table.

            # This current code is fairly jank, and will crash if new datatypes are
            # added, but I don't think we'll need to worry about that for this project.

            if type(current_cell) == int:
                if metadata[COL_DATA_TYPE] == TYPE_TEXT:
                    # this means our data is in the lookup table
                    # and we should treat the current column as 
                    # an array position, not a literal integer
                    lookup_key = metadata[LOOKUP_TABLE_ID]
                    row.append(lookup[lookup_key][current_cell])

                else:
                    # TODO throw up some kind of alerting
                    # there's prolly other integer-like data 
                    # types out there, including actual integers
                    row.append(current_cell)
            else:
                row.append(current_cell)
        result.append(row)
    return(result)

with open("./json_files/wastewater_oct15_2nd_ext2.json", "r") as read_file:
    data = json.load(read_file)
    result = extract(data)

    ## for projected_waste
    # cols = ['region', 'province', 'city_municipality', 'projected_waste', 'year']
    
    ## for water quality
    # cols = ['year', 'region', 'waterbodies', 'parameter', 'geometric_mean', 'rating']
    
    ## for wastewater
    cols = ['emb_region', 'office_name', 'branch_name', 'branch_city', 'branch_province', 'application_date', 'date_approved', 'date_expired', 'status', 'valid_permit']
    
    ## for wastewater discharge
    
    df = pd.DataFrame(result, columns=cols)
    print(df.shape)
    df.to_csv('csv_files/wastewater_oct15_2nd_ext2.csv', encoding='utf-8')
    print("Finish export!")
    
    
    
        
        