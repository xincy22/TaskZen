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