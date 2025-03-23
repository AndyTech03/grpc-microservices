import os
import shutil

microservices_folder = 'microservices'
envoy_proto_dir = os.path.join('envoy', 'proto')
proto_pb_path = os.path.join('envoy', 'proto.pb')

# Установка кодовой страницы UTF-8 для консоли Windows
os.system('chcp 65001 > nul')

# Создаем структуру каталогов
os.makedirs(envoy_proto_dir, exist_ok=True)

# Получаем абсолютный путь к googleapis
gopath = os.environ.get('GOPATH', '')
if not gopath:
    raise EnvironmentError("GOPATH environment variable is not set")
googleapis_path = os.path.join(gopath, 'src', 'googleapis')

for folder in next(os.walk(microservices_folder))[1]:
    service_path = os.path.join(microservices_folder, folder)
    proto_file = os.path.join(service_path, f"{folder}.proto")
    
    if not os.path.exists(proto_file):
        continue
    
    # Генерация кодов и swagger
    cmd = (
        f'python -m grpc_tools.protoc '
        f'-I{service_path} '
        f'-I{googleapis_path} '
        f'--proto_path=. '
        f'--python_out={service_path} '
        f'--grpc_python_out={service_path} '
        f'--swagger_out=logtostderr=true,allow_delete_body=true:{service_path} '
        f'{proto_file}'
    )
    exit_code = os.system(cmd)
    if exit_code != 0:
        print(f"Error generating code for {folder}")
        continue
    
    # Копируем .proto файлы
    for file in os.listdir(service_path):
        if file.endswith('.proto'):
            src = os.path.join(service_path, file)
            dst = os.path.join(envoy_proto_dir, file)
            shutil.copy(src, dst)

# Генерация descriptor set
proto_files = ' '.join([f'"{os.path.join(envoy_proto_dir, f)}"' for f in os.listdir(envoy_proto_dir) if f.endswith('.proto')])
cmd = (
    f'protoc '
    f'-I. -I"{googleapis_path}" '
    f'--proto_path=. '
    f'--include_imports '
    f'--descriptor_set_out="{proto_pb_path}" '
    f'{proto_files}'
)
exit_code = os.system(cmd)
if exit_code != 0:
    print("Error generating descriptor set")

# Очистка временных файлов
shutil.rmtree(envoy_proto_dir, ignore_errors=True)