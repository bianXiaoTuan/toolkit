package com.chenhuan0103.wordcount;

/**
 * Created by chenhuan on 16/1/22.
 */
import backtype.storm.Config;
import backtype.storm.tuple.Fields;
import backtype.storm.LocalCluster;
import backtype.storm.StormSubmitter;
import backtype.storm.topology.TopologyBuilder;

public class WordCount {
    public static void main(String[] args) throws Exception {
        TopologyBuilder builder = new TopologyBuilder();

        builder.setSpout("spout", new RandomSentence(), 2);
        builder.setBolt("split", new SplitSentence(), 1).shuffleGrouping("spout");
        builder.setBolt("count", new Count(), 1).fieldsGrouping("split", new Fields("word"));

        Config conf = new Config();
        conf.setDebug(true);

        if (args != null && args.length > 0) {
            conf.setNumWorkers(3);

            StormSubmitter.submitTopologyWithProgressBar(args[0], conf, builder.createTopology());
        }
        else {
            conf.setMaxTaskParallelism(3);

            LocalCluster cluster = new LocalCluster();
            cluster.submitTopology("word-count", conf, builder.createTopology());

            Thread.sleep(10000);

            cluster.shutdown();
        }
    }
}
