import inquirer
import re


class Validations():
    def chess_club_id_validation(answers, current):
        if not re.match(r"^[A-Z]{2}\d{5}$", current):
            reason_string = "Chess club ID must be two characters followed by 5 digits (example: AB12345)."
            raise inquirer.errors.ValidationError("", reason=reason_string)
        return True

    def date_validation(answers, current):
        if not re.match(r"^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[012])\/((19|20)\d\d)$", current):
            raise inquirer.errors.ValidationError("", reason="Date must be formatted as DD/MM/YYYY (ex: 19/10/1995)")
        return True

    def number_validation(answers, current):
        if not re.match(r"^\d*$", current):
            raise inquirer.errors.ValidationError("", reason="Must be a number.")
        return True

    def time_validation(answers, current):
        if not re.match(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", current):
            raise inquirer.errors.ValidationError("", reason="Time must be formatted as HH:MM (ex: 12:00)")
        return True
