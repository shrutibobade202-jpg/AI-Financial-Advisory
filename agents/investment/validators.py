import user
from utils.central_logging import setup_logging,get_logger

logger = get_logger("investment_validator")


def validate_investment_input(data:dict) -> None:
     """
    Validate minimum required fields for investment analysis.
    Raises ValueError if invalid.
    """
     if "user" not in data:
        message = "Missing 'user' section"
        logger.error(message)
        raise ValueError(message)

     if "question" not in data:
        message = "Missing user question"
        logger.error(message)
        raise ValueError(message)
    
     user = data["user"]

     if "risk_tolerance" not in user:
        message = "Missing user risk tolerance"
        logger.error(message)
        raise ValueError(message)
    
     if "assets" not in user:
        message = "Missing user assets"
        logger.error(message)
        raise ValueError(message)

     if "goals" not in user:
        message = "Missing user goals"
        logger.error(message)
        raise ValueError(message)

     if "portfolio" not in data:
        message = "Missing investment portfolio"
        logger.error(message)
        raise ValueError(message)

     if user["risk_tolerance"] not in {"Low", "Moderate", "High"}:
        message = "Invalid risk tolerance value"  
        logger.error(message)
        raise ValueError(message)
