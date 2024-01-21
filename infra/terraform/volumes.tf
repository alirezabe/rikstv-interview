resource "docker_volume" "zoo1data" {
  name = "zoo1data"
}

resource "docker_volume" "zoo2data" {
  name = "zoo2data"
}

resource "docker_volume" "zoo3data" {
  name = "zoo3data"
}

resource "docker_volume" "kafka1data" {
  name = "kafka1data"
}

resource "docker_volume" "kafka2data" {
  name = "kafka2data"
}

resource "docker_volume" "kafka3data" {
  name = "kafka3data"
}

resource "docker_volume" "pgdata" {
  name = "pgdata"
}

resource "docker_volume" "clickhousedata" {
  name = "clickhousedata"
}

resource "docker_volume" "kuidata" {
  name = "kuidata"
}