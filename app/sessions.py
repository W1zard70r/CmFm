from uuid import UUID, uuid4
from fastapi import Depends, HTTPException, Response
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from pydantic import BaseModel
from typing import Annotated


class SessionData(BaseModel):
    login: str

cookie_params = CookieParameters()
cookie = SessionCookie(
    cookie_name="session",
    identifier="general_verifier",
    secret_key="Some secret key",
    cookie_params=cookie_params,
    auto_error=True
)

backend = InMemoryBackend[UUID, SessionData]()

class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(self, *, identifier: str, auto_error: bool, backend, auth_http_exception):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier
    
    @property
    def backend(self):
        return self._backend
    
    @property
    def auto_error(self):
        return self._auto_error
    
    @property
    def auth_http_exception(self):
        return self._auth_http_exception 
    
    def verify_session(self, model: SessionData) -> bool:
        print(f"Verifying session with login: {model.login}")
        return True

verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="Invalid session")
)

SessionDataDep = Annotated[SessionData, Depends(verifier)]

async def get_session_data(session_data: SessionDataDep):
    return session_data