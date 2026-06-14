from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy import text
from app.database import engine
from app.schemas import *
from app.dependencies import require_admin, get_current_user

router = APIRouter(
    prefix="/trip_assignments",
    tags=["Trip Assignments"]
)

@router.post("")
def create_trip_assignments(trip_assignments: Trip_assignmentsCreate, current_user=Depends(get_current_user)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO trip_assignments (
                    trip_id,
                    driver_id,
                    assigned_at
                )
                VALUES (
                    :trip_id,
                    :driver_id,
                    NOW()
                )
                RETURNING assignment_id
            """),
            {
                   "trip_id" :trip_assignments.trip_id,
                    "driver_id" :trip_assignments.driver_id,
            }
        )
        assignment_id  = result.scalar()

    return {
        "message": "Trip assignments created successfully",
        "assignment_id": assignment_id
    }
        


@router.get("")
def get_trip_assignments(current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                *
                from trip_assignments
        """))
        rows = result.fetchall()

        return [
            {
                "driver_id": row.driver_id,
                "trip_id": row.trip_id,
                "assignment_id": row.assignment_id,
                
            }
            for row in rows
        ]
        
        


@router.get("/{assignment_id}")
def get_trip_assignment(assignment_id: int, current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT *
                FROM trip_assignments
                WHERE assignment_id = :assignment_id
            """),
            {"assignment_id": assignment_id}
        )

        row = result.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Assignment not found"
            )

        return {
            "driver_id": row.driver_id,
            "trip_id": row.trip_id,
            "assignment_id": row.assignment_id
        }


@router.put("/{assignment_id}")
def update_trip_assignments(assignment_id: int, assignment: Trip_assignmentsUpdate, current_user=Depends(get_current_user)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE trip_assignments
                SET 
                   trip_id = :trip_id,
                    driver_id = :driver_id
                 WHERE assignment_id = :assignment_id
            """),
            {
                    
                    "trip_id" :assignment.trip_id,
                    "driver_id":assignment.driver_id,
                    "assignment_id":assignment_id,
            }
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Trip assignment not found"
            )

        return {"message": "Trip assignment updated successfully"}



@router.delete("/{assignment_id}")
def delete_trip_assignments(assignment_id: int,current_user=Depends(require_admin)):
    with engine.begin()  as conn:
        result = conn.execute(
            text("""
                DELETE FROM trip_assignments
                WHERE assignment_id = :assignment_id
            """),
            {"assignment_id": assignment_id}
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Trip assignment not found"
            )

        return {"message": "Trip assignment deleted successfully"}
    


