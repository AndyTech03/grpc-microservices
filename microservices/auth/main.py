from concurrent import futures
import grpc
import uuid
import auth_pb2, auth_pb2_grpc
import logging


class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def Login(self, request, context):
        logging.info(f"Login attempt for user: {request.userLogin}")
        return auth_pb2.LoginResponse(
            accessToken=f"token-{uuid.uuid4()}"
        )

    def Auth(self, request, context):
        logging.info(f"Auth check for token: {request.accessToken}")
        return auth_pb2.AuthResponse(
            userLogin="demo_user",
            valid=True
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