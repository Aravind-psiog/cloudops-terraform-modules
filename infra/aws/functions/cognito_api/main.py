from fastapi import FastAPI, HTTPException, Request
import boto3
import uuid  # For generating unique usernames
from cognito_api.services import resources, config_service
from cognito_api.models.request_model import SignInRequest, SignUpRequest, VerifyRequest
from starlette.middleware.cors import CORSMiddleware
from mangum import Mangum

config_service.load_config()
lambdaPaths = resources.lambda_path()
cognitoConfigs = resources.cognito()


if lambdaPaths["staging"] is None:
    fastapi_doc = None
else:
    fastapi_doc = f'{lambdaPaths["staging"]}/{lambdaPaths["resource"]}'

app = FastAPI(root_path=fastapi_doc)

COGNITO_REGION = cognitoConfigs["cognito_region"]
COGNITO_USER_POOL_ID = cognitoConfigs["cognito_user_pool"]
COGNITO_CLIENT_ID = cognitoConfigs["cognito_client"]

cognito_client = boto3.client('cognito-idp', region_name=COGNITO_REGION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    """
    Add Cors Header
    ---------------

    This function will add CORS headers to HTTP responses

    Args:
        request (Request): The incoming HTTP request object
        call_next: A callable representing the next middleware or route handler in the chain.

    Returns:
        Response: The HTTP response object with added CORS headers
    """
    response = await call_next(request)
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response


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

handler = Mangum(app, api_gateway_base_path=lambdaPaths["resource"])
