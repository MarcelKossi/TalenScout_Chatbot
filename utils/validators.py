import re


class Validators:
    """
    Centralized validation functions used to ensure clean and correct
    candidate data before storing it in the state manager.
    Each validator returns:
        - (True, cleaned_value) if valid
        - (False, error_message) if invalid
    """

    @staticmethod
    def validate_name(name: str):
        """
        Validates a full name:
        - must contain at least 2 words
        - only letters plus optional hyphens/apostrophes
        """
        if not name or not isinstance(name, str):
            return False, "Name must be a valid string."

        cleaned = name.strip()
        parts = cleaned.split()

        if len(parts) < 2:
            return False, "Please enter your first and last name."

        # Allow letters, hyphens, and apostrophes
        pattern = r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$"
        if not re.match(pattern, cleaned):
            return False, "Full name contains invalid characters."

        return True, cleaned

    @staticmethod
    def validate_email(email: str):
        """
        Validates email format using a simplified regex (not full RFC spec).
        """
        if not email or not isinstance(email, str):
            return False, "Please provide a valid email address."

        cleaned = email.strip()

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, cleaned):
            return False, "Invalid email format. Please enter a correct email."

        return True, cleaned

    @staticmethod
    def validate_phone(phone: str):
        """
        Validates phone number:
        - numeric
        - optional "+" prefix
        - minimum 7 digits
        """
        if not phone or not isinstance(phone, str):
            return False, "Please provide a valid phone number."

        cleaned = phone.strip()

        pattern = r"^\+?\d{7,15}$"
        if not re.match(pattern, cleaned):
            return False, "Invalid phone number. It should be numeric and at least 7 digits."

        return True, cleaned

    @staticmethod
    def validate_experience(years: str):
        """
        Validates years of experience:
        - must be a number
        - range 0 to 40
        """
        if not years:
            return False, "Please provide the number of years of experience."

        try:
            value = float(years)
        except ValueError:
            return False, "Years of experience must be a number."

        if value < 0.1 or value > 40.0:
            return False, "Experience must be between 0 and 40 years."

        return True, value

    @staticmethod
    def validate_positions(positions: str):
        """
        Validates desired positions:
        - must be text
        - can contain multiple positions separated by commas
        """
        if not positions or not isinstance(positions, str):
            return False, "Please provide at least one desired position."

        cleaned = positions.strip()
        if len(cleaned) < 2:
            return False, "Position name is too short or unclear."

        # Convert comma-separated string to list
        if "," in cleaned:
            position_list = [p.strip() for p in cleaned.split(",") if p.strip()]
        else:
            position_list = [cleaned]

        return True, position_list

    @staticmethod
    def validate_location(location: str):
        """
        Validates current location:
        - must be text
        - ensures not empty
        """
        if not location or not isinstance(location, str):
            return False, "Please provide a valid location."

        cleaned = location.strip()
        if len(cleaned) < 2:
            return False, "Location seems too short. Please specify city or country."

        return True, cleaned

    @staticmethod
    def validate_tech_stack(stack_input: str):
        """
        Validates tech stack input:
        - must be text
        - Option A parsing rules (comma-separated list, otherwise treat as one item)
        """
        if not stack_input or not isinstance(stack_input, str):
            return False, "Please list at least one technology."

        cleaned = stack_input.strip()
        if not cleaned:
            return False, "Tech stack input is too short."

        if "," in cleaned:
            raw_items = [t.strip() for t in cleaned.split(",") if t.strip()]
        else:
            raw_items = [cleaned]

        # Remove duplicates while preserving original casing and order
        items = []
        seen = set()
        for item in raw_items:
            if item not in seen:
                seen.add(item)
                items.append(item)

        if not items:
            return False, "Unable to extract valid technologies."

        return True, items
