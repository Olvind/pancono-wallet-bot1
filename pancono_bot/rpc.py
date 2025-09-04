# Mock RPC / blockchain interaction

database_file = "database.json"

def get_balance(user_id):
    import json
    with open(database_file, "r") as f:
        db = json.load(f)
    return db.get(str(user_id), {}).get("balance", 0.0)

def update_balance(user_id, amount):
    import json
    with open(database_file, "r") as f:
        db = json.load(f)
    user = db.get(str(user_id), {})
    user["balance"] = user.get("balance", 0.0) + amount
    db[str(user_id)] = user
    with open(database_file, "w") as f:
        json.dump(db, f, indent=4)
