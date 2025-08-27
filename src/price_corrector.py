# Wrap price_corrector as a function with concise example
import pandas as pd

# build price corrector
# find median price for specified refnis and property_type at t0
# find median price for same refnis, property_type at t1
# compute a correction factor dividing median price t1 with median price t0
# multiply the original listing_price by this correction factor to get the corrected price t1

def price_corrector(df,listing_price,refnis_code, property_type,t0_quarter, t1_quarter):
    """
    correct a listing price based on median prices at two different quarters

    Parameters:
    df: pd.Dataframe
        DataFrame containing real estate data with columns 'refnis', 'property_type','quarter', and 'prix_median'
    listing_price : float
        The initial listing price to be adjusted
    refnis_code: str or int
        identifier for the municipality
    property_type : str
        Type of property 'toute_maison','maison_2_3','maison_4_plus', 'apartment'
    t0_quarter : str
        The intial quarter string eg. 2022-Q1
    t1_quarter : str
        The target  quarter to which the price is adjusted

    Returns:
        float
            The price corrected for marlet changes between t0_quarter and t1_quarter
    
    Raises: 
        ValueError
            If median price data for provided quarters is missing

    """
   
    # find the median price at time t0
    median_t0_df = df[(df['refnis'] == refnis_code) &
    (df['property_type'] == property_type) &
    (df['quarter']== t0_quarter)]

    print(median_t0_df)

    if median_t0_df.empty:
        raise ValueError(f"No median price data for refnis = {refnis_code},property_type={property_type}, quarter={t0_quarter}")
    
    
    median_t0 = median_t0_df['prix_median'].values[0]


    # find the median price at time t1
    median_t1_df = df[(df['refnis']==refnis_code) &
    (df['property_type']==property_type) &
    (df['quarter']==t1_quarter)]

    if median_t1_df.empty:
        raise ValueError(f"No median price data for refnis = {refnis_code},property_type={property_type}, quarter={t1_quarter}")

    median_t1 = median_t1_df['prix_median'].values[0]

    # calculate the corrected price using ratio of median prices
    corrected_price = listing_price * (median_t1/median_t0)

    return corrected_price

if __name__ == "__main__":
    # Example usage:
    estate_data = pd.read_csv("../data/clean/normalized_table_1nf.csv")
    
    # create the quarter column as combined string of 'annee' and 'periode'
    estate_data['quarter'] = estate_data['annee'].astype(str) + '-' + estate_data['periode']

    # Select example refnins and property type from the dataset
    example_refnis = estate_data ['refnis'].iloc[0]
    example_property_type = estate_data['property_type'].iloc[0]

    # find two different quarters for the example
    example_t0 = estate_data[(estate_data['refnis']==example_refnis)&
    (estate_data['property_type']==example_property_type)]['quarter'].dropna().unique()[0]

    example_t1 = estate_data[(estate_data['refnis']==example_refnis)&
    (estate_data['property_type']==example_property_type)]['quarter'].dropna().unique()[10] # a quarter later in time


    # use a hypothetical price
    listing_price  =  estate_data[(estate_data['refnis']==example_refnis)&
    (estate_data['property_type']==example_property_type) &
    (estate_data['quarter'] == example_t0)]['prix_median'].values[0]

    print(listing_price)

    # Calculate the corrected price
    corrected_price_example = price_corrector(estate_data,listing_price,example_refnis, example_property_type, example_t0,example_t1)

    print(f"Example Price Correction:")
    print(f"Refnis: {example_refnis}")
    print(f"Property Type: {example_property_type}")
    print(f"Listed Price at {example_t0}:{listing_price} €")
    print(f"Corrected Price at {example_t1}:{corrected_price_example:.2f} €")

    


