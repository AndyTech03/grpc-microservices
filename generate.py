import os

microservices_folder = 'microservices'

os.system('mkdir envoy\\proto\\')
for folder in next(os.walk(microservices_folder))[1]:
	path = f'{microservices_folder}/{folder}'
	os.system(
		f'python -m grpc_tools.protoc ' +
		f'-I{path} ' +
		r'-I%GOPATH%/src/googleapis ' +
		f'--proto_path=. ' +
		f'--python_out={path} ' +
		f'--grpc_python_out={path} ' +
		f'--swagger_out=logtostderr=true,allow_delete_body=true:{path} ' +
		f'{folder}.proto'
		)
	os.system(f'copy {path}/*.proto envoy/proto/ > nul'.replace('/', '\\'))

os.system(
	r'protoc ' +
	r'-I. -I%GOPATH%/src/googleapis ' +
	'--proto_path=. ' +
	'--include_imports ' +
	'--descriptor_set_out=./envoy/proto.pb ' +
	'envoy/proto/*.proto '
	)
os.system('del envoy\\proto\\*.proto > nul')
os.system('rmdir envoy\\proto\\')