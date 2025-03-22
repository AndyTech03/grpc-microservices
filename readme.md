Скачиваем googleapis
`git clone https://fuchsia.googlesource.com/third_party/googleapis`

Собираем .proto
`protoc -I. -I./googleapis --proto_path=./proto --include_imports --descriptor_set_out=proto.pb auth.proto posts.proto users.proto`