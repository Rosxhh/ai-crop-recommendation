import os

path = r'c:\Users\acer\Desktop\CropYieldProject\crop_project\templates\result.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace sustainability dict with .score where needed
new_content = content.replace('analytics.sustainability|add:"-100"', 'analytics.sustainability.score|add:"-100"')
new_content = new_content.replace('{{ analytics.sustainability }}', '{{ analytics.sustainability.score }}')

# Fix any other potential issues found in the screenshot
# The screenshot shows a loading spinner and broken layout.
# This often happens if tags are not closed.

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed sustainability references in result.html")
