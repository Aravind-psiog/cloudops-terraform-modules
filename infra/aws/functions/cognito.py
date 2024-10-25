from fastapi import FastAPI, HTTPException
import boto3
from pydantic import BaseModel
import uuid  # For generating unique usernames

app = FastAPI()

COGNITO_REGION = 'us-east-1'
COGNITO_USER_POOL_ID = 'us-east-1_xxxxxxxxxx'
COGNITO_CLIENT_ID = 'xxxxxxxxxxxxxxxxxxxxxxxxx'

cognito_client = boto3.client('cognito-idp', region_name=COGNITO_REGION)


class SignUpRequest(BaseModel):
    email: str
    password: str


class SignInRequest(BaseModel):
    email: str
    password: str


class VerifyRequest(BaseModel):
    email: str
    code: str


@app.post("/signup")
async def sign_up(signup_request: SignUpRequest):
    try:
        # Generate a unique username (not in email format) for Cognito's `Username` field
        unique_username = str(uuid.uuid4())

        response = cognito_client.sign_up(
            ClientId=COGNITO_CLIENT_ID,
            Username=signup_request.email,  # Use the generated unique username
            Password=signup_request.password,
            # UserAttributes=[
            #     {"Name": "email", "Value": signup_request.email},
            # ]
        )
        return {"message": "User signup successful, please verify your email."}
    except cognito_client.exceptions.UsernameExistsException:
        raise HTTPException(status_code=400, detail="User already exists.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/signin")
async def sign_in(signin_request: SignInRequest):
    try:
        response = cognito_client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                # Use email for sign-in (Cognito supports email as an alias)
                "USERNAME": signin_request.email,
                "PASSWORD": signin_request.password,
            }
        )
        return {"message": "Sign-in successful", "tokens": response["AuthenticationResult"]}
    except cognito_client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/verify")
async def verify_user(verify_request: VerifyRequest):
    try:
        response = cognito_client.confirm_sign_up(
            ClientId=COGNITO_CLIENT_ID,
            # Use email for verifying (as an alias)
            Username=verify_request.email,
            ConfirmationCode=verify_request.code
        )
        return {"message": "Email verified successfully."}
    except cognito_client.exceptions.CodeMismatchException:
        raise HTTPException(
            status_code=400, detail="Invalid verification code.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
