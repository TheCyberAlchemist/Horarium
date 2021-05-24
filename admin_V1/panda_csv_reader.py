a = pd.read_csv("filename.csv")

a.isnull().any() # for checking if any of the rows have empty cols

{'Email','Password', 'first_name', 'last_name'} == set(a.head(0)) 

# for checking all the headers

