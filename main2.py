import json

FILENAME = "people.json"
RESULT_FILENAME = "result.json"

def create_initial_data():
    people = [
        {"Name": "Ivan Petrenko", "Gender": "m", "Height": 180},
        {"Name": "Oleh Shevchenko", "Gender": "m", "Height": 172},
        {"Name": "Maksym Bondar", "Gender": "m", "Height": 190},
        {"Name": "Serhii Kovalenko", "Gender": "m", "Height": 175},
        {"Name": "Yurii Melnyk", "Gender": "m", "Height": 185},
        {"Name": "Anna Ivanova", "Gender": "f", "Height": 165},
        {"Name": "Olha Sydorenko", "Gender": "f", "Height": 160},
        {"Name": "Iryna Tkachenko", "Gender": "f", "Height": 170},
        {"Name": "Kateryna Hrytsenko", "Gender": "f", "Height": 167},
        {"Name": "Tetiana Marchenko", "Gender": "f", "Height": 162}
    ]
    with open(FILENAME, "w") as f:
        json.dump(people, f, ensure_ascii=False, indent=4)

def read_json():
    try:
        with open(FILENAME, "r") as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Invalid data format in JSON.")
            return data
    except FileNotFoundError:
        print("File not found. Creating new file...")
        create_initial_data()
        return read_json()
    except (json.JSONDecodeError, ValueError):
        print("Error reading JSON. Creating new file...")
        create_initial_data()
        return read_json()

def write_json(data):
    if not isinstance(data, list):
        print("Error: invalid data format for writing.")
        return
    with open(FILENAME, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def show_data():
    data = read_json()
    print("\nCurrent data:")
    for person in data:
        print(f"Name: {person.get('Name','Unknown')}, Gender: {person.get('Gender','-')}, Height: {person.get('Height','-')} cm")

def add_person():
    data = read_json()

    while True:
        full_name = input("Enter Name and Surname (e.g., Ivan Petrenko): ").strip()
        if len(full_name.split()) == 2 and all(part.isalpha() for part in full_name.split()):
            break
        else:
            print("Enter valid Name and Surname (letters only, separated by a space).")

    while True:
        gender = input("Gender (m - male / f - female): ").lower().strip()
        if gender in ("m", "f"):
            break
        else:
            print("Enter only 'm' or 'f'!")

    while True:
        try:
            height = float(input("Height (cm): "))
            if 50 <= height <= 250:
                break
            else:
                print("Unrealistic height. Enter value between 50-250 cm.")
        except ValueError:
            print("Error: enter a number!")

    if any(p["Name"].lower() == full_name.lower() for p in data):
        print("Error: person with this Name and Surname already exists.")
        return

    data.append({"Name": full_name, "Gender": gender, "Height": height})
    write_json(data)
    print(f"Record for {full_name} added!")

def delete_person():
    data = read_json()
    full_name = input("Enter Name and Surname to delete: ").strip()
    new_data = [p for p in data if p["Name"].lower() != full_name.lower()]
    if len(new_data) == len(data):
        print("Person not found.")
    else:
        write_json(new_data)
        print(f"Record for {full_name} deleted.")

def search_person():
    data = read_json()
    name_part = input("Enter Name or Surname to search: ").strip()
    results = [p for p in data if name_part.lower() in p["Name"].lower()]
    if results:
        print("\nSearch results:")
        for p in results:
            print(f"Name: {p['Name']}, Gender: {p['Gender']}, Height: {p['Height']} cm")
    else:
        print("Nothing found.")

def average_male_height():
    data = read_json()
    males = [p["Height"] for p in data if p["Gender"] == "m" and isinstance(p.get("Height"), (int, float))]
    if not males:
        print("No male data available.")
        return
    avg = sum(males) / len(males)
    result = {"Average male height (cm)": round(avg, 2)}
    with open(RESULT_FILENAME, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    print(f"Average male height = {avg:.2f} cm (saved in {RESULT_FILENAME})")

def main():
    while True:
        print("\nPROGRAM MENU")
        print("1) Show data")
        print("2) Add record")
        print("3) Delete record")
        print("4) Search by Name or Surname")
        print("5) Calculate average male height")
        print("6) Exit")

        choice = input("Choose an option (1–6): ").strip()

        if choice == "1":
            show_data()
        elif choice == "2":
            add_person()
        elif choice == "3":
            delete_person()
        elif choice == "4":
            search_person()
        elif choice == "5":
            average_male_height()
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice! Enter a number from 1 to 6.")

if __name__ == "__main__":
    main()

