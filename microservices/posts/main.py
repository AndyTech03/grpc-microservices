from concurrent import futures
import grpc
import posts_pb2, posts_pb2_grpc
import logging

class PostsService(posts_pb2_grpc.PostsServiceServicer):
    def __init__(self):
        self.posts = []
        self.post_id = 1

    def GetPosts(self, request, context):
        return posts_pb2.GetPostsResponse(
            posts=[p for p in self.posts if p.userLogin == request.userLogin]
        )

    def CreatePost(self, request, context):
        new_post = posts_pb2.Post(
            id=self.post_id,
            content=request.content,
            userLogin="demo_user"  # В реальности получать из метаданных
        )
        self.posts.append(new_post)
        self.post_id += 1
        return posts_pb2.CreatePostResponse(id=new_post.id)

    def DeletePost(self, request, context):
        self.posts = [p for p in self.posts if p.id != request.id]
        return posts_pb2.DeletePostResponse()

def serve():
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    posts_pb2_grpc.add_PostsServiceServicer_to_server(PostsService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    logging.info("Posts Service started on port 50052")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()