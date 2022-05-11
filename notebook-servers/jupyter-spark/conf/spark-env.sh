#!/usr/bin/env bash

NAMESPACE=$(echo $NB_PREFIX | awk -F '/' '{print $3}')
NOTEBOOK_NAME=$(echo $NB_PREFIX | awk -F '/' '{print $4}')
SPARK_CONFIG_FILE="$SPARK_CONF_DIR/spark-defaults.conf"

if ! grep -q "spark.kubernetes.namespace" $SPARK_CONFIG_FILE; then
    echo "spark.kubernetes.namespace    $NAMESPACE" >> $SPARK_CONFIG_FILE
fi

if ! grep -q "spark.driver.host" $SPARK_CONFIG_FILE; then
    echo "spark.driver.host             $NOTEBOOK_NAME.$NAMESPACE.svc.cluster.local" >> $SPARK_CONFIG_FILE
fi
