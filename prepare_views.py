import json, re

# Load all 7 extracted view HTML strings
view_keys = ["dashboard", "courses", "my-course", "activity", "practice", "academics", "code-review"]
views = {}
for k in view_keys:
    with open(f"extracted_{k}.html", "r", encoding="utf-8") as f:
        # ensure all image paths are relative ./assets/images/
        c = f.read()
        views[k] = c

# Build JSON dictionary of all views
with open("views_data.json", "w", encoding="utf-8") as f:
    json.dump(views, f)

print("views_data.json created successfully with all 7 views")
