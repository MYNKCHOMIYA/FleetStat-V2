from fastapi import APIRouter, HTTPException ,Depends
from sqlalchemy import text
from app.database import engine
from app.schemas import *
from app.dependencies import require_admin, get_current_user

router = APIRouter(
    prefix="/containers",
    tags=["Containers"]
)

@router.post("")
def create_container(container: ContainerCreate,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO containers (
                    container_code,
                    container_type,
                    capacity_kg,
                    status,
                    description,
                    is_active,
                    created_at,
                    updated_at
                )
                VALUES (
                    :container_code,
                    :container_type,
                    :capacity_kg,
                    'AVAILABLE',
                    :description,
                    TRUE,
                    NOW(),
                    NOW()
                )
                RETURNING container_id
            """),
            {
                "container_code": container.container_code,
                "container_type": container.container_type,
                "capacity_kg": container.capacity_kg,
                "description": container.description
            }
        )
        container_id = result.scalar()

    return {
        "message": "Container created successfully",
        "container_id": container_id
    }




@router.get("")
def get_containers(current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT *
            FROM containers
            WHERE is_active = TRUE
        """))
        rows = result.fetchall()

        return [
            {
                "container_id": row.container_id,
                "container_code": row.container_code,
                "container_type": row.container_type,
                "capacity_kg": row.capacity_kg,
                "status": row.status,
                "description": row.description
            }
            for row in rows
        ]




@router.get("/{container_id}")
def get_container(container_id: int, current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT * FROM containers
                WHERE container_id = :container_id 
                AND is_active = TRUE
            """),
            {"container_id": container_id}
        )
        row = result.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Container not found"
            )

        return {
            "container_id": row.container_id,
            "container_code": row.container_code,
            "container_type": row.container_type,
            "capacity_kg": row.capacity_kg,
            "status": row.status,
            "description": row.description
        }




@router.put("/{container_id}")
def update_container(container_id: int, container: ContainerUpdate,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE containers
                SET 
                    container_code = :container_code,
                    container_type = :container_type,
                    capacity_kg = :capacity_kg,
                    status = :status,
                    description = :description,
                    updated_at = NOW()
                WHERE container_id = :container_id 
                AND is_active = TRUE
            """),
            {
                "container_code": container.container_code,
                "container_type": container.container_type,
                "capacity_kg": container.capacity_kg,
                "status": container.status,
                "description": container.description,
                "container_id": container_id
            }
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Container not found"
            )

        return {"message": "Container updated successfully"}




@router.delete("/{container_id}")
def delete_container(container_id: int,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE containers
                SET
                    is_active = FALSE,
                    status = 'OUT_OF_SERVICE',
                    updated_at = NOW()
                WHERE container_id = :container_id
            """),
            {"container_id": container_id}
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Container not found"
            )

        return {"message": "Container deleted successfully"}




