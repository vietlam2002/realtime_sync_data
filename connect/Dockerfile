FROM quay.io/debezium/connect:latest

# Install PostgreSQL JDBC Driver
RUN curl -L https://jdbc.postgresql.org/download/postgresql-42.5.0.jar -o /kafka/libs/postgresql-42.5.0.jar

RUN curl -L https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-8.0.30.tar.gz -o /tmp/mysql-connector-java-8.0.30.tar.gz \
    && tar -xvzf /tmp/mysql-connector-java-8.0.30.tar.gz -C /tmp \
    && mv /tmp/mysql-connector-java-8.0.30/mysql-connector-java-8.0.30.jar /kafka/libs/mysql-connector-java-8.0.30.jar

# USER root
# # Install Confluent Hub Client
# RUN curl -sL --http1.1 https://client.hub.confluent.io/confluent-hub-client-latest.tar.gz | tar -xz -C /usr/local \
#     && export PATH=$PATH:/usr/local/confluent-hub-client/bin

# # Install Kafka JDBC Connector
# RUN confluent-hub install confluentinc/kafka-connect-jdbc:latest --no-prompt 