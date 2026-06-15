from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    users,
    drivers,
    trucks,
    trips,
    shipments,
    containers,
    customers,
    payments,
    fuel_logs,
    damage_reports,
    truck_services,
    trip_assignments,
    container_assignments,
    shipment_items,
    analytics,
    auth
)

app = FastAPI(title="FleetStat API")

app.add_middleware(
        CORSMiddleware,
        allow_origins=[
                "http://localhost:5173",
                ],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
    )


@app.get("/")
def root():
    return {"message": "FleetStat Backend Running"}


# Register all routers
app.include_router(users.router)
app.include_router(drivers.router)
app.include_router(trucks.router)
app.include_router(trips.router)
app.include_router(shipments.router)
app.include_router(containers.router)
app.include_router(customers.router)
app.include_router(payments.router)
app.include_router(fuel_logs.router)
app.include_router(damage_reports.router)
app.include_router(truck_services.router)
app.include_router(trip_assignments.router)
app.include_router(container_assignments.router)
app.include_router(shipment_items.router)
app.include_router(analytics.router)
app.include_router(auth.router, prefix="/api/v1")

