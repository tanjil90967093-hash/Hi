with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    lines = f.readlines()

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    for line in lines[:929]:
        f.write(line)
