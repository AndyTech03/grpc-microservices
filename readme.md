Скачиваем googleapis глобально
`git clone https://fuchsia.googlesource.com/third_party/googleapis %GOPATH%/src/googleapis`

Скачиваем protoc версии 29.0
`https://github.com/protocolbuffers/protobuf/releases/download/v29.0/protoc-29.0-win64.zip`

Скачиваем плагины
`go install github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger@latest`
`go install google.golang.org/protobuf/cmd/protoc-gen-go@latest`
`go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest`

## Сборка
Генерируем gRpc и Swagger для всех .proto файлов
`python generate.py`

Собираем Compose (весь)
`docker-compose build`


Собираем Compose (по сервисам)
`docker-compose build auth-service`
`docker-compose build posts-service`
`docker-compose build users-service`

## Запуск
Запускаем Compose (весь)
`docker-compose up`

Запускаем Compose (по сервисам)
`docker-compose up auth-service`
`docker-compose up posts-service`
`docker-compose up users-service`

