def studentEntity(student) -> dict:
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "age": student["age"],
        "address": student["address"]
    }

def studentListEntity(students) -> list:
    return [studentEntity(student) for student in students]