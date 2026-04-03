import os

templates_dir = r"c:\Users\acer\Desktop\CropYieldProject\crop_project\templates"
files_to_append = [
    "index.html",
    "recommend.html",
    "result.html",
    "weather.html",
    "soil_upload.html"
]

def fix_append(filename):
    path = os.path.join(templates_dir, filename)
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Simple check for block end
    if "{% endblock %}" in content and "</div>\n{% endblock %}" not in content:
        # We want to ensure at least N divs close the containers opened at the start.
        # But a safer way is just to add the ONE missing div for the relative wrapper.
        new_content = content.replace("{% endblock %}", "</div>\n{% endblock %}")
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed {filename}")
    else:
        print(f"Skipping {filename} or already fixed.")

for f in files_to_append:
    fix_append(f)

# Special case for home.html (Cleanup extra divs)
home_path = os.path.join(templates_dir, "home.html")
if os.path.exists(home_path):
    with open(home_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # We saw redundant divs at the end.
    # Original lines 164-166 were extra divs.
    # Let's just find the last few divs and keep only what's needed.
    # 164:         </div>
    # 165:     </div>
    # 166: </div>
    # 167: {% endblock %}
    
    # Actually, let's just rewrite the end of home.html precisely.
    end_pattern = """        </div>
    </div>
</div>
{% endblock %}
"""
    # Find the last occurrence of the content before the mess.
    content = "".join(lines)
    if " Talk to AI " in content:
        # Re-construct the end of the file.
        # The last feature card ends at </a>
        last_a = content.rfind("</a>")
        if last_a != -1:
            new_end = content[:last_a+4] + "\n\n        </div>\n    </div>\n</div>\n{% endblock %}\n"
            with open(home_path, "w", encoding="utf-8") as f:
                f.write(new_end)
            print("Fixed home.html")
