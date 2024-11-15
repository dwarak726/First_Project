import mysql.connector

# 1. Establish the connection
connection = mysql.connector.connect(
    host='localhost',        # e.g., 'localhost'
    user='root',             # e.g., 'root'
    password='dwaraksql@726',# e.g., 'password'
    database='apartment_info'# e.g., 'apartment_info'
)
    
# 2. Create a cursor object (outside the loop)
cursor = connection.cursor()

flatno = 100
a = int(input("Enter the number of records to insert: "))

for i in range(a):
    b = input("Phone number: ")
    c = input("Username: ")
    d = input("Password: ")
    e = input("Vehicle count: ")

    # 3. Write the SQL Insert query for residants
    query = """
        INSERT INTO residants (phoneno, vehiclecount, flatno, username, password) 
        VALUES (%s, %s, %s, %s, %s)
    """
    
    # 4. Data to be inserted into residants
    values = (b, e, flatno, c, d)  # Use `e` as vehicle count
    cursor.execute(query, values)

    # Commit the transaction after inserting into residants
    connection.commit()

    # 5. Insert corresponding vehicles into vehicleinfo
    for _ in range(int(e)):  # Loop based on vehicle count
        query2 = """
        INSERT INTO vehicleinfo (vehicle_regno, flatno, vehicle_name) 
        VALUES (%s, %s, %s)
        """
        k = input("Registration no: ")
        l = input("Vehicle name: ")
        values2 = (k, flatno, l)  # Use the same `flatno` as residants
        cursor.execute(query2, values2)

    # Commit the transaction after inserting into vehicleinfo
    connection.commit()

    # Optional: Print the number of rows inserted
    print(cursor.rowcount, "record(s) inserted.")

    # Increment flat number for the next record in residants
    flatno += 1  

# 6. Close the cursor and connection
cursor.close()
connection.close()

