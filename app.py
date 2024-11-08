from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from db_connect_and_create import get_db_connection
from mysql.connector import Error


app = Flask(__name__)
ma  = Marshmallow(app)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Member and Workout Schema

class MemberSchema(ma.Schema):
    member_id = fields.String(dump_only=True)
    name = fields.String(required=True)
    age = fields.String(required=True)

    class Meta:
        fields = ("id", "name", "age")

class WorkoutSchema(ma.Schema):
    session_id = fields.String(dump_only=True)
    member_id = fields.String(required=True)
    # date = fields.String(required=True)
    duration_minutes = fields.String(required=True)
    calories_burned = fields.String(required=True)

    class Meta:
        fields = ("session_id", "member_id", "date", "duration_minutes", "calories_burned")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Welcome Page Route

@app.route('/')
def home():
    return 'Welcome to the Gym!'

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# View All Members Route

@app.route("/members", methods=["GET"])
def get_members():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error":"Database connection failed"}), 500
        cursor = conn.cursor(dictionary = True)

        query = "SELECT * FROM members"

        cursor.execute(query)

        members = cursor.fetchall()

        return members_schema.jsonify(members)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error":"Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Add Member Route

@app.route("/members", methods=["POST"])
def add_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error":"Database connection failed"}), 500
        cursor = conn.cursor()

        new_member = (member_data['name'], member_data['age'])

        query = "INSERT INTO members (name,age) VALUES (%s, %s)"

        cursor.execute(query, new_member)
        conn.commit()

        return jsonify({"message":"New member successfully added"}), 201  
          
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Update Member Route

@app.route("/members/<int:id>", methods=["PUT"])
def update_member(id):
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error":"Database connection failed"}), 500
        cursor = conn.cursor()

        updated_member = (member_data['name'], member_data['age'], id)

        query = "UPDATE members SET name = %s, age = %s WHERE id = %s"

        cursor.execute(query,updated_member)
        conn.commit()

        return jsonify({"message":"Member updated successfully"}), 201  
          
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Delete Member Route

@app.route("/members/<int:id>", methods=["DELETE"])
def delete_member(id):   
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error":"Database connection failed"}), 500
        cursor = conn.cursor()

        member_to_remove = (id,)

        cursor.execute("SELECT * from members WHERE id = %s", member_to_remove)
        customer = cursor.fetchone()
        if not customer:
            return jsonify({"error": "customer not found"}), 404
        
        query = "DELETE from members WHERE id = %s"
        cursor.execute(query,member_to_remove)
        conn.commit()

        return jsonify({"message":"Customer removed successfully"}), 200  
          
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Add Workout Route

@app.route("/workouts", methods=["POST"])
def add_workout():
    try:
        workout_data = workout_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error":"Database connection failed"}), 500
        cursor = conn.cursor()

        new_workout = (workout_data['member_id'], workout_data['duration_minutes'], workout_data['calories_burned'])

        query = "INSERT INTO workoutsessions (member_id, date, duration_minutes, calories_burned) VALUES (%s, CURRENT_TIMESTAMP(), %s, %s)"

        cursor.execute(query, new_workout)
        conn.commit()

        return jsonify({"message":"New workout successfully added"}), 201  
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error":"Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Update Workout Route


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# View Member Workouts Route

@app.route("/workouts/<int:member_id>", methods=["GET"])
def get_member_workouts(member_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error":"Database connection failed"}), 500
        cursor = conn.cursor(dictionary = True)

        query = "SELECT * FROM workoutsessions WHERE member_id=%s"

        cursor.execute(query, (member_id,))

        workouts = cursor.fetchall()

        return workouts_schema.jsonify(workouts)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error":"Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# View All Workouts Route

@app.route("/workouts", methods=["GET"])
def get_workouts():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error":"Database connection failed"}), 500
        cursor = conn.cursor(dictionary = True)

        query = "SELECT * FROM workoutsessions"

        cursor.execute(query)

        workouts = cursor.fetchall()

        return workouts_schema.jsonify(workouts)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error":"Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Run in Debug

if __name__ == '__main__':
    app.run(debug=True)