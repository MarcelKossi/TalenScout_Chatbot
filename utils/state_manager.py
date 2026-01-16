class ConversationState:
    """
    Finite State Machine controlling the entire conversation flow.
    This class determines what step the chatbot is on, what information
    is required next, and when the conversation can move to question
    generation and final confirmation.
    """

    # Ordered list of required fields
    REQUIRED_FIELDS = [
        "name",
        "email",
        "phone",
        "experience_years",
        "desired_positions",
        "location",
        "tech_stack"
    ]

    def __init__(self):
        # Starts at first field
        self.current_step_index = 0
        self.current_field = self.REQUIRED_FIELDS[self.current_step_index]

        # Storage for user-provided data
        self.collected_data = {
            "name": None,
            "email": None,
            "phone": None,
            "experience_years": None,
            "desired_positions": None,
            "location": None,
            "tech_stack": None,
            "additional_notes": None  # NEW FIELD
        }

        # State flags
        self.is_complete = False
        self.final_confirmation_stage = False
        self.exit_requested = False

        # Exit keywords
        self.exit_keywords = ["exit", "quit", "stop", "end", "thank you"]

    @staticmethod
    def _normalize_message(user_message: str) -> str:
        return " ".join((user_message or "").lower().strip().split())

    @staticmethod
    def _is_missing_value(value) -> bool:
        if value is None:
            return True
        if isinstance(value, str):
            return value.strip() == ""
        if isinstance(value, (list, tuple, set, dict)):
            return len(value) == 0
        return False

    def detect_exit_intent(self, user_message: str) -> bool:
        """
        Check if the user wants to end the conversation.
        """
        if not user_message:
            return False

        message = self._normalize_message(user_message)
        if not message:
            return False

        # This avoids accidental exit when user says "thank you" as part of a longer message
        # (e.g., "thank you, my email is ..."). Only treat it as exit when it's the full message.
        if message.rstrip(".!?,") == "thank you":
            self.exit_requested = True
            return True

        # Token-based matching prevents false positives like "friend" containing "end".
        tokens = {t.strip(".!?,") for t in message.split() if t}
        for key in self.exit_keywords:
            if key == "thank you":
                continue
            if key in tokens:
                self.exit_requested = True
                return True
        return False

    def store_response(self, field_name: str, value):
        """
        Store user input safely and advance state.
        """
        if field_name not in self.collected_data:
            raise ValueError(f"Unknown field: {field_name}")

        self.collected_data[field_name] = value

        # If already complete and entering final confirmation
        if field_name == "additional_notes":
            self.exit_requested = True
            return

        # Move to next field if not finished
        if self.current_step_index < len(self.REQUIRED_FIELDS) - 1:
            self.current_step_index += 1
            self.current_field = self.REQUIRED_FIELDS[self.current_step_index]
        else:
            # All required fields collected.
            # Final confirmation should begin only after technical question generation
            # (or an attempted generation) in the app layer.
            self.is_complete = True

    def get_current_question(self) -> str:
        """
        Return the next question based on current state.
        """

        # Handle final confirmation step
        if self.final_confirmation_stage and not self.collected_data["additional_notes"]:
            return (
                "Before we conclude, is there anything important you would like to add?\n"
                "(You can reply with 'no' if you have nothing to add.)"
            )

        # Standard information-collection questions
        questions_mapping = {
            "name": "Please provide your full name (first and last name).",
            "email": "What is your email address?",
            "phone": "What is your phone number?",
            "experience_years": "How many years of professional experience do you have?",
            "desired_positions": "Which position(s) are you applying for?",
            "location": "What is your current location (city/country)?",
            "tech_stack": "Please list the programming languages, frameworks, and tools in your tech stack."
        }

        return questions_mapping.get(self.current_field, "Unexpected step encountered.")

    def missing_fields(self):
        """
        Return a list of REQUIRED fields that have not been filled yet.
        """
        return [
            field
            for field in self.REQUIRED_FIELDS
            if self._is_missing_value(self.collected_data.get(field))
        ]

    def ready_for_questions(self) -> bool:
        """
        True when all required fields are filled.
        """
        if not self.missing_fields():
            self.is_complete = True
            return True
        return False

    def needs_final_confirmation(self) -> bool:
        """
        True when all required fields are completed and
        we are ready for the final add-notes question.
        """
        return self.is_complete and self.final_confirmation_stage

    def reset(self):
        """
        Reset conversation state completely.
        """
        self.__init__()
