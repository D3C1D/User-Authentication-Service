from fastapi import (
    HTTPException,
    status
)


class InvalidCredentialsException(
    HTTPException
):

    def __init__(self):

        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


class InvalidTokenException(
    HTTPException
):

    def __init__(self):

        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


class UserNotFoundException(
    HTTPException
):

    def __init__(self):

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


class AdminAccessRequiredException(
    HTTPException
):

    def __init__(self):

        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
