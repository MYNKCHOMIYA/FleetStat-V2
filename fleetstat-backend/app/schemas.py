from pydantic import BaseModel
from datetime import date, datetime


class DriverCreate(BaseModel):
    full_name: str
    date_of_birth: date
    address: str
    license_number: str
    email: str
    phone_number: str
    prior_experience_years: int
    joining_date: date
    user_id: int


class DriverUpdate(BaseModel):
    address: str
    phone_number: str
    email: str


class DriverResponse(BaseModel):
    driver_id: int
    full_name: str
    user_id: int
    email: str
    phone_number: str    


class TruckCreate(BaseModel):
    license_plate: str
    manufacturer: str
    model: str
    purchase_date: date
    purchase_cost: float
    capacity_tons: float
    total_distance_travelled: int = 0
    last_service_date: date | None = None
    description: str | None = None 


class TruckUpdate(BaseModel):
    license_plate: str
    manufacturer: str
    model: str
    purchase_date: date
    purchase_cost: float
    capacity_tons: float
    total_distance_travelled: int = 0
    last_service_date: date | None = None
    description: str | None = None 


class TripCreate(BaseModel):
    truck_id: int
    start_location: str
    end_location: str
    trip_distance: int
    fuel_used: int
    start_time: datetime
    end_time: datetime
    trip_status: str


class TripUpdate(BaseModel):
    truck_id: int
    start_location: str
    end_location: str
    trip_distance: int
    fuel_used: int
    start_time: datetime
    end_time: datetime
    trip_status: str


class ShipmentCreate(BaseModel):
    trip_id: int
    container_id: int
    sender_customer_id: int
    receiver_customer_id: int
    shipment_status: str
    received_date: date
    shipped_date: date | None = None
    delivered_date: date | None = None
    notes: str | None = None


class ShipmentUpdate(BaseModel):
    trip_id: int
    container_id: int
    sender_customer_id: int
    receiver_customer_id: int
    shipment_status: str
    received_date: date
    shipped_date: date | None = None
    delivered_date: date | None = None
    notes: str | None = None


class Trip_assignmentsCreate(BaseModel):
    trip_id: int
    driver_id: int
    

class Trip_assignmentsUpdate(BaseModel):
    trip_id: int
    driver_id: int
    

class UserCreate(BaseModel):
    username: str
    email: str
    password_hash: str
    role: str


class UserUpdate(BaseModel):
    username: str
    email: str
    password_hash: str
    role: str
    is_active: bool


class CustomerCreate(BaseModel):
    customer_type: str
    customer_name: str
    gst_number: str
    email: str
    phone_number: str
    address: str


class CustomerUpdate(BaseModel):
    customer_type: str
    customer_name: str
    gst_number: str
    email: str
    phone_number: str
    address: str


class ContainerCreate(BaseModel):
    container_code: str
    container_type: str
    capacity_kg: float
    description: str | None = None


class ContainerUpdate(BaseModel):
    container_code: str
    container_type: str
    capacity_kg: float
    status: str
    description: str | None = None


class ContainerAssignmentsCreate(BaseModel):
    trip_id: int
    container_id: int


class ContainerAssignmentsUpdate(BaseModel):
    trip_id: int
    container_id: int


class ShipmentItemCreate(BaseModel):
    shipment_id: int
    item_name: str
    quantity: int
    weight_kg: float
    declared_value: float
    temperature_required: float | None = None


class ShipmentItemUpdate(BaseModel):
    shipment_id: int
    item_name: str
    quantity: int
    weight_kg: float
    declared_value: float
    temperature_required: float | None = None


class PaymentCreate(BaseModel):
    shipment_id: int
    amount: float
    payment_method: str
    payment_status: str
    remarks: str | None = None


class PaymentUpdate(BaseModel):
    shipment_id: int
    amount: float
    payment_method: str
    payment_status: str
    remarks: str | None = None


class DamageReportCreate(BaseModel):
    shipment_id: int
    damage_percentage: float
    description: str


class DamageReportUpdate(BaseModel):
    shipment_id: int
    damage_percentage: float
    description: str


class FuelLogCreate(BaseModel):
    truck_id: int
    trip_id: int | None = None
    fuel_amount: float
    fuel_cost: float


class FuelLogUpdate(BaseModel):
    truck_id: int
    trip_id: int | None = None
    fuel_amount: float
    fuel_cost: float


class TruckServiceCreate(BaseModel):
    truck_id: int
    service_center: str
    service_date: date
    service_cost: float
    next_due_date: date | None = None
    description: str | None = None


class TruckServiceUpdate(BaseModel):
    truck_id: int
    service_center: str
    service_date: date
    service_cost: float
    next_due_date: date | None = None
    description: str | None = None
    

class LoginRequest(BaseModel):
    username: str
    password: str
        

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
