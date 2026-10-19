from pathlib import Path
import pandas as pd
import random

class UserRepository:
    def __init__(self, users_path, preferences_path):
        self.users_path = Path(users_path)
        self.preferences_path = Path(preferences_path)

    def get_user_with_preference(self, user_id):
        if not self.users_path.exists():
            raise FileNotFoundError(f"No existe {self.users_path}")
        if not self.preferences_path.exists():
            raise FileNotFoundError(f"No existe {self.preferences_path}")

        users = pd.read_csv(self.users_path, dtype={"user_id": str}).fillna("")
        preferences = pd.read_csv(self.preferences_path, dtype={"user_id": str}).fillna("")

        required_users = {"user_id", "name", "email"}
        required_preferences = {"user_id", "category"}
        if not required_users.issubset(users.columns):
            raise ValueError(f"users.csv debe contener las columnas: {sorted(required_users)}")
        if not required_preferences.issubset(preferences.columns):
            raise ValueError(f"preferences.csv debe contener las columnas: {sorted(required_preferences)}")

        matches = users[users["user_id"].astype(str).str.strip() == str(user_id).strip()]
        if matches.empty:
            return None

        user_row = matches.iloc[0]
        preference_rows = preferences[
            preferences["user_id"].astype(str).str.strip() == str(user_id).strip()
        ]
        if preference_rows.empty:
            category = ""
        else:
            # Si existen varias preferencias, toma aleatoriamente la que va a usarse
            # category = str(preference_rows.iloc[0]["category"]).strip()
            if preference_rows.empty:
                category = ""
            else:
                categories = preference_rows["category"].dropna().astype(str).str.strip()
                categories = categories[categories != ""]

                category = random.choice(categories.tolist()) if not categories.empty else ""

        return {
            "user_id": str(user_row["user_id"]).strip(),
            "name": str(user_row["name"]).strip(),
            "email": str(user_row["email"]).strip(),
            "category": category,
        }
