import pandas as pd
import string
import os
import secrets
import django
import numpy as np

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_management_web.settings')
django.setup()

# Import models after Django setup
from main.models import CustomUser
from main.models import Farm

# Read data from Excel file into a pandas DataFrame
def import_users():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    excel_file = os.path.join(current_directory, 'windwood_farmer_data.xlsx')
    df = pd.read_excel(excel_file, engine='openpyxl')

    # Initialize a list to store the newly created user data
    new_users_data = []

    # Define a function to generate a random password
    def generate_password():
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for i in range(10))  # Generate a 10-character random password
        return password

    # Iterate over rows of the DataFrame
    for index, row in df.iterrows():
        # Extract information from the row
        full_name = row['full_name']
        gender = row['gender']
        birth_year = row['birth_year']

            # Check if birth_year is NaN
        if pd.isna(birth_year):
            # Default birth_year to 0 if missing or invalid
            birth_year = 0
            
        national_id = row['national_id']
        district = row['district']
        phone_number = row['phone_number']
        crops = row['crops']
        farmer_orgs = row['farmer_orgs']
        land_size = row.get('land_size', 0)

          # Check if full_name is NaN
        if pd.isna(full_name):
            # Skip this row if full_name is NaN
            continue
        
         # Convert full_name to a string if it's not already a string
        if isinstance(full_name, float): 
            full_name = str(full_name)
        
        # Replace underscores with spaces in the full name
        full_name = full_name.replace('_', ' ')

        # Split the full name into first name and last name
        name_parts = full_name.rsplit(maxsplit=1)  # Split from the right side
        if len(name_parts) == 1:
            # If there's only one part, consider it as the first name
            first_name = name_parts[0]
            last_name = ""
        else:
            # Otherwise, assign the parts accordingly
            first_name, last_name = name_parts

        # Create a base username based on the full name (e.g., remove spaces and lowercase)
        base_username = first_name[0].lower() + last_name.lower()
        
        # Check if the base username already exists
        username = base_username
        count = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{count}"
            count += 1
     
        # Generate a random password
        password = generate_password()

        # Create a new Django User object
        user = CustomUser.objects.create_user(username=username, email='windwoodfarmernetwork@gmail.com', password=password)

        if pd.notna(phone_number):
            formatted_phone_number = str(int(float(phone_number)))
            user.phone_number = formatted_phone_number
   
        # user.first_name = full_name.split()[0]  # First name from the full name
        user.full_name = full_name
        user.first_name = first_name  # First name from the full name
        user.last_name = last_name  # Last name from the full name
    
        # Assign other attributes to the User object
        user.gender = gender
        user.birth_year = birth_year
        user.national_id = national_id
        user.district = district
        user.farmer_orgs = farmer_orgs
       
        # Save the User object
        user.save()
        
        # Create a new Farm object associated with the user

        farm_name = f"{full_name} {crops} Farm"
        
        farm = Farm.objects.create(user=user, name=farm_name, crops=crops, district=district, land_size=land_size)
        
        # Append user data to the list
        new_users_data.append({
            'full_name': full_name,
            'username': username,
            'password':password,
            'gender': gender,
            'birth_year': birth_year,
            'national_id': national_id,
            'district': district,
            'phone_number': phone_number,
            'crops': crops,
            'farmer_orgs': farmer_orgs,
            'land_size': land_size
        })

    # Convert the list of dictionaries to a DataFrame
    new_users_df = pd.DataFrame(new_users_data)

    # Write the DataFrame to a new Excel file
    new_excel_file = 'windwood_farmer_data-new_users-2.xlsx'
    new_users_df.to_excel(new_excel_file, index=False)

    print('OPERATION COMPLETED!!')

if __name__ == "__main__":
    import_users()
