# Step 1: Create file and write initial content
with open("mydata.txt", "w") as file:
    file.write("This is the original content.\nSecond line of original content.")

# Step 2: Read and print original content
with open("mydata.txt", "r") as file:
    original_content = file.read()
    print("Original Content:\n", original_content)

# Step 3: Overwrite with new content
with open("mydata.txt", "w") as file:
    file.write("This is the new content after overwriting.\nJust another line.")

# Step 4: Read and print updated content
with open("mydata.txt", "r") as file:
    updated_content = file.read()
    print("\nUpdated Content:\n", updated_content)
