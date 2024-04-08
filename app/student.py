from datetime import datetime
from fastapi import HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Student
from app.student_serializers import studentEntity, studentListEntity
from bson.objectid import ObjectId
import json

router = APIRouter()


@router.get('/', response_model=schemas.StudentListResponse)
def get_students(limit: int = 10, page: int = 1, country: str = None, age: int = None):
    skip = (page - 1) * limit
    pipeline = [
        {
            '$skip': skip
        }, {
            '$limit': limit
        }
    ]
    
    if country:
        pipeline.append({'$match': {'address.country': country}})
    
    if age:
        pipeline.append({'$match': {'age': {'$gte': age}}})
    
    students = studentListEntity(Student.aggregate(pipeline))
    
    return {'data': students}


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.StudentResponse)
def create_student(payload: schemas.StudentBaseSchema):
    try:
        result = Student.insert_one(payload.dict(exclude_none=True))
        new_student = Student.find_one({'_id': result.inserted_id})
        return Response(status_code=status.HTTP_201_CREATED, content=json.dumps({"id": str(new_student["_id"])}), headers={"Content-Type": "application/json"})
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Student with title: {payload.title} already exists")


@router.patch('/{studentId}', response_model=schemas.StudentBaseSchema)
def update_student(studentId: str, payload: schemas.StudentBaseSchema):
    if not ObjectId.is_valid(studentId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {studentId}")
    updated_student = Student.find_one_and_update(
        {'_id': ObjectId(studentId)}, {'$set': payload.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if not updated_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No student with this id: {studentId} found')
    return Response(status_code=status.HTTP_200_OK, content=json.dumps({}), headers={"Content-Type": "application/json"})


@router.get('/{studentId}', response_model=schemas.StudentBaseSchema)
def get_student(studentId: str):
    if not ObjectId.is_valid(studentId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {studentId}")

    student = Student.find_one({'_id': ObjectId(studentId)})
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No student with this id: {studentId} found")
    return studentEntity(student)

@router.delete('/{studentId}')
def delete_student(studentId: str):
    if not ObjectId.is_valid(studentId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {studentId}")
    student = Student.find_one_and_delete({'_id': ObjectId(studentId)})
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No student with this id: {studentId} found')
    return Response(status_code=status.HTTP_200_OK, content=json.dumps({}), headers={"Content-Type": "application/json"})
