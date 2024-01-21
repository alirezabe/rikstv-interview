resource "docker_container" "zoo1" {
  image = docker_image.zookeeper_image.name
  name  = "zoo1"
  hostname = "zoo1"
  restart = "always"
  volumes {
    container_path  = "/var/lib/zookeeper"
    volume_name     = docker_volume.zoo1data.name
    read_only       = false
  }
  ports {
    internal = 2181
    external = 2181
  }
  env = [
    "ZOOKEEPER_CLIENT_PORT=2181",
    "ZOOKEEPER_SERVER_ID=1",
    "ZOOKEEPER_SERVERS=zoo1:2888:3888;zoo2:2888:3888;zoo3:2888:3888"
  ]
}

resource "docker_container" "zoo2" {
  image = docker_image.zookeeper_image.name
  name  = "zoo2"
  hostname = "zoo2"
  restart = "always"
  volumes {
    container_path  = "/var/lib/zookeeper"
    volume_name     = docker_volume.zoo2data.name
    read_only       = false
  }
  ports {
    internal = 2181
    external = 2181
  }
  env = [
    "ZOOKEEPER_CLIENT_PORT=2181",
    "ZOOKEEPER_SERVER_ID=1",
    "ZOOKEEPER_SERVERS=zoo1:2888:3888;zoo2:2888:3888;zoo3:2888:3888"
  ]
}

resource "docker_container" "zoo3" {
  image = docker_image.zookeeper_image.name
  name  = "zoo1"
  hostname = "zoo1"
  restart = "always"
  volumes {
    container_path  = "/var/lib/zookeeper"
    volume_name     = docker_volume.zoo3data.name
    read_only       = false
  }
  ports {
    internal = 2181
    external = 2181
  }
  env = [
    "ZOOKEEPER_CLIENT_PORT=2181",
    "ZOOKEEPER_SERVER_ID=1",
    "ZOOKEEPER_SERVERS=zoo1:2888:3888;zoo2:2888:3888;zoo3:2888:3888"
  ]
}

// Define Docker Containers for Kafka (kafka1)
resource "docker_container" "kafka1" {
  image = docker_image.kafka_image.name
  name  = "kafka1"
  hostname = "kafka1"
  restart = "always"
  volumes {
    container_path  = "/var/lib/kafka/data"
    volume_name     = docker_volume.kafka1data.name
    read_only       = false
  }
  ports {
    internal = 9092
    external = 9092
  }
  ports {
   internal = 29092
    external = 29092
  }
  env = [
    "KAFKA_ADVERTISED_LISTENERS=INTERNAL://kafka1:19092,DOCKER://host.docker.internal:29092",
    "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT,DOCKER:PLAINTEXT",
    "KAFKA_INTER_BROKER_LISTENER_NAME=INTERNAL",
    "KAFKA_ZOOKEEPER_CONNECT=zoo1:2181,zoo2:2182,zoo3:2183",
    "KAFKA_BROKER_ID=1",
    "KAFKA_LOG4J_LOGGERS=kafka.controller=INFO,kafka.producer.async.DefaultEventHandler=INFO,state.change.logger=INFO",
    "KAFKA_AUTHORIZER_CLASS_NAME=kafka.security.authorizer.AclAuthorizer",
    "KAFKA_ALLOW_EVERYONE_IF_NO_ACL_FOUND=true"
  ]
  depends_on = [docker_container.zoo1, docker_container.zoo2, docker_container.zoo3]
}

resource "docker_container" "kafka2" {
  image = docker_image.kafka_image.name
  name  = "kafka1"
  hostname = "kafka1"
  restart = "always"
  volumes {
    container_path  = "/var/lib/kafka/data"
    volume_name     = docker_volume.kafka2data.name
    read_only       = false
  }
  ports {
    internal = 9093
    external = 9093
  }
  ports {
   internal = 29093
    external = 29093
  }
  env = [
    "KAFKA_ADVERTISED_LISTENERS=INTERNAL://kafka2:19093,DOCKER://host.docker.internal:29093",
    "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT,DOCKER:PLAINTEXT",
    "KAFKA_INTER_BROKER_LISTENER_NAME=INTERNAL",
    "KAFKA_ZOOKEEPER_CONNECT=zoo1:2181,zoo2:2182,zoo3:2183",
    "KAFKA_BROKER_ID=2",
    "KAFKA_LOG4J_LOGGERS=kafka.controller=INFO,kafka.producer.async.DefaultEventHandler=INFO,state.change.logger=INFO",
    "KAFKA_AUTHORIZER_CLASS_NAME=kafka.security.authorizer.AclAuthorizer",
    "KAFKA_ALLOW_EVERYONE_IF_NO_ACL_FOUND=true"
  ]
  depends_on = [docker_container.zoo1, docker_container.zoo2, docker_container.zoo3]
}

resource "docker_container" "kafka3" {
  image = docker_image.kafka_image.name
  name  = "kafka1"
  hostname = "kafka1"
  restart = "always"
  volumes {
    container_path  = "/var/lib/kafka/data"
    volume_name     = docker_volume.kafka1data.name
    read_only       = false
  }
  ports {

    internal = 9094
    external = 9094
  }
  ports {
   internal = 29094
    external = 29094
  }
  env = [
    "KAFKA_ADVERTISED_LISTENERS=INTERNAL://kafka2:19094,DOCKER://host.docker.internal:29094",
    "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT,DOCKER:PLAINTEXT",
    "KAFKA_INTER_BROKER_LISTENER_NAME=INTERNAL",
    "KAFKA_ZOOKEEPER_CONNECT=zoo1:2181,zoo2:2182,zoo3:2183",
    "KAFKA_BROKER_ID=3",
    "KAFKA_LOG4J_LOGGERS=kafka.controller=INFO,kafka.producer.async.DefaultEventHandler=INFO,state.change.logger=INFO",
    "KAFKA_AUTHORIZER_CLASS_NAME=kafka.security.authorizer.AclAuthorizer",
    "KAFKA_ALLOW_EVERYONE_IF_NO_ACL_FOUND=true"
  ]
  depends_on = [docker_container.zoo1, docker_container.zoo2, docker_container.zoo3]
}

// Repeat kafka2 and kafka3 configuration here with changes for names, ports, and other specific settings

// Define Docker Containers for Metabase
resource "docker_container" "metabase" {
  image = docker_image.metabase_image.name
  name  = "metabase"
  hostname = "metabase"
  restart = "always"
  ports {
    internal = 3000
    external = 3000
  }
  env = [
    "MB_DB_TYPE=postgres",
    "MB_DB_DBNAME=metabase",
    "MB_DB_PORT=5432",
    "MB_DB_USER=postgres",
    "MB_DB_PASS=password@@@",
    "MB_DB_HOST=postgres",
    "DB_PASSWORD=",
    "DB_USER="
  ]
  volumes {
    container_path = "/dev/random"
    host_path      = "/dev/urandom"
    read_only      = true
  }
  volumes {
    container_path = "/plugins/clickhouse.jar"
    host_path      = abspath("../plugins/clickhouse.metabase-driver.jar")
    read_only      = true
  }
  healthcheck {
    test     = ["CMD", "curl", "--fail", "-I", "http://localhost:3000/api/health"]
    interval = "15s"
    timeout  = "5s"
    retries  = 5
  }

}

// Define Docker Containers for Postgres
resource "docker_container" "postgres" {
  image = docker_image.postgres_image.name
  name  = "postgres"
  hostname = "postgres"
  restart = "always"
  env = [
    "POSTGRES_USER=postgres",
    "POSTGRES_DB=metabase",
    "POSTGRES_PASSWORD=password@@@",
  ]
  volumes {
    container_path  = "/var/lib/postgresql/data"
    volume_name     = docker_volume.pgdata.name
    read_only       = false
  }
}

// Define Docker Containers for Producer
resource "docker_container" "producer" {
  image = docker_image.producer_image.name
  name  = "producer"
  env = [
    "KAFKA_TOPIC_NAME=python.test",
    "KAFKA_GROUP_ID=matine",
    "VAULT_TOKEN='TOKEN'",
    "VAULT_PATH=",
    "PARTITIONS=10",
    "REPLICATION_FACTOR=3",
    "BOOTSTRAP_SERVERS=172.16.40.40:9092,172.16.40.40:9093,172.16.40.40:9094",
    "CLICKHOUSE_HOST=172.16.40.40",
    "CLICKHOUSE_PORT=18123",
    "CLICKHOUSE_USER=default",
    "CLICKHOUSE_PASSWORD=",
    "CLICKHOUSE_DB=rikstv",
    "CLICKHOUSE_TABLE=data_series"
  ]
  depends_on = [
    docker_container.kafka1,
    docker_container.kafka2,
    docker_container.kafka3,
    null_resource.serverless_execution
  ]
}

// Define Docker Containers for Consumer
resource "docker_container" "consumer" {
  image = docker_image.consumer_image.name
  name  = "consumer"
  env = [
    "KAFKA_TOPIC_NAME=python.test",
    "KAFKA_GROUP_ID=matine",
    "VAULT_TOKEN='TOKEN'",
    "VAULT_PATH=",
    "PARTITIONS=10",
    "REPLICATION_FACTOR=3",
    "BOOTSTRAP_SERVERS=172.16.40.40:9092,172.16.40.40:9093,172.16.40.40:9094",
    "CLICKHOUSE_HOST=172.16.40.40",
    "CLICKHOUSE_PORT=18123",
    "CLICKHOUSE_USER=default",
    "CLICKHOUSE_PASSWORD=",
    "CLICKHOUSE_DB=rikstv",
    "CLICKHOUSE_TABLE=data_series"
  ]
  depends_on = [
    docker_container.kafka1,
    docker_container.kafka2,
    docker_container.kafka3,
    docker_container.clickhouse_server,
    docker_container.producer,
    null_resource.serverless_execution
  ]
}

// Define Docker Containers for App
resource "docker_container" "app" {
  image = docker_image.app_image.name
  name  = "app"
  ports {
    internal = 8000
    external = 80
  }
  command = ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
  env = [
    "CLICKHOUSE_HOST=172.16.40.40",
    "CLICKHOUSE_PORT=18123",
    "CLICKHOUSE_USER=default",
    "CLICKHOUSE_PASSWORD=",
    "CLICKHOUSE_DB=rikstv",
    "CLICKHOUSE_TABLE=data_series"
  ]
  depends_on = [
    docker_container.clickhouse_server,
    null_resource.serverless_execution
  ]
}

// Define Docker Containers for Kafka UI
resource "docker_container" "kafka_ui" {
  image = docker_image.kafka_ui_image.name
  name  = "kafka-ui"
  ports {
    internal = 8080
    external = 8080
  }
  env = [
    "DYNAMIC_CONFIG_ENABLED=true"
  ]
  volumes {
    container_path  = "/etc/kafkaui/"
    volume_name     = docker_volume.kuidata.name
    read_only       = false
  }
}

// Define Docker Containers for Clickhouse Server
resource "docker_container" "clickhouse_server" {
  image = docker_image.clickhouse_image.name
  name  = "clickhouse-server"
  hostname = "clickhouse-server"
  restart = "always"
  ports {
    internal = 8123
    external = 8123
  }
  volumes {
    container_path  = "/var/lib/clickhouse"
    volume_name     = docker_volume.clickhousedata.name
    read_only       = false
  }
}


resource "null_resource" "serverless_execution" {
  triggers  =  { always_run = timestamp() }

  provisioner "local-exec" {
    command = "../../build-all.sh"
  }
}
