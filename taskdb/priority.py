from enum import Enum

class Priority(Enum):
    """
    Enum class for task priorities.
    """
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'

    def __str__(self):
        """
        Return the string representation of the enum member.
        """
        return self.value

    @staticmethod
    def from_string(priority_str):
        """
        Convert a string to a Priority enum member.

        Parameters:
        priority_str (str): The priority as a string.

        Returns:
        Priority: The corresponding Priority enum member.

        Raises:
        ValueError: If the priority string is invalid.
        """
        priority_str = priority_str.lower()
        if priority_str == 'high':
            return Priority.HIGH
        elif priority_str == 'medium':
            return Priority.MEDIUM
        elif priority_str == 'low':
            return Priority.LOW
        else:
            raise ValueError(f"Invalid priority: {priority_str}")