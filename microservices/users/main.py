from concurrent import futures
import grpc
import users_pb2, users_pb2_grpc
import logging

class UsersService(users_pb2_grpc.UsersServiceServicer):
    def __init__(self):
        self.users = set()

    def UserExists(self, request, context):
        return users_pb2.UserExistsResponse(
            exists=request.userLogin in self.users
        )

    def CreateUser(self, request, context):
        if request.userLogin in self.users:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return users_pb2.CreateUserResponse(
                message="User already exists"
            )
            
        self.users.add(request.userLogin)
        return users_pb2.CreateUserResponse(
            message="User created successfully"
        )

def serve():
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UsersServiceServicer_to_server(UsersService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    logging.info("Users Service started on port 50053")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()