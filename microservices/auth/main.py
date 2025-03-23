from concurrent import futures
import grpc
import uuid
import auth_pb2, auth_pb2_grpc
import logging
import jwt

secret_key = "my-secret-key"

class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def Login(self, request, context):
        logging.info(f"Login attempt for user: {request.userLogin}")
        payload = { "userLogin": request.userLogin }
        jwt_token = jwt.encode(payload, secret_key, algorithm="HS256")
        return auth_pb2.LoginResponse(
            accessToken=f"token-{jwt_token}"
        )

    def Auth(self, request, context):
        logging.info(f"Auth check for token: {request.accessToken}")
        jwt_token = str(request.accessToken).replace('token-', '')
        userLogin = None
        valid = True
        try:
            decoded_token = jwt.decode(jwt_token, secret_key, algorithms=["HS256"])
            userLogin = str(decoded_token["userLogin"])
        except:
            valid = False
        return auth_pb2.AuthResponse(
            userLogin=userLogin,
            valid=valid
        )

def serve():  
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Auth Service started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()