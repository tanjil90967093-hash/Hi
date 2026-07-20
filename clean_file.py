with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    lines = f.readlines()

# delete lines 882 to 947
# line numbers are 1-based, so indices 881 to 946
del lines[881:947]

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.writelines(lines)
