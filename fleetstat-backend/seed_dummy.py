#!/usr/bin/env python3
"""
Seed Script for FleetStat Database
Generates significant, realistic, and relationally consistent dummy data.
Preserves the 'mayank' admin user (user_id = 1).
"""

import os
import sys
import random
from datetime import datetime, date, timedelta
from sqlalchemy import text

# Add current path to sys.path so we can import from app
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
env_local_path = os.path.join(os.path.dirname(__file__), ".env.local")
if os.path.exists(env_local_path):
    print(f"[Seeder] Loading environment overrides from {env_local_path}")
    load_dotenv(env_local_path, override=True)
else:
    load_dotenv(override=True)

from app.database import engine
from app.auth import hash_password

def generate_indian_license_plate():
    states = ["MH", "DL", "KA", "HR", "GJ", "UP", "MH", "KA", "DL", "GJ", "UP", "MH", "KA", "DL"]
    state = random.choice(states)
    district = f"{random.randint(1, 99):02d}"
    letters = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=2))
    number = f"{random.randint(100, 9999):04d}"
    return f"{state} {district} {letters} {number}"

def generate_gst_number():
    state_code = f"{random.randint(10, 37):02d}"
    pan = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5)) + \
          "".join(random.choices("0123456789", k=4)) + \
          "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=1))
    entity_code = f"{random.randint(1, 9)}"
    z_char = "Z"
    checksum = "".join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=1))
    return f"{state_code}{pan}{entity_code}{z_char}{checksum}"

def main():
    print("[Seeder] Starting database seeding process...")

    # We generate the hash for driverpassword123 once to keep the seed script fast
    print("[Seeder] Hashing default password for dummy drivers...")
    driver_password_hash = hash_password("driverpassword123")
    print("[Seeder] Hashing complete.")

    # Driver Name lists
    driver_names = [
        "Aarav Sharma", "Vihaan Patel", "Aditya Verma", "Sai Kalyan", "Arjun Reddy",
        "Rohan Mehta", "Kabir Gupta", "Ishaan Singh", "Anirudh Nair", "Pranav Rao",
        "Krishna Murthy", "Sanjay Dutt", "Vijay Kumar", "Ramesh Kumar", "Suresh Raina",
        "Dinesh Karthik", "Amit Mishra", "Karan Johar", "Rahul Dravid", "Sachin Tendulkar",
        "Yuvraj Singh", "Mahendra Singh Dhoni", "Virat Kohli", "Rohit Sharma", "Hardik Pandya",
        "Jasprit Bumrah", "Rishabh Pant", "Ravindra Jadeja", "Shikhar Dhawan", "Cheteshwar Pujara"
    ]

    # Manufacturers and models
    truck_models = [
        {"manufacturer": "Tata Motors", "model": "Signa 4825.T", "capacity": 25.0},
        {"manufacturer": "Tata Motors", "model": "Prima FL 5530", "capacity": 30.0},
        {"manufacturer": "Mahindra", "model": "Blazo X 49", "capacity": 28.0},
        {"manufacturer": "Mahindra", "model": "Furio 14", "capacity": 14.0},
        {"manufacturer": "Ashok Leyland", "model": "U-Truck 3718", "capacity": 18.0},
        {"manufacturer": "Ashok Leyland", "model": "Ecomet 1615", "capacity": 16.0},
        {"manufacturer": "BharatBenz", "model": "2823R", "capacity": 20.0},
        {"manufacturer": "Eicher Motors", "model": "Pro 6028", "capacity": 22.0},
        {"manufacturer": "Volvo Trucks", "model": "FM 420", "capacity": 40.0},
        {"manufacturer": "Scania", "model": "G 410", "capacity": 35.0}
    ]

    # Logistics Customers
    customer_list = [
        {"name": "Reliance Retail", "type": "BUSINESS"},
        {"name": "Adani Logistics", "type": "BUSINESS"},
        {"name": "Tata Steel", "type": "BUSINESS"},
        {"name": "Amazon India", "type": "BUSINESS"},
        {"name": "Flipkart Wholesale", "type": "BUSINESS"},
        {"name": "DHL Express India", "type": "BUSINESS"},
        {"name": "FedEx Logistics", "type": "BUSINESS"},
        {"name": "Blue Dart Express", "type": "BUSINESS"},
        {"name": "Delhivery Private Ltd", "type": "BUSINESS"},
        {"name": "DTDC Express", "type": "BUSINESS"},
        {"name": "Mahindra Logistics Ltd", "type": "BUSINESS"},
        {"name": "Safexpress India", "type": "BUSINESS"},
        {"name": "VRL Logistics Ltd", "type": "BUSINESS"},
        {"name": "Transport Corp of India", "type": "BUSINESS"},
        {"name": "Gati KWE", "type": "BUSINESS"},
        {"name": "Allcargo Logistics", "type": "BUSINESS"},
        {"name": "Ekart Logistics", "type": "BUSINESS"},
        {"name": "Shadowfax Logistics", "type": "BUSINESS"},
        {"name": "Porter Logistics Services", "type": "BUSINESS"},
        {"name": "Blowhorn Logistics", "type": "BUSINESS"}
    ]

    # Locations
    locations = [
        "Mumbai, Maharashtra", "Delhi, NCR", "Bengaluru, Karnataka", "Chennai, Tamil Nadu",
        "Kolkata, West Bengal", "Hyderabad, Telangana", "Pune, Maharashtra", "Ahmedabad, Gujarat",
        "Jaipur, Rajasthan", "Lucknow, Uttar Pradesh", "Chandigarh, Punjab", "Indore, Madhya Pradesh",
        "Kochi, Kerala", "Visakhapatnam, Andhra Pradesh", "Surat, Gujarat", "Nagpur, Maharashtra",
        "Patna, Bihar", "Guwahati, Assam", "Bhubaneswar, Odisha", "Coimbatore, Tamil Nadu"
    ]

    # Shipment items
    shipment_items_pool = [
        {"name": "Electronics (TV, Mobile, Laptop)", "weight": 1200, "val": 1500000},
        {"name": "Cotton Textiles & Apparels", "weight": 2500, "val": 800000},
        {"name": "Industrial Machinery Spare Parts", "weight": 4000, "val": 2400000},
        {"name": "Fresh Fruits (Mango, Apple)", "weight": 1800, "val": 350000, "temp": 4.5},
        {"name": "Pharmaceutical Formulations", "weight": 800, "val": 4200000, "temp": 15.0},
        {"name": "Chemical Raw Powders", "weight": 5000, "val": 1200000},
        {"name": "Automotive Engine Components", "weight": 3500, "val": 1900000},
        {"name": "Packaged Snacks & Beverages", "weight": 2200, "val": 450000},
        {"name": "Stainless Steel Rods & Pipes", "weight": 8000, "val": 1400000},
        {"name": "Polyester Plastic Granules", "weight": 6000, "val": 700000},
        {"name": "Monocrystalline Solar Panels", "weight": 3000, "val": 3100000},
        {"name": "Computer Server Racks", "weight": 1500, "val": 5500000},
        {"name": "Premium Footwear Products", "weight": 1000, "val": 1100000},
        {"name": "Home Appliances (AC, Refrigerator)", "weight": 3200, "val": 1600000},
        {"name": "Rechargeable Lithium-ion Batteries", "weight": 2800, "val": 2900000}
    ]

    with engine.begin() as conn:
        print("[Seeder] Clearing old records (except admin mayank user_id=1)...")
        # 1. Clear child tables first
        conn.execute(text("TRUNCATE public.damage_reports CASCADE;"))
        conn.execute(text("TRUNCATE public.payments CASCADE;"))
        conn.execute(text("TRUNCATE public.shipment_items CASCADE;"))
        conn.execute(text("TRUNCATE public.shipments CASCADE;"))
        conn.execute(text("TRUNCATE public.container_assignments CASCADE;"))
        conn.execute(text("TRUNCATE public.trip_assignments CASCADE;"))
        conn.execute(text("TRUNCATE public.fuel_logs CASCADE;"))
        conn.execute(text("TRUNCATE public.truck_services CASCADE;"))
        conn.execute(text("TRUNCATE public.trips CASCADE;"))
        conn.execute(text("TRUNCATE public.containers CASCADE;"))
        conn.execute(text("TRUNCATE public.customers CASCADE;"))
        conn.execute(text("TRUNCATE public.drivers CASCADE;"))
        conn.execute(text("TRUNCATE public.trucks CASCADE;"))
        conn.execute(text("TRUNCATE public.vehicles CASCADE;"))

        # 2. Clear users except mayank (user_id=1)
        conn.execute(text("DELETE FROM public.users WHERE user_id != 1;"))

        # 3. Reset all sequences to restart from clean numbers
        conn.execute(text("SELECT setval('users_user_id_seq', 1, true);"))
        conn.execute(text("ALTER SEQUENCE public.containers_container_id_seq RESTART WITH 1;"))
        conn.execute(text("ALTER SEQUENCE public.customers_customer_id_seq RESTART WITH 1;"))
        conn.execute(text("ALTER SEQUENCE public.driver_driver_id_seq RESTART WITH 1;"))
        conn.execute(text("ALTER SEQUENCE public.trips_trip_id_seq RESTART WITH 1;"))
        conn.execute(text("ALTER SEQUENCE public.trip_assignments_assignment_id_seq RESTART WITH 1;"))
        conn.execute(text("ALTER SEQUENCE public.container_assignments_assignment_id_seq RESTART WITH 1;"))
        conn.execute(text("ALTER SEQUENCE public.shipments_shipment_id_seq RESTART WITH 1;"))
        conn.execute(text("ALTER SEQUENCE public.shipment_items_item_id_seq RESTART WITH 1;"))
        conn.execute(text("ALTER SEQUENCE public.payments_payment_id_seq RESTART WITH 1;"))
        conn.execute(text("ALTER SEQUENCE public.fuel_logs_fuel_log_id_seq RESTART WITH 1;"))
        conn.execute(text("ALTER SEQUENCE public.damage_reports_damage_id_seq RESTART WITH 1;"))
        conn.execute(text("ALTER SEQUENCE public.truck_services_service_id_seq RESTART WITH 1;"))
        print("[Seeder] Tables cleared and sequences reset successfully.")

        # 4. Insert Trucks
        print("[Seeder] Seeding trucks...")
        trucks = []
        for i in range(1, 16):
            model_info = random.choice(truck_models)
            plate = generate_indian_license_plate()
            # Random status
            status = random.choices(["ACTIVE", "ON_TRIP", "MAINTENANCE", "OUT_OF_SERVICE"], weights=[70, 15, 10, 5], k=1)[0]
            # Condition based on status or random
            condition = random.choices(["EXCELLENT", "GOOD", "FAIR", "POOR"], weights=[40, 40, 15, 5], k=1)[0]
            p_date = date(2022, 1, 1) + timedelta(days=random.randint(0, 1400))
            cost = random.randint(2500000, 6000000)
            dist = random.randint(15000, 180000)
            
            res = conn.execute(text("""
                INSERT INTO public.trucks (
                    license_plate, manufacturer, model, purchase_date, purchase_cost, 
                    capacity_tons, total_distance_travelled, truck_condition, status, 
                    last_service_date, description, is_active
                ) VALUES (
                    :plate, :manufacturer, :model, :p_date, :cost, 
                    :capacity, :dist, :condition, :status, 
                    :last_serv, :desc, TRUE
                ) RETURNING truck_id
            """), {
                "plate": plate,
                "manufacturer": model_info["manufacturer"],
                "model": model_info["model"],
                "p_date": p_date,
                "cost": cost,
                "capacity": model_info["capacity"],
                "dist": dist,
                "condition": condition,
                "status": status,
                "last_serv": p_date + timedelta(days=random.randint(100, 200)),
                "desc": f"Seeded truck fleet unit #{i}",
            })
            trucks.append(res.scalar())
        print(f"[Seeder] Seeded {len(trucks)} trucks.")

        # 5. Insert Users & Drivers
        print("[Seeder] Seeding driver users and drivers...")
        drivers = []
        for i, name in enumerate(driver_names, start=1):
            username = name.lower().replace(" ", "_")
            email = f"{username}@fleetstat.com"
            
            # Insert User first
            res_user = conn.execute(text("""
                INSERT INTO public.users (
                    username, email, password_hash, role, is_active
                ) VALUES (
                    :username, :email, :pw_hash, 'driver', TRUE
                ) RETURNING user_id
            """), {
                "username": username,
                "email": email,
                "pw_hash": driver_password_hash
            })
            uid = res_user.scalar()
            
            # Insert Driver
            dob = date(1980, 1, 1) + timedelta(days=random.randint(0, 7300))
            join = date(2023, 1, 1) + timedelta(days=random.randint(0, 900))
            exp = max(0, datetime.now().year - dob.year - 20)
            phone = f"{random.randint(6, 9)}{random.randint(100000000, 999999999)}"
            lic = f"DL{random.randint(10, 99)} " + "".join(random.choices("0123456789", k=11))
            addr = random.choice(locations)
            avail = random.choices(["idle", "on_trip", "off_duty"], weights=[65, 25, 10], k=1)[0]
            emp = random.choices(["active", "inactive", "suspended"], weights=[90, 8, 2], k=1)[0]

            res_driver = conn.execute(text("""
                INSERT INTO public.drivers (
                    full_name, date_of_birth, avatar_url, address, license_number, 
                    email, phone_number, prior_experience_years, employment_status, 
                    availability_status, joining_date, user_id, is_active
                ) VALUES (
                    :name, :dob, :avatar, :addr, :lic, 
                    :email, :phone, :exp, :emp, 
                    :avail, :join, :uid, TRUE
                ) RETURNING driver_id
            """), {
                "name": name,
                "dob": dob,
                "avatar": f"https://api.dicebear.com/7.x/pixel-art/svg?seed={username}",
                "addr": addr,
                "lic": lic,
                "email": email,
                "phone": phone,
                "exp": exp,
                "emp": emp,
                "avail": avail,
                "join": join,
                "uid": uid
            })
            drivers.append(res_driver.scalar())
        print(f"[Seeder] Seeded {len(drivers)} drivers and users.")

        # 6. Insert Customers
        print("[Seeder] Seeding customers...")
        customers = []
        for cust in customer_list:
            email = f"contact@{cust['name'].lower().replace(' ', '').replace('ltd','').replace('private','')}.com"
            phone = f"022-{random.randint(20000000, 89999999)}"
            addr = random.choice(locations)
            gst = generate_gst_number()
            
            res = conn.execute(text("""
                INSERT INTO public.customers (
                    customer_type, customer_name, gst_number, email, 
                    phone_number, address, is_active
                ) VALUES (
                    :type, :name, :gst, :email, 
                    :phone, :addr, TRUE
                ) RETURNING customer_id
            """), {
                "type": cust["type"],
                "name": cust["name"],
                "gst": gst,
                "email": email,
                "phone": phone,
                "addr": f"HQ: {addr}"
            })
            customers.append(res.scalar())
        print(f"[Seeder] Seeded {len(customers)} customers.")

        # 7. Insert Containers
        print("[Seeder] Seeding containers...")
        containers = []
        c_types = ["DRY VAN", "REEFER", "FLAT RACK", "OPEN TOP", "INSULATED"]
        for i in range(1, 31):
            code = f"FSCU{random.randint(100000, 999999)}"
            c_type = random.choice(c_types)
            cap = random.choice([10000.0, 15000.0, 20000.0, 24000.0])
            status = random.choices(["AVAILABLE", "IN_USE", "MAINTENANCE"], weights=[70, 20, 10], k=1)[0]
            
            res = conn.execute(text("""
                INSERT INTO public.containers (
                    container_code, container_type, capacity_kg, status, 
                    description, is_active
                ) VALUES (
                    :code, :type, :cap, :status, 
                    :desc, TRUE
                ) RETURNING container_id
            """), {
                "code": code,
                "type": c_type,
                "cap": cap,
                "status": status,
                "desc": f"Standard capacity {c_type} shipping unit #{i}"
            })
            containers.append(res.scalar())
        print(f"[Seeder] Seeded {len(containers)} containers.")

        # 8. Insert Trips, Assignments, Containers, Shipments, Items, Payments, Fuel Logs, Damage Reports
        print("[Seeder] Seeding trips, assignments, shipments, and payments (historical 12-month data)...")
        now_dt = datetime.now()
        start_date = now_dt - timedelta(days=365) # Back 12 months
        
        # We will seed 350 trips distributed across the timeline
        total_trips_to_seed = 350
        
        trip_statuses = ["COMPLETED", "IN_PROGRESS", "PLANNED", "CANCELLED"]
        trip_status_weights = [78, 10, 8, 4]
        
        for t_idx in range(total_trips_to_seed):
            # Select random status
            status = random.choices(trip_statuses, weights=trip_status_weights, k=1)[0]
            
            # Select truck and driver
            truck_id = random.choice(trucks)
            driver_id = random.choice(drivers)
            
            # Set timing based on status
            if status == "COMPLETED" or status == "CANCELLED":
                # Random timestamp in the past year
                days_offset = random.randint(0, 360)
                start_dt = start_date + timedelta(days=days_offset, hours=random.randint(0, 23), minutes=random.randint(0, 59))
                # Duration 12h to 96h
                duration_hours = random.randint(12, 96)
                end_dt = start_dt + timedelta(hours=duration_hours)
                actual_start = start_dt
                actual_end = end_dt if status == "COMPLETED" else None
            elif status == "IN_PROGRESS":
                # Start within last 36 hours
                start_dt = now_dt - timedelta(hours=random.randint(4, 36))
                end_dt = None
                actual_start = start_dt
                actual_end = None
            else: # PLANNED
                # Start in next 1 to 7 days
                start_dt = now_dt + timedelta(days=random.randint(1, 7), hours=random.randint(8, 18))
                end_dt = None
                actual_start = None
                actual_end = None

            start_loc = random.choice(locations)
            end_loc = random.choice(locations)
            while start_loc == end_loc:
                end_loc = random.choice(locations)
                
            dist = round(random.uniform(150.0, 1500.0), 2)
            
            # Mileage between 3.5 and 7.5 km/liter
            mileage = random.uniform(3.5, 7.5)
            fuel_used = round(dist / mileage, 2)
            
            # Insert Trip
            res_trip = conn.execute(text("""
                INSERT INTO public.trips (
                    truck_id, start_location, end_location, trip_distance, 
                    fuel_used, start_time, end_time, trip_status, 
                    actual_start_time, actual_end_time
                ) VALUES (
                    :truck_id, :start_loc, :end_loc, :dist, 
                    :fuel, :start_time, :end_time, :status, 
                    :act_start, :act_end
                ) RETURNING trip_id
            """), {
                "truck_id": truck_id,
                "start_loc": start_loc,
                "end_loc": end_loc,
                "dist": dist,
                "fuel": fuel_used if status in ["COMPLETED", "IN_PROGRESS"] else None,
                "start_time": start_dt,
                "end_time": end_dt,
                "status": status,
                "act_start": actual_start,
                "act_end": actual_end
            })
            trip_id = res_trip.scalar()

            # Insert Trip Assignment
            conn.execute(text("""
                INSERT INTO public.trip_assignments (
                    trip_id, driver_id, assigned_at
                ) VALUES (
                    :trip_id, :driver_id, :assigned_at
                )
            """), {
                "trip_id": trip_id,
                "driver_id": driver_id,
                "assigned_at": start_dt - timedelta(hours=random.randint(1, 4))
            })

            # Assign 1 or 2 containers
            num_containers = random.choice([1, 2])
            assigned_containers = random.sample(containers, k=num_containers)
            
            for c_id in assigned_containers:
                conn.execute(text("""
                    INSERT INTO public.container_assignments (
                        trip_id, container_id, assigned_at
                    ) VALUES (
                        :trip_id, :c_id, :assigned_at
                    )
                """), {
                    "trip_id": trip_id,
                    "c_id": c_id,
                    "assigned_at": start_dt - timedelta(hours=random.randint(1, 4))
                })

            # Create Fuel Log for completed/in-progress trips
            if status in ["COMPLETED", "IN_PROGRESS"]:
                # Let's say fuel price is around 94 to 98 Rs/liter
                fuel_price = random.uniform(94.0, 98.0)
                fuel_cost = round(fuel_used * fuel_price, 2)
                
                conn.execute(text("""
                    INSERT INTO public.fuel_logs (
                        truck_id, trip_id, fuel_amount, fuel_cost, filled_at
                    ) VALUES (
                        :truck_id, :trip_id, :amount, :cost, :filled_at
                    )
                """), {
                    "truck_id": truck_id,
                    "trip_id": trip_id,
                    "amount": fuel_used,
                    "cost": fuel_cost,
                    "filled_at": start_dt
                })

            # Create Shipments (1 shipment per assigned container)
            for c_id in assigned_containers:
                sender = random.choice(customers)
                receiver = random.choice(customers)
                while sender == receiver:
                    receiver = random.choice(customers)
                
                # Determine shipment status based on trip status
                if status == "COMPLETED":
                    shipment_status = random.choices(["DELIVERED", "DAMAGED"], weights=[96, 4], k=1)[0]
                elif status == "IN_PROGRESS":
                    shipment_status = "IN_TRANSIT"
                elif status == "CANCELLED":
                    shipment_status = "CANCELLED"
                else: # PLANNED
                    shipment_status = "RECEIVED"
                    
                rec_date = (start_dt - timedelta(days=1)).date()
                shp_date = start_dt.date() if status in ["COMPLETED", "IN_PROGRESS", "CANCELLED"] else None
                del_date = end_dt.date() if shipment_status in ["DELIVERED", "DAMAGED"] else None
                
                res_ship = conn.execute(text("""
                    INSERT INTO public.shipments (
                        container_id, sender_customer_id, receiver_customer_id, 
                        shipment_status, received_date, shipped_date, delivered_date, 
                        notes, trip_id
                    ) VALUES (
                        :c_id, :sender, :receiver, 
                        :status, :rec_date, :shp_date, :del_date, 
                        :notes, :trip_id
                    ) RETURNING shipment_id
                """), {
                    "c_id": c_id,
                    "sender": sender,
                    "receiver": receiver,
                    "status": shipment_status,
                    "rec_date": rec_date,
                    "shp_date": shp_date,
                    "del_date": del_date,
                    "notes": f"Bulk logistics shipment - Trip #{trip_id}",
                    "trip_id": trip_id
                })
                shipment_id = res_ship.scalar()
                
                # Insert shipment items
                num_items = random.randint(1, 3)
                selected_item_templates = random.sample(shipment_items_pool, k=num_items)
                
                total_weight = 0
                for item_temp in selected_item_templates:
                    quantity = random.randint(1, 5)
                    weight = item_temp["weight"] * quantity
                    total_weight += weight
                    declared = item_temp["val"] * quantity
                    temp = item_temp.get("temp")
                    
                    conn.execute(text("""
                        INSERT INTO public.shipment_items (
                            shipment_id, item_name, quantity, weight_kg, 
                            declared_value, temperature_required
                        ) VALUES (
                            :shipment_id, :name, :qty, :weight, 
                            :val, :temp
                        )
                    """), {
                        "shipment_id": shipment_id,
                        "name": item_temp["name"],
                        "qty": quantity,
                        "weight": weight,
                        "val": declared,
                        "temp": temp
                    })
                
                # Create Payment for this shipment
                # Price logic: base charge 5,000 + distance-based charge (dist * 40) + weight-based charge (weight_kg * 3)
                base_charge = 5000.0
                dist_charge = dist * 40.0
                weight_charge = total_weight * 3.0
                payment_amount = round(base_charge + dist_charge + weight_charge, 2)
                
                # Determine payment status
                if shipment_status in ["DELIVERED", "DAMAGED"]:
                    pay_status = random.choices(["SUCCESS", "FAILED"], weights=[98, 2], k=1)[0]
                elif shipment_status == "IN_TRANSIT":
                    pay_status = random.choices(["SUCCESS", "PENDING"], weights=[40, 60], k=1)[0]
                elif shipment_status == "CANCELLED":
                    pay_status = "FAILED"
                else: # RECEIVED
                    pay_status = "PENDING"
                    
                pay_method = random.choice(["Net Banking", "UPI", "Credit Card", "Cash"])
                
                # Payment date: same or shortly after shipment date (or start time)
                pay_date = start_dt + timedelta(hours=random.randint(1, 12)) if pay_status == "SUCCESS" else None
                
                conn.execute(text("""
                    INSERT INTO public.payments (
                        shipment_id, amount, payment_method, payment_status, 
                        payment_date, remarks
                    ) VALUES (
                        :shipment_id, :amount, :method, :status, 
                        :pay_date, :remarks
                    )
                """), {
                    "shipment_id": shipment_id,
                    "amount": payment_amount,
                    "method": pay_method if pay_status != "PENDING" else None,
                    "status": pay_status,
                    "pay_date": pay_date,
                    "remarks": f"Invoice payment for shipment #{shipment_id}"
                })
                
                # If shipment status is DAMAGED, create a damage report
                if shipment_status == "DAMAGED":
                    damage_pct = round(random.uniform(5.0, 75.0), 2)
                    reported = start_dt + timedelta(hours=random.randint(6, 48))
                    d_status = random.choice(["PENDING", "UNDER_REVIEW", "RESOLVED"])
                    
                    conn.execute(text("""
                        INSERT INTO public.damage_reports (
                            shipment_id, damage_percentage, description, 
                            reported_at, status
                        ) VALUES (
                            :shipment_id, :pct, :desc, 
                            :reported_at, :status
                        )
                    """), {
                        "shipment_id": shipment_id,
                        "pct": damage_pct,
                        "desc": f"Package damaged during transit. Found issues upon unboxing. Average damage pct: {damage_pct}%",
                        "reported_at": reported,
                        "status": d_status
                    })

        print(f"[Seeder] Seeded {total_trips_to_seed} trips with consistent logistics workflows.")

        # 9. Seeding Truck Services
        print("[Seeder] Seeding truck services...")
        services_count = 0
        for trk_id in trucks:
            # Generate 1 to 3 services
            num_serv = random.randint(1, 3)
            for _ in range(num_serv):
                s_date = date(2025, 1, 1) + timedelta(days=random.randint(0, 450))
                s_cost = random.randint(5000, 35000)
                next_due = s_date + timedelta(days=random.randint(90, 180))
                centers = ["Tata Authorized Service Center", "Mahindra Heavy Fleet Service", "National Highway Repair Shop", "Volvo Truck Care Center"]
                center = random.choice(centers)
                desc = random.choice([
                    "Routine engine oil and filter replacement, brake pad inspection.",
                    "Wheel alignment, tire rotation, and suspension checkup.",
                    "Coolant system flushing, air filter replacement, general electrical diagnostic.",
                    "Clutch plate replacement and gearbox maintenance."
                ])
                
                conn.execute(text("""
                    INSERT INTO public.truck_services (
                        truck_id, service_center, service_date, service_cost, 
                        next_due_date, description
                    ) VALUES (
                        :truck_id, :center, :s_date, :cost, 
                        :due, :desc
                    )
                """), {
                    "truck_id": trk_id,
                    "center": center,
                    "s_date": s_date,
                    "cost": s_cost,
                    "due": next_due,
                    "desc": desc
                })
                services_count += 1
        print(f"[Seeder] Seeded {services_count} truck service log entries.")

    print("\n[Seeder] Seeding completed successfully!")
    print("[Seeder] Database contains consistent mock records for the last 12 months.")

if __name__ == "__main__":
    main()
