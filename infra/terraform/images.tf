resource "docker_image" "zookeeper_image" {
  name = "confluentinc/cp-zookeeper:7.3.2"
}

resource "docker_image" "kafka_image" {
  name = "confluentinc/cp-kafka:7.3.2"
}

resource "docker_image" "metabase_image" {
  name = "metabase/metabase:latest"
}

resource "docker_image" "postgres_image" {
  name = "postgres:latest"
}

resource "docker_image" "kafka_ui_image" {
  name = "provectuslabs/kafka-ui:latest"
}

resource "docker_image" "producer_image" {
  name = "producer"
}

resource "docker_image" "consumer_image" {
  name = "consumer"
}

resource "docker_image" "app_image" {
  name = "app"
}

resource "docker_image" "clickhouse_image" {
  name = "yandex/clickhouse-server:latest"
}