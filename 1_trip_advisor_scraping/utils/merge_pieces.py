import pandas as pd

df1 = pd.read_csv('../output_files/restaurants_definitive.csv')
df2 = pd.read_csv('../output_files/restaurants_definitive2700.csv')
df3 = pd.read_csv('../output_files/restaurants_definitive6210.csv')

df4 = pd.read_csv('../output_files/reviewLinks.csv')
df5 = pd.read_csv('../output_files/reviewLinks2700.csv')
df6 = pd.read_csv('../output_files/reviewLinks6210.csv')

reviews = pd.read_csv('../output/reviews_save.csv')
restaurants = pd.read_csv('../output/trip_restaurants_final.csv')

df = restaurants.merge(reviews, how='left', on='id')
df.to_csv('../output/trip_advisor_DEFINITIVE.csv')

# result_rest = pd.concat([df1, df2, df3])
# result_reviews = pd.concat([df4, df5, df6])


# result_rest.to_csv('../output/trip_restaurants_final.csv', index=False)
# result_reviews.to_csv('../output/trip_reviews_link.csv', index=False)


