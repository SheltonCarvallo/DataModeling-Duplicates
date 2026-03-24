from recordlinkage.preprocessing.encoding import phonetic
import random

def preprocess_dataframe(df, index_name='', dataset_name="dataset"):
      """Clean and encode a customer dataframe for record linkage."""
      df = df.copy()  # avoid modifying original

      df['first_name_cleaned'] = df['first_name'].str.strip().str.title()
      df['surname_cleaned'] = df['surname'].str.strip().str.title()
      df['postcode_cleaned'] = df['postcode'].str.strip()

      df['phonetic_first_name'] = phonetic(df['first_name_cleaned'], 'soundex')
      df['phonetic_surname'] = phonetic(df['surname_cleaned'], 'soundex')
      df['initials'] = df['first_name_cleaned'].str[0] + df['surname_cleaned'].str[0]

      df = df.set_index(index_name)
      print(f"{dataset_name}: {df.shape[0]} rows after preprocessing")
      return df


def show_pairs_dfs(df1, df2, multi_index, random_samples=False, number_of_samples=5):
    try:
        if(not random_samples):
            for idx1, idx2 in multi_index:
                print(df1.loc[idx1])
                print(df2.loc[idx2])
                print('--'*12)
            return
        random.seed(42)
        counter = 0
        while(counter < number_of_samples):
            random_index = random.randrange(0, len(multi_index))
            idx1, idx2 = multi_index[random_index]
            print(df1.loc[idx1])
            print(df2.loc[idx2])
            print('--'*12)        
            counter += 1
    except Exception as ex:
        print(f"There was a problem: {ex}")


def show_dfs_lengths(dict_of_dfs):
    for k, v in dict_of_dfs.items():
        print(f'Número de emparejamientos {k}: {len(v)}')

""" This function returns boolean masks
for each column introduce in the list_columns parameter
each boolean mask is stored in a dictionary with its respective key
"""
def get_boolean_masks(dataframe1, dataframe2, multiIndex, list_columns):
    try:
        df1 = dataframe1.loc[multiIndex.get_level_values(0), list_columns]
        df2 = dataframe2.loc[multiIndex.get_level_values(1), list_columns]
        dict_mask_booleans = {}
        for column in list_columns:
            dict_mask_booleans[column] = df1[column].values == df2[column].values
        return dict_mask_booleans
    except Exception as e:
        print(f"An unexpected error ocurred: {e}")        