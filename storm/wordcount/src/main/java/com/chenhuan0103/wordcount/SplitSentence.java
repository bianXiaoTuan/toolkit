package com.chenhuan0103.wordcount;

import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.task.TopologyContext;
import backtype.storm.task.OutputCollector;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Values;
import backtype.storm.tuple.Tuple;

import java.util.Map;
import java.util.StringTokenizer;

/**
 * Created by chenhuan on 16/1/25.
 */
public class SplitSentence extends BaseRichBolt{
    private OutputCollector _collector;

    @Override
    public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
        _collector = collector;
    }

    @Override
    public void execute(Tuple tuple) {
        String sentence = tuple.getString(0);
        StringTokenizer iter = new StringTokenizer(sentence);
        while(iter.hasMoreElements()) {
            _collector.emit(new Values(iter.nextToken()));
        }
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("word"));
    }
}