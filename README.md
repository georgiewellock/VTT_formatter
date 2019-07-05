# VttFormatter 

Converts WEBVTT files into text removing timestamps and identifiers and formatting the text into paragraphs.

## Example Input/Output 

### Input

```
WEBVTT

NOTE duration:"00:00:32.5820000"

NOTE language:en-us

NOTE Confidence: 0.69450831413269

ef04c7c2-a59e-463f-9d27-b5b1259d6777
00:00:03.300 --> 00:00:06.870
Hello.

NOTE Confidence: 0.621036410331726

8a017ebb-1722-4e7f-8984-fc6da39c3489
00:00:08.100 --> 00:00:09.620
Hi there.

NOTE Confidence: 0.713402450084686

d9a1567a-1ebe-40ce-983a-98436bcabcfe
00:00:19.240 --> 00:00:20.240
Can you hear me properly?

NOTE Confidence: 0.536461710929871

b8e0fa64-8c2f-4070-9b0f-922a50f3fcde
00:00:21.930 --> 00:00:23.490
Yeah.

NOTE Confidence: 0.889019846916199

88910870-8af9-48f5-bcc4-a501eda95d3f
00:00:24.670 --> 00:00:28.778
But now my headphones are playing
up, I can still hear you though.

NOTE Confidence: 0.889019846916199

7d633414-089b-4813-9617-9533f5f215c0
00:00:28.778 --> 00:00:32.570
Well, I mean it is crackling. It 
will still be recording the audio.
```

### Output

```
Hello.

Hi there.

Can you hear me properly?

Yeah.

But now my headphones are playing up, I can still hear you though. Well, I mean it is crackling. It will still be recording the audio.
'''
