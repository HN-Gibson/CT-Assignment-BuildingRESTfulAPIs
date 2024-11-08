from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from db_connect_and_create import get_db_connection
from mysql.connector import Error


app = Flask(__name__)
ma  = Marshmallow(app)

class MemberSchema(ma.Schema):
    member_id = fields.String(required=True)
    name = fields.String(required=True)
    age = fields.String(required=True)

    class Meta:
        fields = ("id", "name", "age")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

@app.route('/')
def home():
    return 'Welcome to the Gym!'

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



if __name__ == '__main__':
    app.run(debug=True)