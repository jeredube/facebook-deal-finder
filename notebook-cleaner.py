import re

input_file = "fb-scrapper.py"
output_file = "cleaned-fb-scrapper.py"

with open(input_file, "r") as f:
    code = f.readlines()

cleaned = []
for line in code:
    # remove jupyter cell markers like "# In[1]:", "# %%", "# run cell..."
    if re.match(r"#\s*In\[\d*\]:", line):
        continue
    if line.strip() in ["# %%", "# run cell below", "# run cell above"]:
        continue
    cleaned.append(line)

with open(output_file, "w") as f:
    f.writelines(cleaned)

print("Clean file generated:", output_file)