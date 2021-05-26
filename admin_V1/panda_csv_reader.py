import pandas as pd

a = pd.read_csv("student_details.csv")
b = a.loc[1]

# u = CustomUser(email=b['E-mail'],first_name=b['First name'],last_name=b['Last name'],password=b['Password'])
# a.isnull().any() # for checking if any of the rows have empty cols

# {'Email','Password', 'first_name', 'last_name'} == set(a.head(0)) 

# # for checking all the headers

