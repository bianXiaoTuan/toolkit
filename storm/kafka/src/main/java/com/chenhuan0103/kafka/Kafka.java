package com.chenhuan0103.kafka;

/**
 * Created by chenhuan on 16/1/26.
 */
import backtype.storm.Config;
import backtype.storm.LocalCluster;
import backtype.storm.StormSubmitter;
import backtype.storm.spout.SchemeAsMultiScheme;
import backtype.storm.topology.BoltDeclarer;
import backtype.storm.topology.TopologyBuilder;

import java.util.UUID;

import storm.kafka.*;

public class Kafka {
    public static void main(String[] args) throws Exception {
        TopologyBuilder builder = new TopologyBuilder();

        // Init kafka spout
        BrokerHosts hosts = new ZkHosts("chenhuan0103.com:2181");
        SpoutConfig spoutConfig = new SpoutConfig(hosts, "chenhuan0103-nginx-log-topic", "/chenhuan0103-nginx-log-topic", UUID.randomUUID().toString());
        spoutConfig.scheme = new SchemeAsMultiScheme(new StringScheme());
        KafkaSpout kafkaSpout = new KafkaSpout(spoutConfig);

        builder.setSpout("kafka_spout", kafkaSpout, 1);
        builder.setBolt("split", new ProcessNginxLogBolt(), 1).shuffleGrouping("kafka_spout");
//        builder.setBolt("count", new Count(), 1).fieldsGrouping("split", new Fields("word"));

        Config conf = new Config();
        conf.setDebug(true);

        if (args != null && args.length > 0) {
            conf.setNumWorkers(3);

            StormSubmitter.submitTopologyWithProgressBar(args[0], conf, builder.createTopology());
        }
        else {
            conf.setMaxTaskParallelism(3);

            LocalCluster cluster = new LocalCluster();
            cluster.submitTopology("kafka", conf, builder.createTopology());

            Thread.sleep(10000);

            cluster.shutdown();
        }
    }
}
