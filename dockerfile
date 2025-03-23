# Базовый образ для сборки
FROM python

# Обновляем apt-get
RUN apt-get update

# Устанавливаем git
RUN apt-get install git

#Устанавливаем protoc
RUN apt-get install protobuf-compiler --assume-yes --no-install-recommends

# Клонируем googleapis один раз в образ
RUN git clone https://fuchsia.googlesource.com/third_party/googleapis /opt/googleapis
