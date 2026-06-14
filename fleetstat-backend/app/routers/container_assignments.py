from fastapi import APIRouter, HTTPException ,Depends
from sqlalchemy import text
from app.database import engine
from app.schemas import *
from app.dependencies import require_admin, get_current_user

router = APIRouter(
    prefix="/container_assignments",
    tags=["Container Assignments"]
)

@router.post("")
def create_container_assignment(assignment: ContainerAssignmentsCreate, current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO container_assignments (
                    trip_id,
                    container_id,
                    assigned_at
                )
                VALUES (
                    :trip_id,
                    :container_id,
                    NOW()
                )
                RETURNING assignment_id
            """),
            {
                "trip_id": assignment.trip_id,
                "container_id": assignment.container_id
            }
        )
        assignment_id = result.scalar()

    return {
        "message": "Container assignment created successfully",
        "assignment_id": assignment_id
    }




@router.get("")
def get_container_assignments(current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT * FROM container_assignments
        """))
        rows = result.fetchall()

        return [
            {
                "assignment_id": row.assignment_id,
                "trip_id": row.trip_id,
                "container_id": row.container_id,
                "assigned_at": row.assigned_at
            }
            for row in rows
        ]




@router.get("/{assignment_id}")
def get_container_assignment(assignment_id: int, current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT * FROM container_assignments
                WHERE assignment_id = :assignment_id
            """),
            {"assignment_id": assignment_id}
        )
        row = result.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Container assignment not found"
            )

        return {
            "assignment_id": row.assignment_id,
            "trip_id": row.trip_id,
            "container_id": row.container_id,
            "assigned_at": row.assigned_at
        }




@router.put("/{assignment_id}")
def update_container_assignment(assignment_id: int, assignment: ContainerAssignmentsUpdate, current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE container_assignments
                SET 
                    trip_id = :trip_id,
                    container_id = :container_id
                WHERE assignment_id = :assignment_id
            """),
            {
                "trip_id": assignment.trip_id,
                "container_id": assignment.container_id,
                "assignment_id": assignment_id
            }
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Container assignment not found"
            )

        return {"message": "Container assignment updated successfully"}




@router.delete("/{assignment_id}")
def delete_container_assignment(assignment_id: int,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                DELETE FROM container_assignments
                WHERE assignment_id = :assignment_id
            """),
            {"assignment_id": assignment_id}
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Container assignment not found"
            )

        return {"message": "Container assignment deleted successfully"}




