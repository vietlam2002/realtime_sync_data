FROM quay.io/debezium/connect:latest

# Install PostgreSQL JDBC Driver
RUN curl -L https://jdbc.postgresql.org/download/postgresql-42.5.0.jar -o /kafka/libs/postgresql-42.5.0.jar

# USER root
# # Install Confluent Hub Client
# RUN curl -sL --http1.1 https://client.hub.confluent.io/confluent-hub-client-latest.tar.gz | tar -xz -C /usr/local \
#     && export PATH=$PATH:/usr/local/confluent-hub-client/bin

# # Install Kafka JDBC Connector
# RUN confluent-hub install confluentinc/kafka-connect-jdbc:latest --no-prompt