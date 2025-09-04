import json

DATABASE_FILE = "database.json"

def generate_referral_code(user_id):
    return f"PANCO{str(user_id)[-4:]}"

def process_referral(user_id, args):
    referral_code = generate_referral_code(user_id)
    if args:
        ref_code = args[0]
        with open(DATABASE_FILE, "r") as f:
            db = json.load(f)
        for uid, data in db.items():
            if generate_referral_code(uid) == ref_code:
                if user_id not in data["referrals"]:
                    data["referrals"].append(user_id)
                    db[uid] = data
                    with open(DATABASE_FILE, "w") as f:
                        json.dump(db, f, indent=4)
                break
    return referral_code
